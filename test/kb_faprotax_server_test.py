# -*- coding: utf-8 -*-
import os
import logging
import time
import unittest
import uuid
import pandas as pd

from configparser import ConfigParser
from kb_faprotax.kb_faprotaxImpl import kb_faprotax
from kb_faprotax.kb_faprotaxServer import MethodContext
from kb_faprotax.authclient import KBaseAuth as _KBaseAuth
from installed_clients.WorkspaceClient import Workspace

from kb_faprotax.util.error import *
from kb_faprotax.util.message import *
from kb_faprotax.util.dprint import dprint
from kb_faprotax.util.varstash import Var
from kb_faprotax.util.kbase_obj import AttributeMapping





_17770 = '48666/2/9'
first50 = "48402/9/2"
secret = '49926/6/1'
secret_wRDP = '49926/9/3'


params_debug = {
    'skip_obj': True,
    'skip_run': True,
    'skip_kbReport': True,
    'return_test_info': True,
    }


class kb_faprotaxTest(unittest.TestCase):

    def _test(self):
        ret = self.serviceImpl.faprotax(
            self.ctx, {
                **self.params_ws,
                'amplicon_set_upa': secret_wRDP,
                #**params_debug,
                }
            )
        return
   

    def _test_attribute_and_source_exists(self):
        pass
   

    def test_add_new_attribute(self): # TODO tie to source
        ret = self.serviceImpl.faprotax(
            self.ctx, {
                **self.params_ws,
                'amplicon_set_upa': secret_wRDP,
            })
        

    def _test_no_taxonomy_no_AttributeMapping(self):
        with self.assertRaises(NoTaxonomyException) as cm:
            ret = self.serviceImpl.faprotax(
                self.ctx, {
                    **self.params_ws,
                    'amplicon_set_upa': secret,
                })
            

    def _test_against_reference(self):
        ret = self.serviceImpl.faprotax(
            self.ctx, {
                **self.params_ws,
                'amplicon_set_upa': _17770,
                'return_test_info': True,
                }
            )

        logging.info('Comparing traits in AttributeMapping to answers')

        # load AttributeMapping
        row_attrmap = AttributeMapping(ret['objects_created'][0]['ref'])
        instances_d = row_attrmap.obj['instances']
        attribute_d_l = row_attrmap.obj['attributes']

        # find index in attribute list
        for i, attribute_d in enumerate(attribute_d_l):
            if attribute_d['attribute'] == 'FAPROTAX Traits':
                ind = i

        # id to attribute
        results_d = {id: attr_l[ind] for id, attr_l in instances_d.items()}

        # id to traits
        answers_d = self.parse_answers_file()

        html_l = []

        for id in answers_d:
            assert id in results_d

            res = results_d[id]
            ans = answers_d[id]

            if res != ans:
                res_l = res.split(':')
                ans_l = ans.split(':')
                assert set(ans_l).issubset(res_l)
                
                html = '<p>' + ':'.join([res if res in ans_l else '<b>' + res + '</b>' for res in res_l]) + '</p>'
                html_l.append(html)

        html_l = list(set(html_l))


        with open(f'/kb/module/work/tmp/diff.html', 'w') as fp: # TODO automate the left-off parent function detection so you don't have to look at this every time
            fp.write('\n'.join(html_l))

                  


    @staticmethod
    def parse_answers_file():
        answers_flpth = '/kb/module/test/data/OTUMetaData_reduced.tsv'
        answers_df = pd.read_csv(
            answers_flpth, sep='\t', header=0, index_col='#OTU ID', usecols=['#OTU ID', 'FAPROTAX Traits']).fillna('')
        answers_d = answers_df.to_dict(orient='index')
        answers_d = {key: value['FAPROTAX Traits'] for key, value in answers_d.items()}
        return answers_d



    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_faprotax'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_faprotax',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.wsName = 'kb_faprotax_' + str(uuid.uuid4())                                                 
        cls.wsId = cls.wsClient.create_workspace({'workspace': cls.wsName})[0]                      
        cls.params_ws = {                                                                           
            'workspace_id': cls.wsId,                                                               
            'workspace_name': cls.wsName,                                                           
            }                                                                                       
        dprint('cls.wsId', run=locals())  
        cls.serviceImpl = kb_faprotax(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')
        test_names = [key for key, value in cls.__dict__.items() if type(key) == str and key.startswith('test') and callable(value)]
        print('All tests:', test_names)
        dec = '!!!' * 200
        print(dec, "DON'T FORGET TO SEE DIFF", dec)
