
from phenospy import *
import os


# # versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

# Get the current directory
current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim'

#------
cd /Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim
phenospy phs2owl 'Grebennikovius_toy-example.phs' 'out/greb'

# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'Grebennikovius_toy-example.phs')
yaml_file   = os.path.join(current_dir, 'phs-config.yaml')
save_dir    = os.path.join(current_dir, 'output/')
#save_pref   = 'Greb_toy'
save_pref   = 'Greb_toy_updated'

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
file_md = os.path.join(current_dir, 'output', 'Greb_toy_updated.md')
ind0 = onto.search(label = taxon)[0]
xxx=NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =True)

xxx



#--------- To HTML

import markdown

def save_html_to_file(html_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(html_content)

html = markdown.markdown(xxx)
output_html = os.path.join(current_dir, 'output', 'Greb_toy_updated.html')
save_html_to_file(html, output_html)




#----------- Download Ontologies

import os
import requests
import yaml

# Load the configuration from phs-config.yaml
# Update with the path to your phs-config.yaml file
config_path = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim/phs-config.yaml'  
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

# Create a directory to store downloaded ontologies
ontology_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim/ontologies'
os.makedirs(ontology_dir, exist_ok=True)

# Iterate over the ontologies and download them
for ontology_url in config['importOntologies']:
    # Get the filename from the URL
    filename = os.path.basename(ontology_url)
    file_path = os.path.join(ontology_dir, filename)

    # Download the ontology
    response = requests.get(ontology_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as ontology_file:
            ontology_file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename} (Status Code: {response.status_code})")

print("All ontologies downloaded.")

#-----
#robot merge --input out/greb.owl --inputs "ontologies/*.owl" --output results/merged.owl

# merge ontologies
robot merge --inputs "ontologies/*.owl" --output ontologies/merged.owl

robot merge --inputs "source_ontologies/*.owl" --output merged_ontologies/merged.owl

# remove individuals
robot remove --input ontologies/merged1.owl --select individuals --output ontologies/merged2.owl


# reason
robot reason --reasoner ELK \
  --input ontologies/merged.owl 

robot reason --reasoner whelk \
  --input ontologies/merged.owl 

robot reason --reasoner ELK --input merged_ontologies/merged_clean.owl > merged_ontologies/ELK_merged_clean.log

robot reason --reasoner whelk --input merged_ontologies/merged_clean.owl

robot reason --reasoner whelk --input output/grebennikovius_merged.owl



robot explain --input output/grebennikovius_merged.owl --reasoner ELK \
  -M unsatisfiability --unsatisfiable all --explanation explain/explanation.md


robot explain --input output/grebennikovius_merged.owl --reasoner ELK -M inconsistency --explanation explanation.md