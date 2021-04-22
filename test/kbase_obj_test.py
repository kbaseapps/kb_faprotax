import numpy as np
import pandas as pd
from pytest import raises
from unittest.mock import patch


from kb_faprotax.util.kbase_obj import AmpliconMatrix, AttributeMapping
from kb_faprotax.util.error import ValidationException
from mock import * # mock business

####################################################################################################
####################################################################################################
def test_AmpliconMatrix_methods():
    '''
    dprint('Var.tmp # globals', run=globals())
    from kb_faprotax.util.kbase_obj import Var; dprint('Var.tmp # locals', run=locals())
    '''

    # use as cm since patch.dict decs interfering with e/o for some reason
    with patch.dict('kb_faprotax.util.kbase_obj.Var', values={
                    'tmp': 'test_AmpMat_methods', 'dfu': mock_dfu}):
        amp_mat = AmpliconMatrix(enigma50by30)
        row_attr_map = AttributeMapping(enigma50by30_rowAttrMap, amp_mat)

    # id_l and tax_l correspond to AmpliconMatrix rows
    # which don't necessarily map 1-to-1 [bijectively] with row AttributeMapping
    ind = row_attr_map.get_attr_ind('taxonomy')
    id_l = amp_mat.obj['data']['row_ids']
    tax_l = row_attr_map.get_ordered_tax_l(ind, id_l)

    # superficially test `to_OTU_table`
    df1 = pd.read_csv(
        os.path.join(TEST_DATA_DIR, 'return/enigma50by30/return/otu_table.tsv'), 
        sep='\t', index_col='taxonomy') 
    df2 = amp_mat.to_OTU_table(tax_l)

    assert df1.columns.tolist() == df2.columns.tolist()
    assert df1.index.tolist() == df2.index.tolist() # index is `taxonomy`
    assert df1['OTU_Id'].tolist() == df2['OTU_Id'].tolist() # first column is `OTU_Id`

    data1 = df1.iloc[:,1:].values # rest of columns are data
    data2 = df2.iloc[:,1:].values

    assert np.allclose(data1, data2) and np.allclose(data2, data1) 

####################################################################################################
####################################################################################################
def test_AttributeMapping_methods():

    # update with
    id2attr0 = {'amplicon_id_2': 'red', 'amplicon_id_5': 'green', 'amplicon_id_9': 'blue'} 
    id2attr1 = {'amplicon_id_2': 'black hole', 'amplicon_id_5': 'quasar', 'amplicon_id_9': 'dark matter'}

    # use as cm since patch.dict decs interfering with e/o for some reason
    with patch.dict('kb_faprotax.util.kbase_obj.Var', values={
                    'tmp': 'AttrMap_methods', 'dfu': mock_dfu}):
        amp_mat = AmpliconMatrix(dummy10by8)
        row_attr_map = AttributeMapping(dummy10by8_rowAttrMap, amp_mat)
        row_attr_map_orig = AttributeMapping(dummy10by8_rowAttrMap, amp_mat)

    # new attribute name
    ind0, name0 = row_attr_map.add_attribute_slot('color', 'unit testing')
    row_attr_map.map_update_attribute(ind0, id2attr0)
    assert ind0 == row_attr_map.attributes_length-1, '%d vs %d' % (ind0, row_attr_map.attributes_length-1)
    assert ind0 == 2
    assert name0 == 'color'
    row_attr_map._check_attr_consistent(ind0, 'color', 'unit testing', id2attr0)

    # update in existing attribute/upload slot
    ind1, name1 = row_attr_map.add_attribute_slot('celestial body', 'upload')
    row_attr_map.map_update_attribute(ind1, id2attr1)
    assert ind1 == row_attr_map.attributes_length-1
    assert ind1 == 3 
    assert name1 == 'celestial body (1)'
    row_attr_map._check_attr_consistent(ind1, 'celestial body (1)', 'upload', id2attr1)

    #
    assert row_attr_map.get_attr_ind('gene') is None

    # gets first attribute match
    assert row_attr_map.get_attr_ind('celestial body (1)') == ind1

    # original attributes unchanged
    assert row_attr_map.get_attributes_at(0) == row_attr_map_orig.get_attributes_at(0)
    assert row_attr_map.get_attributes_at(1) == row_attr_map_orig.get_attributes_at(1)

####################################################################################################
####################################################################################################
def test_AmpliconMatrix_validation():
    '''
    Test validation of amplicon table in AmpliconMatrix
    Should be (1) count data,  missing (None) allowed
    Can assume that obj holds data in list of lists of numeric/None
    '''
    
    logging.info('Testing with test_AmpliconMatrix_validation')

    # use as cm since patch.dict decs interfering with e/o for some reason
    with patch.dict('kb_faprotax.util.kbase_obj.Var', values={
                    'tmp': 'AmpMat_validation', 'dfu': mock_dfu}):
        amp_mat = AmpliconMatrix(dummy10by8)

    
    with raises(ValidationException, match='[Ii]nteger'): amp_mat.validate_amplicon_abundance_data()


    amp_mat.obj['data']['values'] = [0.0, 0.0, 1319.0, 1.0] # float
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [0, 0, 1319, 1] # int
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0., 0., 1319., 1.] # float, with missing
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0, 0, 1319, 1] # int, with missing
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0, -0., 1319.0, 1] # int/float, with missing
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, None, 0, -0, 0.0, 0, 0.] # 0s, with missing
    amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0.999999999] # close enough
    amp_mat.validate_amplicon_abundance_data() 

    amp_mat.obj['data']['values'] = [None, -0.0000000001] # close enough
    amp_mat.validate_amplicon_abundance_data() 

    
    amp_mat.obj['data']['values'] = [0.9]
    with raises(ValidationException, match='[Ii]nteger'): amp_mat.validate_amplicon_abundance_data() 

    amp_mat.obj['data']['values'] = [-1]
    with raises(ValidationException, match='[Nn]egative'): amp_mat.validate_amplicon_abundance_data() 

    amp_mat.obj['data']['values'] = [None, None, None]
    with raises(ValidationException, match='all missing'): amp_mat.validate_amplicon_abundance_data() 

    amp_mat.obj['data']['values'] = [None]
    with raises(ValidationException, match='all missing'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, -1]
    with raises(ValidationException, match='[Nn]egative'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, None, 1.00001]
    with raises(ValidationException, match='[Ii]nteger'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [-1.0, 0, 1319]
    with raises(ValidationException, match='[Nn]egative'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0, 1, 2, 3, 4.5]
    with raises(ValidationException, match='[Ii]nteger'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [None, 0.0, 1.0, 2.0, 3.0, 4.00001] # 4.00001 would pass with np.allclose default rtol
    with raises(ValidationException, match='[Ii]nteger'): amp_mat.validate_amplicon_abundance_data()

    amp_mat.obj['data']['values'] = [0.9, -0.9]
    with raises(ValidationException): amp_mat.validate_amplicon_abundance_data() 



####################################################################################################
####################################################################################################
def test_GenomeSet_methods():
    pass
   

####################################################################################################
####################################################################################################
def test_Genome_methods():
    pass
