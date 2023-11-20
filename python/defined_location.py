

import types
import sys
sys.path.append('/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/python')
from materialize_fun import *


fl = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/source_ontologies/aism-edit.owl'
onto = get_ontology(fl).load()

obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')


with phs_ns:
    class phs_Location(Thing): pass
    class phs_Defined_Location(phs_Location): pass
    class phs_UNDefined_Location(phs_Location): pass


tagmas=[obo.AISM_0000107, obo.AISM_0000108, obo.AISM_0000109, obo.AISM_0000031]


for tagma in tagmas:
    print(tagma)
    with phs_ns:
        newClass = types.new_class(str(uuid_n()), (phs_Defined_Location,))
        newClass .label= "Defined_Loc: " + tagma.label.first()
        newClass.equivalent_to.append(tagma)
        newClass.equivalent_to.append(obo.BFO_0000050.some(tagma))
        newClass.equivalent_to.append(obo.AISM_0000079.some(tagma))
        newClass.equivalent_to.append(obo.BFO_0000051.some(obo.BFO_0000050.some(tagma)))

# ------
fl_save = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/output/test.owl'
onto.save(file = fl_save, format = "rdfxml")











#------------------------------------------
#------------------------------------------

from owlready2 import *
import types
import warnings
#import pdb # pdb.set_trace()
exec(open("./src/reasoning/runELK.py").read())

#-----------------------
# Arguments
#-----------------------
ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/data"
#onto_path.append(ontoPath)
ontoFile="colao_merged.owl"

#--
def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
# set_render_func(render_using_iri)
# set_render_func()
set_log_level(9)
#-----------------------

# additional (default) Args
phs='{https://github.com/sergeitarasov/PhenoScript}'
ns = {'phs': 'https://github.com/sergeitarasov/PhenoScript'}


print('Reading data...\n')

#--- Read in Ontology
onto_path.append(ontoPath)
onto = get_ontology(ontoFile)
#onto= get_ontology("http://test.org/onto.owl#")
onto.load(reload_if_newer=True, reload=True)
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
#-------------------------------



inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")

# with obo:
#     class BFO_0000051(ObjectProperty): pass
#     class AISM_0000078(ObjectProperty): pass

#Has_partart_Encircles.property_chain.append(PropertyChain([obo.BFO_0000051, obo.AISM_0000078])) # this works
# http://purl.obolibrary.org/obo/RO_0002150 continuos_with
# http://purl.obolibrary.org/obo/RO_0002323 meterorologically_related_to
with inf:
    # class Has_part_Encircles(ObjectProperty): pass
    # class Encircles_Has_part(ObjectProperty): pass
    class Part_of_Encircled(TransitiveProperty): pass
    class Encircled_Part_of(TransitiveProperty): pass
    class phs_Reasoning(Thing): pass
    class phs_Defined_Location(phs_Reasoning): pass


# Has_part_Encircles.property_chain.append(PropertyChain([obo.BFO_0000051, obo.AISM_0000078]))
# Encircles_Has_part.property_chain.append(PropertyChain([obo.AISM_0000078, obo.BFO_0000051]))

Part_of_Encircled.property_chain.append(PropertyChain([obo.BFO_0000050, obo.RO_0002150]))
Encircled_Part_of.property_chain.append(PropertyChain([obo.RO_0002150, obo.BFO_0000050]))

topClass=obo.AISM_0000174
#obo.AISM_0000019, obo.AISM_0000107
tagmas=[obo.AISM_0000019, obo.AISM_0000108, obo.AISM_0000109, obo.AISM_0000031]


for tagma in tagmas:
    phs_Defined_Location.equivalent_to.append(tagma)
    phs_Defined_Location.equivalent_to.append(topClass & Part_of_Encircled.some(tagma))
    phs_Defined_Location.equivalent_to.append(topClass & Encircled_Part_of.some(tagma))
    phs_Defined_Location.equivalent_to.append(topClass & obo.BFO_0000050.some(tagma))
    phs_Defined_Location.equivalent_to.append(topClass & obo.AISM_0000079.some(tagma))
    phs_Defined_Location.equivalent_to.append(obo.BFO_0000051.some(obo.BFO_0000050.some(tagma)))
    phs_Defined_Location.equivalent_to.append(obo.BFO_0000051.some(Part_of_Encircled.some(tagma)))


# phs_Defined_Location.equivalent_to.append(topClass & Part_of_Encircled.some(obo.AISM_0000107))
# phs_Defined_Location.equivalent_to.append(topClass & Encircled_Part_of.some(obo.AISM_0000107))
# phs_Defined_Location.equivalent_to.append(topClass & obo.BFO_0000050.some(obo.AISM_0000107))
# phs_Defined_Location.equivalent_to.append(topClass & obo.AISM_0000079.some(obo.AISM_0000107))


#-----
onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/def_loc.owl', format = "rdfxml")
#onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/my_instance_phs_REASON2.owl', format = "rdfxml")

runELK(input='./output/def_loc.owl', output='./output/def_loc_ELK.owl', PATH_TO_ELK="/Applications/ELK/elk.jar")

#--------------
onto.destroy()
ontoPath="/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/"
ontoFile="def_loc_ELK.owl"
onto_path.append(ontoPath)
onto = get_ontology(ontoFile)
onto.load( reload=True)
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")

# list_1=["a", "b", "c", "d", "e"]
# list_2=["a", "f", "c", "m"]
# set(list_2) - set(list_1)

defList=set(inf.phs_Defined_Location.descendants())
allList=set(obo.AISM_0000174.descendants())

undefLocation=allList-defList

for i in undefLocation:
    print(i)

# create undfined location classes
with inf:
    class phs_unDefined_Location(inf.phs_Reasoning): pass

for i in undefLocation:
    i.is_a.append(phs_unDefined_Location)

#-----
onto.save(file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/output/def_loc_ELK.owl', format = "rdfxml")