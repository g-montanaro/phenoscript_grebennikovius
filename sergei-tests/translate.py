
from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()

from phenospy import *
from owlready2 import *
import os

# Get the current directory
# current_dir = os.getcwd()
current_dir = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests'

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
file_md = os.path.join(current_dir, 'output', 'Greb.md')
ind0 = onto.search(label = taxon)[0]
NLgraphToMarkdown(onto, ind0, file_save = file_md, verbose =False)


#-----
onto.save(file = os.path.join(save_dir, 'Greb_temp.owl'), format = "rdfxml")

# manual

# -----------------------------------------
# Make NL Graph for Md rendering from OWL: high-level wrapper
# -----------------------------------------
def owlToNLgraph(owl_file):
    # -----------------------------------------
    # Arguments
    # -----------------------------------------
    # set_log_level(0)
    print(f"{Fore.BLUE}Reading OWL:{Style.RESET_ALL}", owl_file)
    onto = get_ontology(owl_file).load(reload_if_newer=True, reload=True)
    # -----------------------------------------
    # Namespaces
    # -----------------------------------------
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')
    import phenospy.nl_fun
    # -----------------------------------------
    # Make NL graph 
    # -----------------------------------------
    phenospy.nl_fun.makeNLGraph_basic(onto)
    return onto

# -----------------------------------------
# Make NL Graph for Md rendering
# -----------------------------------------
def makeNLGraph_basic(onto):
    global phenoscript_annotations, phs_implies_absence_of, phs_NL 
    global phs_original_assertion, phs_original_class
    # -----------------------------------------
    # Namespaces
    # -----------------------------------------
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')

    # -----------------------------------------
    # Add absence
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding absence traits...{Style.RESET_ALL}")

    for ind in onto.individuals():
        #print(ind)
        if (len(ind.phs_implies_absence_of)>0):
            # print(ind, "---", ind.phs_implies_absence_of)
            abs_class=ind.phs_implies_absence_of[0]
            txt=" [%s](%s): absent;" % (abs_class.label.first(), abs_class.iri)
            # print(txt)
            ind.phs_NL.append(txt)

    # -----------------------------------------
    # Pattern: add chracter prsence
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding presence traits...{Style.RESET_ALL}")
    phenospy.nl_fun.add_presentTag_ToNLinOWL(default_world)

    # -----------------------------------------
    # SPARQL:  Absolute and Relative Mesuarements
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding Absolute and Relative Mesuarements...{Style.RESET_ALL}")
    
    # check is meserument entities are present, othervise sparql does not work
    is_mesure_present = IRIS['http://purl.obolibrary.org/obo/IAO_0000417']
    if bool(is_mesure_present):
        query_tmpMesuare = phenospy.nl_fun.sparql_tmpMeasurements(default_world)
        dic_mesuare = phenospy.nl_fun.tmpMeasureToDic(query_tmpMesuare)
        # dic_mesuare obtained from sparql query to NL in OWL
        phenospy.nl_fun.dic_mesuare_ToNLinOWL(dic_mesuare)

    # -----------------------------------------
    # SPARQL:  Relative Comparison
    #   Pattern: Org1 > E1 >> Q1 |comp| Q2 << E2 < Org2
    # -----------------------------------------
    print(f"{Fore.BLUE}Adding Relative Comparison traits...{Style.RESET_ALL}")

    # Check existence and if existence render it to NL
    # increased in magnitude relative to
    compProp = obo.RO_0015007
    if bool(compProp):
        query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015007.iri)
        dic_RelatComp = tmpRelatToDic(query_RelatComp)
        dic_Relat_ToNLinOWL(dic_RelatComp)
    #
    # decreased in magnitude relative to
    compProp = obo.RO_0015008
    if bool(compProp):
        query_RelatComp = sparql_RelatComp(default_world, comparative_prop = obo.RO_0015008.iri)
        dic_RelatComp = tmpRelatToDic(query_RelatComp)
        dic_Relat_ToNLinOWL(dic_RelatComp)
    #
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")