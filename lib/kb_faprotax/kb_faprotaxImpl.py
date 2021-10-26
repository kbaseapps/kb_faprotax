# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import sys
import uuid
import subprocess
import functools
from dotmap import DotMap


from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace
from installed_clients.FunctionalProfileUtilClient import FunctionalProfileUtil
from installed_clients.GenericsAPIClient import GenericsAPI


from .impl.kbase_obj import AmpliconMatrix, AttributeMapping
from .util.debug import dprint
from .util.varstash import Var, reset_Var # `Var` holds globals, `reset` clears everything but config stuff
from .impl.workflow import do_AmpliconMatrix_workflow, do_GenomeSet_workflow
from .util.params import Params


#END_HEADER


class kb_faprotax:
    '''
    Module Name:
    kb_faprotax

    Module Description:
    A KBase module: kb_faprotax
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "1.0.0"
    GIT_URL = "https://github.com/kbaseapps/kb_faprotax"
    GIT_COMMIT_HASH = "51052ac7907f72c0d3c06313dcae52efb9a36056"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s', level=logging.INFO)

        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.workspace_url = config['workspace-url']
        self.config = config


        #END_CONSTRUCTOR
        pass


    def run_FAPROTAX(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_FAPROTAX
    
        logging.info(params)

        Var.update({ # carry over into globals `Var`, regardless of resetting, for all API-method runs
            'params': Params(params),
            'shared_folder': self.shared_folder,
            'kbase_endpoint': self.config['kbase-endpoint'], # contains environment, for constructing Genome landing page url
            #---
            'ws': Workspace(self.workspace_url),
            'dfu': DataFileUtil(self.callback_url), # instantiate here so within runtime of @patch
            'kbr': KBaseReport(self.callback_url), # instantiate here so within runtime of @patch 
            'gapi': GenericsAPI(self.callback_url),
            'fpu': FunctionalProfileUtil(self.callback_url, service_ver='beta'), # TODO overhead?
            #---
            'warnings': [],
            #---
            'run_dir': os.path.join(self.shared_folder, 'kbfptx_' + str(uuid.uuid4())),
        })
        
        os.mkdir(Var.run_dir)
        Var.update({
            'return_dir': os.path.join(Var.run_dir, 'return'),
        })
        os.mkdir(Var.return_dir)       


        #
        ##
        ### detect input type
        ####
        #####


        oi = Var.ws.get_object_info3({'objects': [{'ref': params['input_upa']}]})['infos'][0]

        if oi[2].startswith('KBaseSearch.GenomeSet'):
            output = do_GenomeSet_workflow()

        elif oi[2].startswith('KBaseMatrices.AmpliconMatrix'):
            output = do_AmpliconMatrix_workflow()

        else:
            raise Exception('Unknown type `%s` for `input_upa`' % oi[2])




        #END run_FAPROTAX

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_FAPROTAX return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
