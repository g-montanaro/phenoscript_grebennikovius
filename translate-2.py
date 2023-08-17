
from phenospy import *
import os

# # versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

# Get the current directory
current_dir = os.getcwd()
#current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests'


# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'grebennikovius_descriptions.phs')
yaml_file   = os.path.join(current_dir, 'phs-config.yaml')
save_dir    = os.path.join(current_dir, 'output/')
save_pref   = 'Greb_2'

# -----------------------------------------
# Convert PHS to OWL and XML
# -----------------------------------------
phsToOWL(phs_file, yaml_file, save_dir, save_pref)

# -----------------------------------------
# OWL to Markdown
# -----------------------------------------
# get owl file
owl_file = os.path.join(save_dir, save_pref + '.owl')

# Make NL graph
onto = owlToNLgraph(owl_file)

# Convert NL graph to Markdown
taxon = 'org_Grebennikovius armiger'
file_md = os.path.join(current_dir, 'output', 'Greb8.md')
ind0 = onto.search(label = taxon)[0]
xxx=NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =True)

xxx

import markdown
from IPython.display import display, HTML

def save_html_to_file(html_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(html_content)

def save_displayed_html_to_file(output_html, output_file):
    # Get the HTML content from the IPython HTML object
    html_content = output_html.data

    # Save the HTML to a file
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(html_content)

html = markdown.markdown(xxx)
output_html = os.path.join(current_dir, 'output', 'Greb8.html')
save_html_to_file(html, output_html)

displayed_html = HTML(output_html)
save_displayed_html_to_file(displayed_html, output_html)




# -----------------------

def substitute_unwanted_combinations(string):
    modified_string = string.replace(" ,", ",")
    modified_string = modified_string.replace(" :", ":")
    return modified_string


import re

huge_string=xxx
def find_and_move_lines(huge_string):
    # pattern = r'\)\s\['
    pattern = '^- [^\]]+\]\([^\)]+\) [^\]]+\]\([^\)]+\)'
    #lines = huge_string.split('\n')
    lines=re.split(r'\n(?!\t)', huge_string)
    matched_lines = []

    for line in lines:
        if re.search(pattern, line):
            matched_lines.append(line)

    modified_string = '\n'.join(matched_lines) + '\n' + '---\n' + '\n'.join(line for line in lines if line not in matched_lines)

    return modified_string

# Example usage:
huge_string = """Some text - [xxx](xxxx) [xxx](xxxx)<some other text>
Another line - [yyy](yyyy) [zzz](zzzz) - [aaa](aaaa) [bbb](bbbb)
Some more text - [ccc](cccc) [ddd](dddd)<some other text>
"""
modified_string = find_and_move_lines(huge_string)
print(modified_string)

xxx=substitute_unwanted_combinations(xxx)
print(xxx)
modified_string = find_and_move_lines(xxx)
print(modified_string)