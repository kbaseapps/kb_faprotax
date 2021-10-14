import unittest
import os
import pandas as pd
from pytest import raises

from kb_faprotax.util.debug import dprint
from kb_faprotax.util.varstash import Var  # dict-like dot-access app globals
from kb_faprotax.impl.error import NoWsReferenceException
from kb_faprotax.impl.kbase_obj import AmpliconMatrix, AttributeMapping
from mock import (
    mock_dfu,
    mock_fpu,
    mock_gapi,
    mock_kbr,
    get_mock_run_check,
)
from upa import (
    enigma50by30,
    enigma50by30_noAttrMaps,
    enigma50by30_RDPClsf,
    enigma17770by511,
)
import config as cfg
from config import DO_PATCH, patch_


class TestCase(cfg.BaseTest):

    # TODO test: missing, rel abund vs raw abund, no tax, attributes at end (spot)

    @patch_('kb_faprotax.kb_faprotaxImpl.DataFileUtil', new=lambda *a: mock_dfu)
    @patch_('kb_faprotax.impl.workflow.run_check', new=get_mock_run_check('enigma50by30_RDPClsf'))
    @patch_('kb_faprotax.kb_faprotaxImpl.GenericsAPI', new=lambda *a, **k: mock_gapi)
    @patch_('kb_faprotax.kb_faprotaxImpl.FunctionalProfileUtil', new=lambda *a, **k: mock_fpu)
    @patch_('kb_faprotax.kb_faprotaxImpl.KBaseReport', new=lambda *a, **k: mock_kbr)
    def test_tax_field(self):
        ret = self.serviceImpl.run_FAPROTAX(
            self.ctx,
            {
                **self.ws,
                'input_upa': enigma50by30_RDPClsf,
                'tax_field': 'RDP Classifier taxonomy, conf=0.777, gene=silva_138_ssu, minWords=default',
                'output_amplicon_matrix_name': 'a_name',
            }
        )

        assert len(Var.params_report.objects_created) == 4
        _check_faprotax_output(Var.out_dir)
        if not DO_PATCH:
            _check_attr_map_populated(
                Var.objects_created[1]['ref'],
                Var.objects_created[0]['ref'],
                'FAPROTAX Functions (taxonomy=<RDP Classifier taxonomy, conf=0.777, gene=silva_138_ssu, minWords=default>)'
            )

    @patch_('kb_faprotax.kb_faprotaxImpl.DataFileUtil', new=lambda *a: mock_dfu)
    @patch_('kb_faprotax.impl.workflow.run_check', new=get_mock_run_check('enigma50by30'))
    @patch_('kb_faprotax.kb_faprotaxImpl.GenericsAPI', new=lambda *a, **k: mock_gapi)
    @patch_('kb_faprotax.kb_faprotaxImpl.FunctionalProfileUtil', new=lambda *a, **k: mock_fpu)
    @patch_('kb_faprotax.kb_faprotaxImpl.KBaseReport', new=lambda *a, **k: mock_kbr)
    def test(self):
        ret = self.serviceImpl.run_FAPROTAX(
            self.ctx,
            {
                **self.ws,
                'input_upa': enigma50by30,
                'tax_field': 'taxonomy',
                'output_amplicon_matrix_name': 'a_name',
            }
        )

        assert len(Var.params_report.objects_created) == 4
        _check_faprotax_output(Var.out_dir)
        if not DO_PATCH:
            _check_attr_map_populated(
                Var.objects_created[1]['ref'],
                Var.objects_created[0]['ref'],
                'FAPROTAX Functions (taxonomy=<taxonomy>)'
            )

    @unittest.skip('long, private data')
    @patch_('kb_faprotax.kb_faprotaxImpl.DataFileUtil', new=lambda *a: mock_dfu)
    @patch_('kb_faprotax.impl.workflow.run_check', new=get_mock_run_check('enigma17770by511'))  #
    @patch_('kb_faprotax.kb_faprotaxImpl.GenericsAPI', new=lambda *a, **k: mock_gapi())
    @patch_('kb_faprotax.kb_faprotaxImpl.FunctionalProfileUtil', new=lambda *a, **k: mock_fpu)
    @patch_('kb_faprotax.kb_faprotaxImpl.KBaseReport', new=lambda *a, **k: mock_kbr)
    def test_against_reference(self):  # TODO
        ret = self.serviceImpl.run_FAPROTAX(
            self.ctx,
            {
                **self.ws,
                'input_upa': enigma17770by511,
                'tax_field': 'taxonomy',
                'output_amplicon_matrix_name': 'a_name',
            }
        )

        assert len(Var.params_report.objects_created) == 4
        _check_faprotax_output(Var.out_dir)
        if not DO_PATCH:
            _check_attr_map_populated(
                Var.objects_created[1]['ref'],
                Var.objects_created[0]['ref'],
                'FAPROTAX Functions (taxonomy=<taxonomy>)'
            )

    @patch_('kb_faprotax.kb_faprotaxImpl.DataFileUtil', new=lambda *a: mock_dfu)
    def test_noRowAttributeMapping(self):
        with raises(NoWsReferenceException):
            ret = self.serviceImpl.run_FAPROTAX(
                self.ctx,
                {
                    **self.ws,
                    'input_upa': enigma50by30_noAttrMaps,
                }
            )


def _check_faprotax_output(out_dir):
    """
    Check output of faprotax still in expected format
    """
    fp = os.path.join(out_dir, Var.COLLAPSED_FUNC_TABLE_FN)
    df = pd.read_csv(fp, sep='\t', index_col=0, header=0)
    assert df.index.name == 'group'
    assert df.shape[0] > 0
    assert df.shape[1] > 0

    fp = os.path.join(out_dir, Var.GROUPS2RECORDS_TABLE_DENSE_FN)
    df = pd.read_csv(fp, sep='\t', comment='#', index_col=0, header=0)
    assert df.index.name == 'record'
    assert df.shape[0] > 0
    assert df.shape[1] == 1

    fp = os.path.join(out_dir, Var.GROUPS2RECORDS_TABLE_FN)
    df = pd.read_csv(fp, sep='\t', comment='#', index_col=0, header=0)
    assert df.index.name == 'record'
    assert df.shape[0] > 0
    assert df.shape[1] > 0

def _check_attr_map_populated(amp_mat_upa, attr_map_upa, attr):
    amp_mat = AmpliconMatrix(amp_mat_upa)
    attr_map = AttributeMapping(attr_map_upa, amp_mat)
    i = attr_map.get_attr_ind(attr)
    attr_l = attr_map.get_attributes_at(i)
    attr_l = [x for x in attr_l if x != '']
    assert len(attr_l) > 0
