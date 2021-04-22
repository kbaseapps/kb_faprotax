import os
import time
import logging
import unittest
from unittest.mock import patch
from configparser import ConfigParser
import uuid
import pandas as pd
import numpy as np
import itertools
import shutil

from kb_faprotax.kb_faprotaxServer import MethodContext
from kb_faprotax.authclient import KBaseAuth as _KBaseAuth
from installed_clients.WorkspaceClient import Workspace

from kb_faprotax.kb_faprotaxImpl import kb_faprotax 


######################################
######################################
######### TOGGLE PATCH ###############
######################################
###################################### 
do_patch = True 

if do_patch:
    patch_ = patch
    patch_dict_ = patch.dict

else:
    patch_ = lambda *args, **kwargs: lambda f: f
    patch_dict_ = lambda *args, **kwargs: lambda f: f
######################################
######################################
######################################
######################################


'''
token = os.environ.get('KB_AUTH_TOKEN', None)
config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
cfg = {}
config = ConfigParser()
config.read(config_file)
for nameval in config.items('kb_faprotax'):
    cfg[nameval[0]] = nameval[1]
# Getting username from Auth profile for token
authServiceUrl = cfg['auth-service-url']
auth_client = _KBaseAuth(authServiceUrl)
user_id = auth_client.get_user(token)
# WARNING: don't call any logging methods on the context object,
# it'll result in a NoneType error
ctx = MethodContext(None)
ctx.update({'token': token,
            'user_id': user_id,
            'provenance': [
                {'service': 'kb_faprotax',
                 'method': 'please_never_use_it_in_production',
                 'method_params': []
                 }],
            'authenticated': 1})
wsURL = cfg['workspace-url']
wsClient = Workspace(wsURL)
shared_folder = cfg['scratch']
'''


####################################################################################################
####################################################################################################
class BaseTest(unittest.TestCase):


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
        cls.ws = {                                                                           
            'workspace_id': cls.wsId,                                                               
            'workspace_name': cls.wsName,                                                           
            }                                                                                       
        cls.serviceImpl = kb_faprotax(cls.cfg)
        cls.shared_folder = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']



    @classmethod
    def tearDownClass(cls):
        print('BaseTest tearDownClass')

        #
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace deleted')
        
    def shortDescription(self):
        '''Override unittest using test*() docstrings in lieu of test*() method name in output summary'''
        return None



