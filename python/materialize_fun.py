from phenospy import *
from owlready2 import *
import os
import uuid

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
set_log_level(9)



# Recursive function to find chains
def find_chains(individual, edges_to_travel, path=None, properties=None, paths=None):
    if path is None:
        path = [individual]
    if properties is None:
        properties = []
    if paths is None:
        paths = []

    extended = False  # Flag to check if path is extended in this call

    # Check for further connections through the properties
    for prop in edges_to_travel:
        for related_individual in prop[individual]:
            if related_individual not in path:  # Avoid cycles
                find_chains(related_individual, edges_to_travel, path + [related_individual], properties + [prop], paths)
                extended = True

    # Add the chain to paths list if it is not extended further (i.e., at the end of a chain)
    if len(path) > 1 and not extended:
        chain = []
        for i, ind in enumerate(path):
            prop_label = properties[i] if i < len(properties) else None
            chain.append((ind, prop_label))
        paths.append(chain)

    return paths

def print_paths(paths):
    i=0
    for path in paths:
        path_str = ""
        for ind, prop in path:
            #print(ind, prop)
            if prop:
                path_str += f"{ind.label.first()} ({prop}) -> "
            else:
                path_str += f"{ind.label.first()} -> "
        path_str = path_str.rstrip(" -> ")
        i+=1
        print(i, path_str)

def get_path_str(path):
        path_str = ""
        for ind, prop in path:
            #print(ind, prop)
            if prop:
                path_str += f"{ind.label.first()} ({prop}) -> "
            else:
                path_str += f"{ind.label.first()} -> "
        path_str = path_str.rstrip(" -> ")
        return(path_str)

# Example usage
# paths = find_chains(i0)
# print(paths)
# print_paths(paths)
# paths[0][0][0].iri
# paths[0][0][0].is_a



def print_pathsClasses(paths):
    for path in paths:
        path_str = ""
        for ind, prop in path:
            #print(ind, prop)
            if prop:
                #path_str += f"{ind.is_a[0]} ({prop}) -> "
                path_str += f"{ind.is_a[0]} & {prop} "
            else:
                path_str += f"{ind.is_a[0]} -> "
        path_str = path_str.rstrip(" -> ")
        print(path_str)

def path2classes(paths):
    for path_index, path in enumerate(paths):
        new_path = []
        for ind, prop in path:
            class_of_ind = ind.is_a[0] if ind.is_a else None  # Replace with the first class, if available
            new_path.append((class_of_ind, prop))

        paths[path_index] = new_path  # Assign the modified path back

#print_pathsClasses(paths)


def format_path(path, index=0):
    if index >= len(path):
        return ""
    
    individual, prop_label = path[index]
    next_part = format_path(path, index + 1)
    
    if prop_label:
        if next_part:
            return f"obo.{individual.name} & obo.{prop_label.name}.some({next_part})"
        else:
            return f"obo.{individual.name} & obo.{prop_label.name}"
    else:
        return f"obo.{individual.name}"
#------------------

def format_path2(path, index=0):
    # Base case: if the path is empty or we've reached the end
    if not path or index >= len(path):
        return ""
    
    individual, prop_label = path[index]

    # If both individual and prop_label are None, return empty string
    if individual is None and prop_label is None:
        return ""
    
    # Recursive part for formatting the next part of the path
    next_part = format_path(path, index + 1)

    # Format the current part based on individual and prop_label presence
    if individual and prop_label:
        formatted_current = f"obo.{individual.name} & obo.{prop_label.name}"
    elif individual:
        formatted_current = f"obo.{individual.name}"
    elif prop_label:
        formatted_current = f"obo.{prop_label.name}"
    else:
        # This should not happen as we already checked for both being None
        return ""
    
    # Combining the current part with the next part
    if next_part:
        return f"{formatted_current}.some({next_part})"
    else:
        return formatted_current

# Example use-cases
# print(format_path([("metaventrite", None)]))
# print(format_path([(None, "has part"), ("punctate cuticle", "has part"), ("anterior region", "has part"), ("cuticular puncture", None)]))
# print(format_path([(None, None)]))  # Should return an empty string



#----------
def print_format_path(paths):
    for path in paths:
        formatted_path = format_path(path)
        print(formatted_path)


def get_unique_sublists(list_of_lists):
    unique_sublists_set = set(tuple(sublist) for sublist in list_of_lists)
    unique_sublists = [list(sublist) for sublist in unique_sublists_set]
    return unique_sublists

def get_unique_paths(entry_points, edges_to_travel):
    path_final = []
    for entry in entry_points:
        paths = find_chains(entry, edges_to_travel)
        path2classes(paths)
        path_final.extend(paths)
    # remove first
    for path in path_final:
        del path[0]
    # Filter out sublists with length more than 2
    path_final = [sublist for sublist in path_final if len(sublist) > 1]
    # select unique
    path_final = get_unique_sublists(path_final)
    #
    # Sort the filtered list by the first element of each sublist
    abc=[]
    for path in path_final:
        #print(path[0][0].label.first())
        abc.extend([path[0][0].label.first()])
    # Sort the words list and get the sorted order
    sorted_words = sorted(abc)
    # Create a mapping from word to its index in the sorted list
    index_mapping = {word: index for index, word in enumerate(sorted_words)}
    # Sort the path_final based on the order of the corresponding words in the sorted list
    path_final = sorted(path_final, key=lambda x: index_mapping[abc[path_final.index(x)]])
    #
    return path_final

def uuid_n(string_length=6):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    # random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


# path=paths[33]
# path=paths[36]
# print_paths(paths)
# make_path_manchester(paths[33])
# make_path_manchester(paths[36])
# ----------
def make_path_manchester(path):
    results = []
    i=1
    for i in range(0, len(path)):
        #print(i, path[i])
        # Splitting the list into two parts
        #to_left = [path[i]
        left = path[:i] + [(path[i][0], None)]
        #left[i][1] = None
        right = [(None, path[i][1])] + path[i+1:]
        #print(left, ':&:', right)

        # Reversing the left part
        left_reversed = left[::-1]
        #
        # shifting properties
        if len(left_reversed) > 1:
            left_reversed_shifted = []
            for i in range(0, len(left_reversed)-1):
                #print(i)
                new_t = (left_reversed[i][0], left_reversed[i+1][1])
                left_reversed_shifted += [new_t]
            # add last elemetn
            left_reversed_shifted += [(left_reversed[i+1][0], None)]
        else:
            left_reversed_shifted = left_reversed
        #
        # # Separating tuples with None as second element
        # none_tuples = [tup for tup in left_reversed if tup[1] is None]
        # #
        # # Filtering out tuples with None
        # other_tuples = [tup for tup in left_reversed if tup[1] is not None]
        # left_reversed_shifted = other_tuples + none_tuples
        # #
        # make props inverse in the left
        left_reversed_shifted  = [(x[0], x[1].inverse) if x[1] is not None else x for x in left_reversed_shifted]
        
        #results = format_path2(left_reversed_shifted) +' & ' + format_path2(right)
        #print(results)
        right_formatted = format_path2(right)
        if right_formatted:
            out = format_path2(left_reversed_shifted) + ' & ' + right_formatted
        else:
            out = format_path2(left_reversed_shifted)
        results.append(out)
    #
    #print(results)
    return results