# -*- coding: utf-8 -*-

from phenospy import *
import os

# Get the current directory
current_dir = os.getcwd()

# -----------------------------------------
# ARGUMENTS
# -----------------------------------------
phs_file    = os.path.join(current_dir, 'grebennikovius_descriptions.phs')
yaml_file   = os.path.join(current_dir, 'phs-config.yaml')
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
taxon = 'Grebennikovius armiger'
file_md = os.path.join(current_dir, 'md', 'Grebennikovius.md')
ind0 = onto.search(label = taxon)[0]
# ind0='iri.....'
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)
