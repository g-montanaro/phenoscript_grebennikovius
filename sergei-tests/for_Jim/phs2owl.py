
from phenospy import *
import os


# # versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

# Get the current directory
current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim'



# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'Grebennikovius_toy-example.phs')
yaml_file   = os.path.join(current_dir, 'phs-config.yaml')
save_dir    = os.path.join(current_dir, 'output/')
save_pref   = 'Greb_toy'

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
file_md = os.path.join(current_dir, 'output', 'Greb_toy.md')
ind0 = onto.search(label = taxon)[0]
xxx=NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =True)

xxx

import markdown

def save_html_to_file(html_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(html_content)

html = markdown.markdown(xxx)
output_html = os.path.join(current_dir, 'output', 'Greb_toy.html')
save_html_to_file(html, output_html)



