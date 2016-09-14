
from pysat.spectral.spectral_data import spectral_data
from pysat.regression.pls_sm import pls_sm
import pandas as pd

class pysat_func(object):
    # Thus make sure that you have if's for all instances in functions where unknown_data doesn't exist.
    def __init__(self):
        self.data = None
        self.unknown_data = None
        self.outpath = None
        self.unknowndatacsv = None
        self.maskfile = None
    

    def get_files(self, **kwargs):
        for key, value in kwargs.items():
            if key == "outpath":
                self.outpath = value
            elif key == "db":
                self.db = value
            elif key == "unknowndatacsv":
                self.unknowndatacsv = value
            elif key == "maskfile":
                self.maskfile = value

    def set_interp(self, data):
        #TODO interp should be it's ownn function
        self.unknown_data.interp(self.data.df['wvl'].columns)

    def get_range(self, data, ranges):
        pass

    def get_spectra(self):
        self.data = pd.read_csv(self.db, header=[0, 1])
        self.data = spectral_data(self.data)
        self.unknown_data = pd.read_csv(self.unknowndatacsv, header=[0, 1])
        self.unknown_data = spectral_data(self.unknown_data)
        
    #TODO make mask it's own function
    #TODO Get rid of maskfile, you will want to stick that into another module
    def set_mask(self):
        self.data.mask(self.maskfile)
        self.unknown_data.mask(self.maskfile)
        
    def get_ranges(self, data, ranges):
        data.norm(ranges)
        unknown_data = self.unknown_data
        unknown_data.norm(ranges)
        return unknown_data

    def set_element_name(self, el):
        self.el = el

    def set_nfolds(self, nfolds_test):
        self.nfolds_test = nfolds_test

    def set_testfold_test(self, testfold_test):
        self.testfold_test = testfold_test

    def get_element_name(self):
        return self.el

    def get_nfolds(self):
        return self.nfolds_test

    def get_testfold_test(self):
        return self.testfold_test

    def set_compranges(self, data):
        """ Usage:         [[-20, 50], [30, 70], [60, 100], [0, 120]]
        :param data:
        :return:
        """
# ###################################################
# # remove a test set to be completely excluded from CV
# # and used to assess the final blended model
# ###################################################
# data1.stratified_folds(nfolds=nfolds_test, sortby=('meta', el))
# data1_train = data1.rows_match(('meta', 'Folds'), [testfold_test], invert=True)
# data1_test = data1.rows_match(('meta', 'Folds'), [testfold_test])
#
# ###################################################
# # Create the models here in order: Low, Mid, High, Full
# # The full model will be used as a references to determine which submodel is appropriate
# # The Full model will be computed last
# ###################################################
# ncs = [7, 7, 5, 9]
# traindata = [data1_train.df, data1_train.df, data1_train.df, data1_train.df]
# testdata = [data1_test.df, data1_test.df, data1_test.df, data1_test.df]
# unkdata = [unknown_data1.df, unknown_data1.df, unknown_data1.df, unknown_data1.df]
#
# sm = pls_sm()
#
# sm.fit(traindata, compranges, ncs, el, figpath=outpath)
#
# predictions_train = sm.predict(traindata)
#
# predictions_test = sm.predict(testdata)
#
# blended_train = sm.do_blend(predictions_train, traindata[0]['meta'][el])
#
# blended_test = sm.do_blend(predictions_test)
#
# ###################################################
# # Create all the Plots in Outpath
# ###################################################
# sm.final(testdata[0]['meta'][el],
#          blended_test,
#          el=el,
#          xcol='Ref Comp Wt. %',
#          ycol='Predicted Comp Wt. %',
#          figpath=outpath)
