from unittest.mock import patch, create_autospec, Mock
import os
from shutil import rmtree, copytree
import logging
import json
from pathlib import Path

from installed_clients.WorkspaceClient import Workspace
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenericsAPIClient import GenericsAPI
from installed_clients.FunctionalProfileUtilClient import FunctionalProfileUtil
from installed_clients.KBaseReportClient import KBaseReport

from kb_faprotax.util.dprint import dprint
from kb_faprotax.util.varstash import Var
from kb_faprotax.util.workflow import run_check
from upa import *


TEST_DATA_DIR = '/kb/module/test/data'
GET_OBJECTS_DIR = TEST_DATA_DIR + '/get_objects'
FETCH_SEQUENCE_DIR = TEST_DATA_DIR + '/fetch_sequence'
WORK_DIR = '/kb/module/work/tmp'
CACHE_DIR = WORK_DIR + '/cache_test_data'

## MOCK FPU ##

def mock_import_func_profile(params):
    logging.info('Mocking `fpu.import_func_profile(%s)`' % str(params))

    return dict(
        func_profile_ref='func/profile/ref'
    )

def get_mock_fpu(dataset=None):
    mock_fpu = create_autospec(FunctionalProfileUtil, instance=True)
    mock_fpu.import_func_profile.side_effect = mock_import_func_profile

    return mock_fpu

mock_fpu = get_mock_fpu()


## MOCK GAPI ##

def mock_gapi_fetch_sequence(params):
    logging.info('Mocking `gapi.fetch_sequence(%s)`' % str(params))

    upa = ref_leaf(params)
    fp = _glob_upa(FETCH_SEQUENCE_DIR, upa)
    
    # Download and cache
    if fp is None:
        logging.info('Calling in cache mode `gapi.fetch_sequence(%s)`' % str(params))

        gapi = GenericsAPI(os.environ['SDK_CALLBACK_URL'], service_ver='dev')
        fp_work = gapi.fetch_sequence(params)
        fp_cache = os.path.join(
            mkcache(FETCH_SEQUENCE_DIR),
            file_safe_ref(upa) + '.fa'
        )
        shutil.copyfile(
            fp_work,
            fp_cache
        )
        return fp_work

    # Pull from cache
    else:
        return fp


def get_mock_gapi():
    mock_gapi = create_autospec(GenericsAPI, instance=True)
    mock_gapi.fetch_sequence.side_effect = mock_gapi_fetch_sequence
    return mock_gapi

mock_gapi = get_mock_gapi()
        


## MOCK DFU ##

def mock_dfu_save_objects(params):
    logging.info('Mocking dfu.save_objects(%s)' % str(params)[:200] + '...' if len(str(params)) > 200 else params)

    return [['mock', 1, 2, 3, 'dfu', 5, 'save_objects']] # UPA made from pos 6/0/4

def mock_dfu_get_objects(params):
    logging.info('Mocking `dfu.get_objects(%s)`' % params)

    upa = ref_leaf(params['object_refs'][0])
    fp = _glob_upa(GET_OBJECTS_DIR, upa)

    # Download and cache
    if fp is None:
        logging.info('Calling in cache mode `dfu.get_objects`')

        dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        obj = dfu.get_objects(params)
        fp = os.path.join(
            mkcache(GET_OBJECTS_DIR),
            file_safe_ref(upa) + TRANSFORM_NAME_SEP + obj['data'][0]['info'][1] + '.json'
        )
        with open(fp, 'w') as fh: json.dump(obj, fh)
        return obj

    # Pull from cache
    else:
        with open(fp) as fh:
            obj = json.load(fh)
        return obj


def get_mock_dfu():
    mock_dfu = create_autospec(DataFileUtil, instance=True, spec_set=True)
    mock_dfu.save_objects.side_effect = mock_dfu_save_objects
    mock_dfu.get_objects.side_effect = mock_dfu_get_objects
    return mock_dfu

mock_dfu = get_mock_dfu()


## MOCK RUN_CHECK ##

def get_mock_run_check(dataset):
    # reset
    mock_run_check = create_autospec(run_check)

    # side effect
    def mock_run_check_(cmd):
        logging.info('Mocking running cmd `%s`' % cmd)
       
        rmtree(Var.return_dir)
        copytree(os.path.join(TEST_DATA_DIR, 'return', dataset, 'return'), Var.return_dir)

    mock_run_check.side_effect = mock_run_check_

    return mock_run_check

## MOCK KBR ##

def mock_create_extended_report(params):
    logging.info('Mocking `kbr.create_extended_report`')

    return {
        'name': 'kbr_mock_name',
        'ref': 'kbr/mock/ref',
    }

mock_kbr = create_autospec(KBaseReport, instance=True, spec_set=True) 
mock_kbr.create_extended_report.side_effect = mock_create_extended_report


## UTIL ##

def mkcache(dir):
    dir = dir.replace(TEST_DATA_DIR, CACHE_DIR)
    os.makedirs(dir, exist_ok=True)
    return dir

def _glob_upa(data_dir, upa):
    p_l = list(Path(data_dir).glob(file_safe_ref(upa) + '*'))
    if len(p_l) == 0:
        return None
    elif len(p_l) > 1:
        raise Exception(upa)

    src_p = str(p_l[0])

    return src_p

def ref_leaf(ref):
    return ref.split(';')[-1]

def file_safe_ref(ref):
    return ref.replace('/', '.').replace(';', '_')

TRANSFORM_NAME_SEP = '_'

