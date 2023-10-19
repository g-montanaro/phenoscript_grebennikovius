from owlready2 import *


ontoFile='/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/output/grebennikovius.owl'
#--
def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
# set_render_func(render_using_iri)
# set_render_func()
set_log_level(9)
#-----------------------

#--- Read in Ontology
onto = get_ontology(ontoFile).load()
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")
pato= onto.get_namespace("http://purl.obolibrary.org/obo/pato#")

obo.BFO_0000050
obo.BFO_0000051

for i in onto.individuals():
    print(i, i.BFO_0000050)

for pair in obo.BFO_0000050.get_relations():
    print(pair)
    i1=pair[0]
    i2=pair[1]
    i2.BFO_0000051.append(i1)

for pair in obo.BFO_0000051.get_relations():
    print(pair)
    i1=pair[0]
    i2=pair[1]
    i2.BFO_0000050.append(i1)

onto.save(file = ontoFile, format = "rdfxml")
