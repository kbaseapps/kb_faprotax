# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace
from installed_clients.FunctionalProfileUtilClient import FunctionalProfileUtil
from installed_clients.GenericsAPIClient import GenericsAPI


from .util.varstash import Var, reset_Var  # `Var` holds globals
from .impl.workflow import do_AmpliconMatrix_workflow, do_GenomeSet_workflow
from .util.params import AmpliconWorkflowParams, GenomeWorkflowParams


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
    GIT_COMMIT_HASH = "7ff7570ddfa6f035176f6d11cd8c731859221662"

    #BEGIN_CLASS_HEADER

    def init_Var(self, params, params_cls):
        Var.update({ # carry over into globals `Var`, regardless of resetting, for all API-method runs
            'params': params_cls(params),
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

    def run_amplicon_workflow(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_amplicon_workflow

        logging.info(params)

        self.init_Var(params, AmpliconWorkflowParams)
        output = do_AmpliconMatrix_workflow()

        #END run_amplicon_workflow

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_amplicon_workflow return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def run_genome_workflow(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_genome_workflow

        logging.info(params)

        self.init_Var(params, GenomeWorkflowParams)
        output = do_GenomeSet_workflow()

        #END run_genome_workflow

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_genome_workflow return value ' +
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
