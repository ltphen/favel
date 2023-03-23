from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
import logging
import numpy as np
import os, sys, ast, warnings, pdb, random
import pandas as pd
import pickle
import sklearn
import statistics
if not sys.warnoptions: warnings.simplefilter("ignore")

class ML:
    
    def __init__(self, output:bool):
        np.random.seed(random.randint(0, 10000))
        self.output = output


    def get_normalizer_object(self, normalizer_name):
        """
        Parse the sklearn normalizer defined in the configuration file as a string into a real normaliser
        """
        if normalizer_name.lower()=='Normalizer'.lower():
            return preprocessing.Normalizer()

        elif normalizer_name.lower()=='MinMaxScaler'.lower():
            return preprocessing.MinMaxScaler()
        
        elif normalizer_name.lower()=='StandardScaler'.lower():
            return preprocessing.StandardScaler()
        
        elif normalizer_name.lower()=='MaxAbsScaler'.lower():
            return preprocessing.MaxAbsScaler()

        elif normalizer_name.lower()=='RobustScaler'.lower():
            return preprocessing.RobustScaler()


    def normalise_data(self, df, normalizer_name=None, normalizer=None):
        """
        Normalise a given data using the normalizer specified as parameters
        """
        x = df.values #returns a numpy array
        
        if normalizer: 
            x_scaled = normalizer.fit_transform(x)
        elif normalizer_name == 'default':
            normalizer=None
            x_scaled = np.copy(x) # return the same matrix without normalising
        else:
            normalizer=self.get_normalizer_object(normalizer_name)
            x_scaled = normalizer.fit_transform(x)
       
        df = pd.DataFrame(x_scaled)
        return df, normalizer 


    def createDataFrame(self, assertions):
        """
        To create the DataFrame that consists of triples and scores from each approach for that particular triple.
        """
        try:
            
            result = dict()
            result['subject'] = []
            result['predicate'] = []
            result['object'] = []
            result['truth'] = []
            
            approaches = assertions[0].score.keys()

            for assertion in assertions:
                result['subject'].append(assertion.subject)
                result['predicate'].append(assertion.predicate)
                result['object'].append(assertion.object)
                result['truth'].append(assertion.expectedScore)
                
                for approach in approaches:
                    if not approach in result:
                        result[approach] = []
                    result[approach].append(assertion.score[approach])

            df = pd.DataFrame(result)
            
            return(df)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in createDataFrame: ', exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in createDataFrame: ' +' '+ str(e) + ' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            raise e


    def get_model_name(self, model):
        """
        Get the model name
        """
        mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
        return mdl_name


    def search_best_params(self,model, ml_model_params, X, y):
        """
        With a given range, this function search for the best parameters giving optimal perfomance to the given model. 
        Done using https://scikit-optimize.github.io/stable/modules/generated/skopt.BayesSearchCV.html 
        """
        params_range_dict={}
        for x in ml_model_params:
            if type(x['range'])==tuple:
                if type(x['range'][0]) == int: 
                    params_range_dict[x['name']] = Integer(x['range'][0], x['range'][1])
                elif type(x['range'][0]) == float: 
                    params_range_dict[x['name']] = Real(x['range'][0], x['range'][1])
            elif type(x['range']) == list:
                params_range_dict[x['name']] = Categorical(x['range'])

        opt = BayesSearchCV(
                    model,
                    params_range_dict,
                    n_iter=5,
                    random_state=0
                )
        _ = opt.fit(X, y)
        best_params=dict(opt.best_params_)
        return best_params


    def get_sklearn_model(self, model_name, ml_model_params, train_data):
        ''' from model name string specified in conf file, here we get the actual sklearn model obj '''

        X=train_data.drop(['subject', 'predicate', 'object', 'truth'], axis=1)
        y=train_data.truth

        xdf=pd.DataFrame(sklearn.utils.all_estimators())
        try:
            model = xdf[xdf[0]==model_name][1].item()
        except ValueError as ex:
            logging.error(f"Model '{model_name}' is unknown.")
            raise ex

        if ml_model_params == 'default':
            model=model()

        elif type(ast.literal_eval(ml_model_params)) == dict:
            model=model()
            ml_model_params=ast.literal_eval(ml_model_params)
            model.set_params(**ml_model_params)

        elif type(ast.literal_eval(ml_model_params)) == list:
            ml_model_params=ast.literal_eval(ml_model_params)
            model=model()
            best_params=self.search_best_params(model, ml_model_params, X, y) # skopt
            model.set_params(**best_params)

        return model


    def custom_model_train(self,X, y, model):
        """
        Training a model without cross validation
        """
        try:
            model=model.fit(X, y)
            mdl_name=self.get_model_name(model)

            # calculate roc_auc
            y_pred=model.predict_proba(X)

            class_1_index = 0 if model.classes_[0]=='1' else 1

            y_pred=y_pred[:, class_1_index]
                    
            roc_auc = metrics.roc_auc_score(y, y_pred)

            y_pred_class=model.predict(X)
            report_df = pd.DataFrame(metrics.classification_report(np.array(y, dtype=int), np.array(y_pred_class, dtype=int), output_dict=True)).T.reset_index(drop=False).rename(columns={'index': 'label'})

            return model, mdl_name, roc_auc, report_df
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in custom_model_train: ' +' '+str(e)+' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            raise e


    def custom_model_train_cv(self, X, y, model):
        """
        Training a model with cross validation
        """
        try:
            skfold=StratifiedKFold(n_splits=5)
            scores=cross_val_score(model, X, y,cv=skfold, scoring="roc_auc")

            return scores
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in custom_model_train_cv: '+' '+str(e) +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            raise e


    # Change model list here to be a single model
    def train_model(self, df, ml_model, normalizer_name, output_path):
        """
        Train a model using a specified algorithm (Given in the favel.conf file)

        Returns:
            - Model
            - Predicate lable encoder
            - Training AUC-ROC score
        """
        try:
            le = preprocessing.LabelEncoder()
            le.fit(df['predicate'])
            df['predicate']=le.transform(np.array(df['predicate'].astype(str), dtype=object))

            X=df.drop(['truth', 'subject', 'object'], axis=1)
            y=df.truth

            X, normalizer = self.normalise_data(df=X, normalizer_name=normalizer_name, normalizer=None)
            if normalizer and self.output:
                with open(f'{output_path}/normalizer.pkl','wb') as fp:   pickle.dump(normalizer,fp)


            print('TRAIN: ', X.shape, y.shape, ml_model, y.dtypes)

            roc_auc_cv_scores = self.custom_model_train_cv(X, y, ml_model)

            trained_model, model_name, roc_auc_overall_score, report_df = self.custom_model_train(X, y, ml_model)
            metrics = {"overall": roc_auc_overall_score, "cv_mean": np.mean(roc_auc_cv_scores), "cv_std": round(statistics.stdev(roc_auc_cv_scores), 2)}

            logging.info('ML model trained')


            if trained_model==False and model_name==False and roc_auc_overall_score==False: 
                return False
            elif self.output:
                report_df.to_excel(f'{output_path}/Classifcation Report.xlsx', index=False)

                with open(f'{output_path}/classifier.pkl','wb') as fp:   pickle.dump(trained_model,fp)
                with open(f'{output_path}/predicate_le.pkl','wb') as fp: pickle.dump(le,   fp)

                logging.debug('ML model and labelencoder saved in output path')

            return trained_model, le, normalizer, metrics
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Error in train_model: ', ex, exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in train_model: ' +' '+str(ex)+' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            raise ex


    def test_model(self, df, ml_model, le_predicate, normalizer):
        """
        Given a trained model, this function predict scores of the assertions given in the df dataframe
        """
        try:
            X=df.drop(['truth','subject', 'object'], axis=1)
            y=df.truth

            X['predicate'] = X['predicate'].map(lambda s: '-1' if s not in le_predicate.classes_ else s)
            le_predicate.classes_ = np.append(le_predicate.classes_, '-1')

            # pdb.set_trace()
            X['predicate'] = le_predicate.transform(np.array(X['predicate'].astype(str), dtype=object))
            # X = df.drop(['subject','object'], axis=1)

            if normalizer is None:
                logging.debug('Using default normalizer')
            else:
                try: 
                    X, normalizer = self.normalise_data(df=X, normalizer_name=None, normalizer=normalizer)
                except: 
                    logging.error('No normalizer found')

            y_pred=ml_model.predict_proba(X)
            class_1_index = 0 if ml_model.classes_[0]=='1' else 1

            y_pred=y_pred[:, class_1_index]
            df['ensemble_score'] = y_pred
                    
            roc_auc = metrics.roc_auc_score(y, y_pred)

            logging.info('Validation completed')

            return df, roc_auc

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in test_model: ', exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in test_model: ' +str(e)+ ' ' +str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            raise e
