import psycopg2 as ps
import pandas as pd

conexao = ps.connect(
    database="db_cadastro",
    user='postgres',
    password='root',
    host='localhost',
    port= '5432'
)
cursor = conexao.cursor()

statement = "Select * from tb_aluno"

cursor.execute(statement)
colunas = [desc[0] for desc in cursor.description]

df = pd.DataFrame(cursor.fetchall())
df.columns = colunas
print(df) 

