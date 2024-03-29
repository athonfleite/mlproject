import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocess_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function performs data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                                   "gender",
                                   "race_ethnicity",
                                   "parental_level_of_education",
                                   "lunch",
                                   "test_preparation_course"
                                   ]
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            logging.info("Numerical columns scaling completed")
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler())
                ]
            )
            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transforamtion(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Data reading completed.")
            logging.info("Getting preprocessed object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_ = train_df.drop(columns=[target_column], axis=1)
            target_feature_train_ = train_df[target_column]
            
            input_feature_test_ = test_df.drop(columns=[target_column], axis=1)
            target_feature_test_ = test_df[target_column]

            logging.info("Applying preprocessor")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_)
        
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_)
            ]
            logging.info(f"Saved preprocessing object")

            return (train_arr,test_arr, self.data_transformation_config.preprocess_obj_file_path)
        except Exception as e:
            raise CustomException(e, sys)
