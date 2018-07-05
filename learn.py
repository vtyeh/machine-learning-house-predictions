import pandas as pd
import numpy as np
import re
import datetime
import pickle
import sklearn as sk
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, SGDClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cross_validation import train_test_split, KFold, StratifiedShuffleSplit
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve, precision_recall_curve
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from definitions import summaryfile_type

california = pd.read_csv('total_2017_ca.csv', dtype=summaryfile_type,
                      nrows=9000000)
california.drop(california.columns[:1], axis=1, inplace=True)
california.rename(columns=lambda x: re.sub('[.]', '_', x), inplace=True)
ca_filtered = california.dropna(subset=('OLTV', 'OCLTV', 'DTI', 'CSCORE_B'))
ca_known = ca_filtered[ca_filtered['Zero_Bal_Code'] > 0]
state_mean = ca_known.groupby('STATE')[('ORIG_AMT', 'OCLTV', 'DTI')].mean()
state_std = ca_known.groupby('STATE')[('ORIG_AMT', 'OCLTV', 'DTI')].std()

class ExtractCreditScore(sk.base.BaseEstimator, sk.base.TransformerMixin):

    def __init__(self, is_take_minimum=True):
        self.take_minimum = is_take_minimum
        self.where = np.where
        pass

    def fit(self, x, y):
        return self

    def transform(self, x):
        result = self.where((x['CSCORE_B'] - x['CSCORE_C'] > 0), x['CSCORE_C'], x['CSCORE_B'])
        return result.reshape(-1, 1)

class ExtractNormalized(sk.base.BaseEstimator, sk.base.TransformerMixin):

    def __init__(self, groupby, target, total_mean=state_mean, total_std=state_std):
        self.groupby = groupby
        self.target = target
        self.total_mean = total_mean
        self.total_std = total_std
        pass

    def fit(self, x, y):
        return self

    def transform(self, x):
        temp1 = x.groupby(self.groupby)[[self.groupby, self.target]
                                        ].apply(lambda x: (x[self.target])).values
        temp2 = x.groupby(self.groupby)[[self.groupby, self.target]].apply(
            lambda x: self.total_mean.loc[x[self.groupby].values, self.target]).values
        temp3 = x.groupby(self.groupby)[[self.groupby, self.target]].apply(
            lambda x: self.total_std.loc[x[self.groupby].values, self.target]).values
        return ((temp1 - temp2) / temp3).reshape(-1, 1)

class ExtractCategory(sk.base.BaseEstimator, sk.base.TransformerMixin):

    def __init__(self, colname):
        self.colname = colname
        self.transformer = LabelEncoder()
        pass

    def fit(self, x, y):
        self.transformer.fit(x[self.colname])
        return self

    def transform(self, x):
        return self.transformer.transform(x[self.colname]).reshape(-1, 1)

class ExtractLoanStatus(sk.base.BaseEstimator, sk.base.TransformerMixin):

    def __init__(self):
        '''
        Initialize the class with bisection of the loan status: Default or Healthy
        '''
        pass

    def fit(self, x):
        return self

    def transform(self, x):
        '''
        Transform the loan status to a tertiary status: Healthy (0), Default (1)
        '''
        status = x['Zero_Bal_Code'].apply(lambda x: 0 if x <= 1 else 1)
        return status
sss = StratifiedShuffleSplit(ExtractLoanStatus().fit_transform(ca_known), 1, test_size=0.15)
for train_index, test_index in sss:
    ca_train = ca_known.iloc[train_index, ]
    ca_test = ca_known.iloc[test_index, ]
    status_train = ExtractLoanStatus().fit_transform(ca_known).iloc[train_index, ]
    status_test = ExtractLoanStatus().fit_transform(ca_known).iloc[test_index, ]

# Stochastic Gradient Descent Method
features = FeatureUnion([
    ('Loan_Amount', ExtractNormalized('STATE', 'ORIG_AMT')),
    ('credit score', ExtractCreditScore()),
    ('Loan_to_Value', ExtractNormalized('STATE', 'OCLTV')),
    ('Debt_to_income', ExtractNormalized('STATE', 'DTI')),
    ('Loan_purpose', ExtractCategory('PURPOSE')),
    ('Property_Type', ExtractCategory('PROP_TYP')),
    ('Occupancy_Status', ExtractCategory('OCC_STAT'))
])

model = Pipeline([
    ('features', features),
    ('scale', StandardScaler()),
    ('SGD', SGDClassifier(loss='hinge', class_weight='balanced'))
])

model.fit(ca_train, status_train)
status_pred = model.predict(ca_test)
print('The AUC of this SGD model is:',
      roc_auc_score(status_test, model.decision_function(ca_test)))

pred = model.predict(ca_test)
print('Classfication Report:')
print(classification_report(status_test, pred))
print(pd.DataFrame(confusion_matrix(status_test, pred), index=['Actual Healthy',
                                                                'Actual Default'],
                   columns=['Pred. Healthy', 'Pred. Default']))
print('Writing Stochastic Gradient Descent model to file...')

with open('sgd-model.pkl', 'wb') as f:
    pickle.dump(model, f)