import requests
import json
import os
from pyspark.sql import SparkSession

def fetch_data():
    print("Iniciando a tarefa de buscar dados")
    url = "https://api.openbrewerydb.org/breweries"
    response = requests.get(url)
    data = response.json()
    
    bronze = '/opt/airflow/data/bronze'
    os.makedirs(bronze, exist_ok=True)
    
    try:
        with open(f'{bronze}/breweries.json', 'w') as f:
            json.dump(data, f)
        print(f'Dados brutos salvos em {bronze}/breweries.json')
    except Exception as e:
        print(f'Erro ao salvar dados brutos: {e}')

def process_data():
    print("Iniciando a tarefa de processar dados")
    try:
        # Inicializa o SparkSession
        spark = SparkSession.builder \
            .appName("BreweryData") \
            .master("spark://inbev-spark-1:7077") \
            .config("spark.driver.host", "localhost") \
            .config("spark.driver.bindAddress", "0.0.0.0") \
            .config("spark.driver.port", "4041") \
            .config("spark.network.timeout", "600s") \
            .getOrCreate()

        
        bronze_ = '/opt/airflow/data/bronze/breweries.json'
        
        if os.path.exists(bronze_):
            try:
                
                spark_df = spark.read.json(bronze_)
                
                silver = '/opt/airflow/data/silver'
                os.makedirs(silver, exist_ok=True)
                spark_df.write.partitionBy("state").parquet(silver)
                print(f'Dados transformados salvos em {silver}')
                
                
                gold_df = spark_df.groupBy("state", "brewery_type").count()
                
                gold_path = '/opt/airflow/data/gold'
                os.makedirs(gold_path, exist_ok=True)
                gold_df.write.parquet(gold_path)
                print(f'Dados agregados salvos em {gold_path}')
                
            except Exception as e:
                print(f'Erro ao processar dados: {e}')
            finally:
                spark.stop()
        else:
            print(f'Arquivo não encontrado: {bronze_}')
    except Exception as e:
        print(f'Erro ao iniciar o Spark: {e}')

if __name__ == "__main__":
    fetch_data()
    process_data()
