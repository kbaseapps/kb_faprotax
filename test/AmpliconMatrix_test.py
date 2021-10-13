import unittest
from pytest import raises

from kb_faprotax.util.debug import dprint
from kb_faprotax.util.varstash import Var  # dict-like dot-access app globals
from kb_faprotax.impl.error import NoWsReferenceException
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
from config import patch_


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
