from configparser import ConfigParser
import os
import logging
import time
import unittest
import uuid
import pandas as pd
import numpy as np
from shutil import rmtree, copytree
import json
from unittest.mock import patch
import pandas as pd
from urllib.parse import urlparse
import re
from pytest import raises

from kb_faprotax.kb_faprotaxImpl import kb_faprotax
from kb_faprotax.kb_faprotaxServer import MethodContext
from kb_faprotax.authclient import KBaseAuth as _KBaseAuth
from installed_clients.WorkspaceClient import Workspace

from kb_faprotax.util.workflow import run_check
from kb_faprotax.util.error import * # exception library
from kb_faprotax.util.dprint import dprint, where_am_i
from kb_faprotax.util.varstash import Var # dict-like dot-access app globals
from kb_faprotax.util.kbase_obj import GenomeSet, Genome, AmpliconMatrix, AttributeMapping
from mock import * # mock business
from upa import * # upa library
import config


####################################################################################################
####################################################################################################
def test_parse_faprotax_functions():
    '''Test function used to parse FAPROTAX's predicted functions from its output'''
    from kb_faprotax.util.workflow import parse_faprotax_functions

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



