import os

from kb_faprotax.util.debug import dprint
from kb_faprotax.impl.workflow import parse_faprotax_functions
from mock import TEST_DATA_DIR


####################################################################################################
####################################################################################################
def test_parse_faprotax_functions():
    '''Test function used to parse FAPROTAX's predicted functions from its output'''

    flnm = 'groups2records_dense.tsv'
    flpth = os.path.join(TEST_DATA_DIR, 'return/refseq/return/FAPROTAX_output', flnm)

    r2g_d = parse_faprotax_functions(flpth)

    taxonomy = '\
cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Pseudomonadales; Moraxellaceae; \
Acinetobacter; Acinetobacter calcoaceticus/baumannii complex; Acinetobacter pittii'
    functions = '\
aerobic_chemoheterotrophy,human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_nosocomia,\
human_pathogens_all,animal_parasites_or_symbionts,aromatic_compound_degradation,chemoheterotrophy'

    assert r2g_d[taxonomy] == functions
