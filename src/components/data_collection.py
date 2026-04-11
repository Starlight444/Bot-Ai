import os 
import sys 

from src.components import scraper 
from src.utils.logger import logging
from src.utils.exception import Custom_exception

from dataclasses import dataclass


@dataclass
class DataCollectionConfig:
    is_airflow = os.getenv("IS_AIRFLOW", "false").lower() == "true"

    if is_airflow:
        path = '/opt/airflow/data'
    else:     
        path = 'data'   
    output_file_path: str = os.path.join(path, "data.csv")
 

class DataCollection:
    def __init__(self):
        self.data_collection_config = DataCollectionConfig()

    def initiate_data_collection(self):
        try:
            keyword = "shirt"
            num_products = 5
            
            logging.info(f"Starting data collection for '{keyword}'")

            data = scraper.scrape_products(keyword, num_products)        

            print("Data shape for", keyword, "is: ", data.shape)
            print("Sample data for", keyword, "is: ", data.head())

            file_path = self.data_collection_config.output_file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            data.to_csv(file_path, index=False)

            logging.info(f"Successfully collected and saved data for: {keyword}")
            return f"Collected data for {keyword}"
        
        except Exception as e:
            logging.error(f"Error occurred in data collection: {str(e)}")
            raise Custom_exception(e, sys)
        

# if __name__=="__main__":
#     data_collection = DataCollection()
#     data_collection.initiate_data_collection()
