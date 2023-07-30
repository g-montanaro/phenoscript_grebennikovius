
from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()

from phenospy import *
from owlready2 import *
import os

# Get the current directory
# current_dir = os.getcwd()
#current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius'
current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius'

# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'grebennikovius_descriptions.phs')
yaml_file   = os.path.join(current_dir, 'sergei-tests', 'phs-config.yaml')
save_dir    = os.path.join(current_dir, 'output/')
save_pref   = 'Grebennikovius'

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
file_md = os.path.join(current_dir, 'output', 'Greb.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)


#-----
onto.save(file = os.path.join(save_dir, 'Greb_temp.owl'), format = "rdfxml")

# -----------------------------------------
# Add absence
# -----------------------------------------
print(f"{Fore.BLUE}Adding absence traits...{Style.RESET_ALL}")

for ind in onto.individuals():
    #print(ind)
    if (len(ind.phs_implies_absence_of)>0):
        print(len(ind.phs_implies_absence_of))
        print(ind, "---", ind.phs_implies_absence_of)
        for index in range(0, len(ind.phs_implies_absence_of)):
            abs_class=ind.phs_implies_absence_of[index]
            print('\t', abs_class)
            txt=", [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
            ind.phs_NL.append(txt)
#---
        abs_class=ind.phs_implies_absence_of[0]
        print('\t', abs_class)
        txt=" [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
        # print(txt)
        ind.phs_NL.append(txt)



obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
dwc = onto.get_namespace("http://rs.tdwg.org/dwc/terms/")
ind0 = onto.search(label = taxon)[0]
# http://rs.tdwg.org/dwc/terms/catalogNumber
x=ind0.catalogNumber[0]
type(ind0.catalogNumber[0])
" %s;" % x

xx=onto.search(label = 'Catalog Number')[0]
xx.iri