from owlready2 import *

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
set_log_level(9)



file_out = "/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/source_queries/query.owl"
onto = get_ontology("http://purl.obolibrary.org/obo/aism.owl").load()


#-----
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
my_onto = onto.get_namespace("http://query_example/")



#  'head capsule' or ('part of' some 'head capsule')

with my_onto:
    class Classes_for_queries(Thing): pass
    class part_of_Head(Classes_for_queries):pass
    class part_of_Thorax(Classes_for_queries):pass
    class part_of_Abdomen(Classes_for_queries):pass
    class part_of_Leg(Classes_for_queries):pass

part_of_Head.equivalent_to.append(obo.AISM_0000107 | (obo.BFO_0000050.some(obo.AISM_0000107)))
part_of_Thorax.equivalent_to.append(obo.AISM_0000108 | (obo.BFO_0000050.some(obo.AISM_0000108)))
part_of_Abdomen.equivalent_to.append(obo.AISM_0000109 | (obo.BFO_0000050.some(obo.AISM_0000109)))
part_of_Leg.equivalent_to.append(obo.AISM_0000031 | (obo.BFO_0000050.some(obo.AISM_0000031)))


onto.save(file=file_out, format="rdfxml")
