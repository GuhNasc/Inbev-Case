Este case é um pipeline de dados que coleta, processa e transforma dados de cervejarias usando Airflow e Spark. 
A coleta de dados é feita através de uma API e os dados são armazenados no data lake que utiliza as camadas: bronze, silver e gold. 
O objetivo é criar um processo automatizado e escalável para transformar dados brutos em dados agregados.

=== EXECUÇÃO DO PROJETO ===

Construa os contêineres usando o Docker Compose:
docker-compose build

Inicie os contêineres:
docker-compose up -d

Acesse o terminal do contêiner do Airflow e execute o script:
docker exec -it inbev-airflow-1 /bin/bash
python /scripts/consumirAPI.py

Ou acesse a interface do airflow e ligue a dag
