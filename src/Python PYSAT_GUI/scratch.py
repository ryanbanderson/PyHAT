from pysat_function import pysat_func

pysat = pysat_func()



# outpath = r'C:\Users\nfinch\Desktop\Output'
# db = r"C:\Users\nfinch\Desktop\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
# unknowndatacsv = r"C:\Users\nfinch\Desktop\lab_data_averages_pandas_format.csv"
# maskfile = r"C:\Users\nfinch\Desktop\mask_minors_noise.csv"

pysat.set_file_outpath(r'C:\Users\nfinch\Desktop\Output')
pysat.set_file_db(r'C:\Users\nfinch\Documents\GitHub\PySAT\src\Python PYSAT_GUI\full_db_mars_corrected_dopedTiO2_pandas_format.csv')
pysat.set_file_unknowndatacsv(r'C:\Users\nfinch\Documents\GitHub\PySAT\src\Python PYSAT_GUI\lab_data_averages_pandas_format.csv')
pysat.set_file_maskfile(r'C:\Users\nfinch\Documents\GitHub\PySAT\src\Python PYSAT_GUI\mask_minors_noise.csv')

pysat.get_spectra()
pysat.set_interp()
pysat.set_file_maskfile()

data.mask(maskfile)
unknown_data.mask(maskfile)

###################################################
# Normalizing Data and getting Ranges
# range3: equivalent to norm3
# range1: equivalent to norm1
###################################################
ranges1 = [(0, 1000)]

data1 = data
data1.norm(ranges1)
unknown_data1 = unknown_data
unknown_data1.norm(ranges1)

###################################################
# nfolds: the number of folds to divide data into to extract an overall test set
# testfold: which fold to use as the overall test set
# nfolds_cv: Number of folds for CV
# testfold_cv: Which fold to use as the test set for cross validation
# Cross Validation
###################################################
el = 'SiO2'
nfolds_test = 6
testfold_test = 4

###################################################
# Composition Ranges
# These are the composition ranges for the submodels
# nc: max number of components
###################################################

compranges = [[-20, 50], [30, 70], [60, 100], [0, 120]]

###################################################
# remove a test set to be completely excluded from CV
# and used to assess the final blended model
###################################################
data1.stratified_folds(nfolds=nfolds_test, sortby=('meta', el))
data1_train = data1.rows_match(('meta', 'Folds'), [testfold_test], invert=True)
data1_test = data1.rows_match(('meta', 'Folds'), [testfold_test])

###################################################
# Create the models here in order: Low, Mid, High, Full
# The full model will be used as a references to determine which submodel is appropriate
# The Full model will be computed last
###################################################
ncs = [7, 7, 5, 9]
traindata = [data1_train.df, data1_train.df, data1_train.df, data1_train.df]
testdata = [data1_test.df, data1_test.df, data1_test.df, data1_test.df]

sm = pls_sm()

sm.fit(traindata, compranges, ncs, el, figpath=outpath)

predictions_train = sm.predict(traindata)

predictions_test = sm.predict(testdata)

blended_train = sm.do_blend(predictions_train, traindata[0]['meta'][el])

blended_test = sm.do_blend(predictions_test)

###################################################
# Create all the Plots in Outpath
###################################################
sm.final(testdata[0]['meta'][el],
         blended_test,
         el=el,
         xcol='Ref Comp Wt. %',
         ycol='Predicted Comp Wt. %',
         figpath=outpath)
