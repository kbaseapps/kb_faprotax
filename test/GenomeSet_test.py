import config
from upa import *


class Test(config.BaseTest):

    def test_GenomeSet_input(self):
        ret = self.serviceImpl.run_FAPROTAX(
            self.ctx, 
            {
                **self.ws,
                'input_upa': A_prok_genomes,
            }
        )

    def test_dup_GenomeSet(self):
        ret = self.serviceImpl.run_FAPROTAX(
            self.ctx, 
            {
                **self.ws,
                'input_upa': A_prok_genomes_dup,
            }
        )


    @classmethod
    def tearDownClass(cls):
        super(cls, cls).tearDownClass()

        dec = '!!!' * 220
        print(dec, "DON'T FORGET TO SEE HTML REPORT(S)", dec)
