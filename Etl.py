import psycopg2 as ps
import pandas as pd
from openpyxl import load_workbook

""" conexao com o banco de dados """
conexao = ps.connect(
    database="db_cadastro",
    user='postgres',
    password='root',
    host='localhost',
    port= '5432'
)

"""criacao de um cursor pra execucao dos comandos sql"""
cursor = conexao.cursor()

""" montando um statement """
statement = "Select * from tb_aluno"

""" executando esse statement """
cursor.execute(statement)

""" processo de compressao de lista """
colunas = [desc[0] for desc in cursor.description]

""" resulado do execute """
df = pd.DataFrame(cursor.fetchall())
df.columns = colunas


""" pd.ExcelWriter ele prepara o contexto da aplicacao, mostrando qual o caminho que deve ser colocado o execel """
with pd.ExcelWriter('df_tabela.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)


""" coletando o tamanho de uma coluna que usa o padrao uuid """
length_of_colummn = len(df.at[0,'aluno_id']) 
print(length_of_colummn)

wb = load_workbook("df_tabela.xlsx")
ws = wb["Sheet1"]

ws.column_dimensions["A"].width = 36

wb.save("df_tabela.xlsx")