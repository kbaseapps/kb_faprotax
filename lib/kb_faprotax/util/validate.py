import numpy as np
import functools

from .debug import dprint



####################################################################################################
####################################################################################################
MISSING_VALS = [None, '', 'None', np.nan] # Below functions should implicitly handle these missing values

class Validate:
    
####################################################################################################
####################################################################################################
    @classmethod
    def replace_missing(cls, a: np.ndarray, rep=np.nan):
        '''
        Use np.ndarray because
        (1) Easier to detect `None`
        (2) Common denominator
        '''    
        if np.issubdtype(a.dtype, int) and rep in [np.nan, None]:
            raise Exception('Cannot assign special missing values to numpy integer array')

        for missing in MISSING_VALS:
            """
            dprint( 
                    'missing',
                    'type(missing)',
                    'a', 
                    'a.dtype', 
                    'a == np.array(missing, dtype=object)', 
                    run={**globals(),**locals()}
                    )
            """
            try:
                a[a == np.array(missing, dtype=object)] = rep
            except:
                raise Exception(missing)

        return a

####################################################################################################
####################################################################################################
    @classmethod
    def get_num_missing(cls, a: np.ndarray):
        num = 0
        for missing in MISSING_VALS:
            
            """
            dprint( 
                    'missing',
                    'type(missing)',
                    'a', 
                    'a.dtype', 
                    'a == np.array(missing, dtype=object)', 
                    run={**globals(),**locals()}
                    )
            """
            
            num = num + (a == np.array(missing, dtype=object)).sum() # cast missing as obj np.array to get element-wise comparison
        
        return num


####################################################################################################
####################################################################################################
    @classmethod
    def as_numeric(cls, a: np.ndarray, rep=np.nan, dtype=float):
        '''
        Warning: NumPy integer arrays do not support missing values (np.nan etc.)
        Also a.astype(int) will truncate floats into ints
        '''

        if np.issubdtype(dtype, int) and rep in [np.nan, None]:
            raise Exception('Cannot assign special missing values to numpy integer array')

        if np.issubdtype(a.dtype, int) and rep in [np.nan, None]:
            a = a.astype(float) # cast to float first to allow assigning special values

        a = cls.replace_missing(a)

        try:
            a = a.astype(dtype)
            return a
        except ValueError:
            return None

        raise



####################################################################################################
####################################################################################################
    @classmethod
    def is_int_like(cls, a: np.ndarray, missingOk=True):

        allclose_ = functools.partial(
            np.allclose, 
            equal_nan=missingOk, # NaNs equal 
            atol=1e-8, # same
            rtol=1e-8, # decrease otherwise 4.00001 == 4
        )
        a_round = np.round(a)

        return allclose_(a, a_round) and allclose_(a_round, a)


####################################################################################################
####################################################################################################
    


