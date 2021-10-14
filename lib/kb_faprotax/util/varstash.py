from dotmap import DotMap

'''
App globals and config
'''

_config = {
    'debug': True,  # toggle for global debugging behavior

    'template_flpth': '/kb/module/ui/template/edge_data.tt',

#----- run cmd
    'db_flpth': '/opt/FAPROTAX_1.2.4/FAPROTAX.txt',  # curated database file for FAPROTAX
    'cmd_flpth': '/opt/FAPROTAX_1.2.4/collapse_table.py',  # FAPROTAX executable

#----- files
    'TAX_TABLE_FN': 'otu_table.tsv',

    'COLLAPSED_FUNC_TABLE_FN': 'collapsed_func_table.tsv',
    'GROUPS2RECORDS_TABLE_FN': 'groups2records.tsv',
    'GROUPS2RECORDS_TABLE_DENSE_FN': 'groups2records_dense.tsv',

#----- names used in files
    'amplicon_hdr_id': 'amplicon_id',  # the column name of amplicon IDs in amplicon matrix file/df
    'taxonomy_hdr_id': 'taxonomy',  # the columns name of taxonomy strings in amplicon matrix file/df
    'amp_abun_flnm': 'amplicon_abundance_matrix.tsv',
}

Var = DotMap(_config, _dynamic=False)  # globals for app


def reset_Var():
    Var.clear()
    Var.update(_config)
