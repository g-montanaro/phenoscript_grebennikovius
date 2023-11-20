
# # versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

#phenospy owl2text -f 'html' -s 'org_*' -o grebennikovius.owl -d NL
#phenospy owl2text -f 'md' -s 'org_*' -o grebennikovius.owl -d NL
# -----------------------------------------
# OWL to Markdown
# -----------------------------------------
from phenospy import *
import markdown
import os

def save_to_file(file_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(file_content)

# get owl file
#owl_file = os.path.join(save_dir, save_pref + '.owl')
str_search = 'org_*'
owl_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/toy_example/output/grebennikovius.owl'
#file_save = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/toy_example/output/grebennikovius.md'
#file_save = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/toy_example/output/grebennikovius.html'
save_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/toy_example/output/NL'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Make NL graph
onto = owlToNLgraph(owl_file)

# Get species/entry points for rendering
entry_points = onto.search(label = str_search)

AR2='html'
for point in entry_points:
    #print(point)
    md = NLgraphToMarkdown(onto, point, verbose = True)
    #save_to_file(md, file_save)
    if AR2=='html':
        html = markdown.markdown(md)
        point_str = point.label.first()
        point_str = point_str.replace(" ", "_") + '.html'
        file_save = os.path.join(save_dir, point_str)
        save_to_file(html, file_save)


#----
# Convert NL graph to Markdown
taxon = 'org_Grebennikovius armiger'
ind0 = onto.search(label = taxon)[0]
md = NLgraphToMarkdown(onto, ind0, verbose = True)

#--------- To MD
save_to_file(md, file_save)

#--------- To HTML
html = markdown.markdown(md)
save_to_file(html, file_save)


