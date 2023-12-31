import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
@dataclass
class DataIngestionConfig: #this will confgure the path where the training and testing data ll need to be saved in
    training_path: str=os.path.join('artifacts',"train.csv") #this creates an attribute wiht a defualt value of the training path resulting in the artifacts folder, and within that folder, there ll be the train.csv
    testing_path: str=os.path.join('artifacts',"test.csv")
    raw_path: str=os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self):
        self.ingest_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('entered the data ingestion')
        try:
            df = pd.read_csv('note_book\data\stud_perf_model.csv')
            logging.info('read the dataset')

            os.makedirs(os.path.dirname(self.ingest_config.training_path), exist_ok = True)

            df.to_csv(self.ingest_config.raw_path, index = False, header = True)
            logging.info('Train test split initiated')
            training_set, testing_set = train_test_split(df, test_size= 0.2, random_state = 42)

            training_set.to_csv(self.ingest_config.training_path, index = False, header = True)
            testing_set.to_csv(self.ingest_config.testing_path, index = False, header = True)

            logging.info("ingestion is completed")
            return (
                self.ingest_config.training_path,
                self.ingest_config.testing_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion() #this instantitates the dataingestion class
    training_path, testing_path = obj.initiate_data_ingestion() #this will create the files and directories and logs

    data_transformation = DataTransformation()#this instantiates the datatransformation class
    train_after_array, test_after_array,_=data_transformation.initiate_data_transform(training_path, testing_path)#this will use the training path and testing path from the ingestion part, and will initiate the data transformation phase

    model_trainer = ModelTrainer() #this instantiates the model trainer class
    model_trainer.initiate_model_training(train_after_array, test_after_array)#this will use the training and testing dataset that has been transformed, and will find the optimal model, and then give the 

