# def make_phsOnto(onto):
with onto:
    class phenoscript_annotations(AnnotationProperty): pass
    class phs_implies_absence_of(phenoscript_annotations): pass
    class phs_NL(phenoscript_annotations): pass
    class phs_original_assertion(phenoscript_annotations): pass
    class phs_original_class(phenoscript_annotations): pass
    class phs_DATA_block(Thing): pass
    class phs_TRAITS_block(Thing): pass
    class phs_OTU_block(Thing): pass

phenoscript_annotations.iri     = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000001'
phs_implies_absence_of.iri      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000003'
phs_NL.iri                      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000004'
phs_original_assertion.iri      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000005'
phs_original_class.iri          = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000002'
phs_DATA_block.iri              = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000020'
phs_TRAITS_block.iri            = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000021'
phs_OTU_block.iri               = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000022'

phenoscript_annotations.label    = 'phenoscript_annotations'
phs_implies_absence_of.label     = 'phs_implies_absence_of'
phs_NL.label                     = 'phs_NL'
phs_original_assertion.label     = 'phs_original_assertion'
phs_original_class.label         = 'phs_original_class'
phs_DATA_block.label             = 'DATA Block'
phs_TRAITS_block.label           = 'TRAITS Block'
phs_OTU_block.label              = 'OTU Block'