import psycopg2 as ps
import pandas as pd
from openpyxl import load_workbook

def connection_with_database(database_name,user_name,password,host,port):
    conexao = ps.connect(
    database= database_name,
    user=user_name,
    password=password,
    host=host,
    port= port
    )
    """ port 5432 é a porta default do postgress """
    cursor = conexao.cursor()
    return cursor

def create_dataframe(statement,cursor):
    cursor.execute(statement)
    dataframe = pd.DataFrame(cursor.fetchall())
    return dataframe

def write_into_excel(name_file,dataframe):
    """ Com ExcelWriter indicamos o contexto/o arquivo onde deve ser transportado os dados"""
    with pd.ExcelWriter(name_file,engine='openpyxl') as writer:
        """ ExcelWriter com to_excel caso tenha mais de uma tabela """
        dataframe.to_excel(writer,index=False)

def defining_cell_length(dataframe,cursor):
    colunas = [desc[0] for desc in cursor.description]
    dataframe.columns = colunas
    length_of_colummn = len(dataframe.at[0,'aluno_id']) 
    return length_of_colummn

def columns_length(dataframe,cursor):
    print(cursor.description)
    