from owlready2 import *

from phenospy import *
import os


# # versions
import pkg_resources
version = pkg_resources.get_distribution("phenospy").version
print(version)

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

def sparql_RelatComp(default_world, comparative_prop):
    # phs_ns.PHS_0000017.iri # has_trait
    # obo.RO_0015007 # increased in magnitude relative to
    # obo.RO_0015008 # deacreased in ...
    # obo.RO_0000053 # bearer of
    has_trait_iri = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000017'
    # !!! ?prop is used on purpose to have acess to the object indownstream scripts
    query = list(default_world.sparql("""
            SELECT DISTINCT ?Q1 ?Org1 ?Q2 ?E2 ?Org2 ?prop
            WHERE {
                ?Q1 a owl:NamedIndividual .
                ?Q2 a owl:NamedIndividual .
                ?Q1  <%s> ?Q2 .
                ?Q1  ?prop ?Q2 .
                ?E2 obo:RO_0000053 ?Q2 .
                ?Org1 <%s> ?Q1 .
                ?Org2 <%s> ?Q2 .
            }
    """ % (comparative_prop, has_trait_iri, has_trait_iri)))
    #print(query)
    return query

def tmpRelatToDic(query):
    # [{'Q1': length:_1e96f5_13-5, 'Org1': org_Grebennikovius_basilewskyi, 
    #   'Q2': length:id-185304, 'E2': leg:_1e96f5_18-3, 'Org2': org_Grebennikovius}]
    dic_RelatComp=[]
    for item in query:
        # print(item)
        dict_templ = {"Q1": None, "Org1": None, "Q2": None, "E2": None, "Org2": None, "CompProp": None}
        dict_templ['Q1']= item[0]
        dict_templ['Org1'] = item[1]
        dict_templ['Q2'] = item[2]
        dict_templ['E2'] = item[3]
        dict_templ['Org2'] = item[4]
        dict_templ['CompProp'] = item[5]
        dic_RelatComp.append(dict_templ)
    return dic_RelatComp

def dic_Relat_ToNLinOWL(dic_RelatComp):
    # We need to:
    # 1. delete inherence_in prop if Q2 inherence in E2 delete inherence_in
    # 2. construct the relative comparison phs_NL only is spp are different
    # --
    # txt: Q2 of E2 in Org2
    # item = dic_RelatComp[0]
    # renderNL(item['CompProp'], onto)
    item=dic_RelatComp[0]
    for item in dic_RelatComp:
        print(item)
        if (item['Org1'].iri != item['Org2'].iri):
            # txt = " %s of %s in _%s_" % \
            # ( nodeToNL(item['Q2']), nodeToNL(item['E2']), item['Org2'].label.first() )
            txt = " of %s in _%s_;" % \
            (nodeToNL(item['E2']), item['Org2'].label.first())
            print(txt)
            # substitute Q1 with fake ind that is not connected to Q2
            make_fakeInd(q1=item['Q1'], q2=item['Q2'], 
            CompProp =item['CompProp'], txt=txt)


def nodeToNL(ind):
    if ind is not None:
        return "[%s](%s)" % (ind.phs_original_class[0].label.first(), ind.phs_original_class[0].iri)

def make_fakeInd(q1, q2, CompProp, txt):
    # remove annotation
    phs_original_assertion[q1, CompProp, q2] = []
    # remove CompProp link q1.CompProp
    CompProp[q1] = []
    # make fake individual
    CL = q1.is_a.first()
    fake_ind = CL('https://temp/tmp/')
    fake_ind.iri = 'https://temp/tmp/' + q1.label.first() + '/fake_ind'
    fake_ind.phs_original_class.append(CL)
    fake_ind.phs_NL.append(txt)
    # make a link between q1 and fake_ind
    CompProp[q1] = [fake_ind]
    phs_original_assertion[q1, CompProp, fake_ind] = True

compProp = obo.RO_0015007
if bool(compProp):
    query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015007.iri)
    #
    dic_RelatComp = tmpRelatToDic(query_RelatComp)
    dic_Relat_ToNLinOWL(dic_RelatComp)


# decreased in magnitude relative to
compProp = obo.RO_0015008
if bool(compProp):
    query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015008.iri)
    dic_RelatComp = tmpRelatToDic(query_RelatComp)
    dic_Relat_ToNLinOWL(dic_RelatComp)



# -----------------------------------------
# OWL to Markdown
# -----------------------------------------
# get owl file
owl_file = os.path.join(ontoFile)

# Make NL graph
onto = owlToNLgraph(owl_file)

ontoFile2='/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/main/output/grebennikovius2.owl'
onto.save(file = ontoFile2, format = "rdfxml")


# Convert NL graph to Markdown
taxon = 'Helictopleurus sicardi'
file_md = os.path.join(current_dir, 'md', 'H_sicardi.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)