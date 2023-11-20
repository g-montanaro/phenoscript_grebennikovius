
import types
import sys
sys.path.append('/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/python')
from materialize_fun import *


fl = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/output/grebennikovius.owl'
onto = get_ontology(fl).load()

obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')



# Define the properties (assuming they are ObjectProperties in your ontology)
has_part = onto.search(iri="*BFO_0000051")[0]
part_of = onto.search(iri="*BFO_0000050")[0]
has_part.inverse = part_of
edges_to_travel = [has_part, part_of]


#---- Enrish has part / part of

# enrich has_part/part of
for N1 in onto.individuals():
    #print(ind)
    #print(has_part[ind])
    for N2 in part_of[N1]:
        #print(N1, '->', N2)
        if N1 not in  has_part[N2]:
            #print(N2, part_of[N2])
            if owl.FunctionalProperty in has_part.is_a:
                exec('N2.%s = N1' % has_part.name)
            else:
                exec('N2.%s.append(N1)' % has_part.name)

for prop in has_part.get_relations():
    #print(prop)
    N1 = prop[0]
    N2 = prop[1]
    exec('N2.%s.append(N1)' % part_of.name)

#--------

entry_points = onto.search(label='org_*')
paths = get_unique_paths(entry_points, edges_to_travel)
print_paths(paths)
print_format_path(paths)

# Create classes
with phs_ns:
    #get_path_str(path)
    MyClass = types.new_class(str(uuid_n()), (owl.Thing,))
    MyClass .label= "My CLASS"

for path in paths:
    #print_paths([path])
    with phs_ns:
        #get_path_str(path)
        newClass = types.new_class(str(uuid_n()), (MyClass,))
        newClass.label= "DEF: " + get_path_str(path)
        manchester=make_path_manchester(path)
        for item in manchester:
            #print(item)
            exec('newClass.equivalent_to.append(%s)' % item)


# ------
onto.save(file = fl, format = "rdfxml")


# ------ Manual Creation

with phs_ns:
    newClass = types.new_class(str(uuid_n()), (owl.Thing,))
    newClass.label= "DEF class 1"

# aism-mid_leg > aism-mesotibia > bspo-proximal_region;
s1 = obo.AISM_0000035 & obo.BFO_0000051.some( obo.AISM_0000068 & obo.BFO_0000051.some(obo.BSPO_0000077)   )
s2 = obo.AISM_0000068 & obo.BFO_0000050.some( obo.AISM_0000035) & (obo.BFO_0000051.some(obo.BSPO_0000077) )
s3 = obo.BSPO_0000077 & obo.BFO_0000050.some( obo.AISM_0000068 &  (obo.BFO_0000050.some(obo.AISM_0000035)) )

newClass.equivalent_to.append(s1)
newClass.equivalent_to.append(s2)
newClass.equivalent_to.append(s3)



# Example usage

# robot reason --reasoner whelk \
#   --annotate-inferred-axioms true \
#   --equivalent-classes-allowed all \
#   --axiom-generators "SubClass EquivalentClass" \
#   --input output/grebennikovius_merged.owl \
#   --output output/grebennikovius_merged_reasoned.owl

#   robot reason --reasoner whelk \
#   --create-new-ontology true \
#   --input output/grebennikovius_merged.owl \
#   --output output/grebennikovius_axioms.owl

