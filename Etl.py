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
    """ print(len(dataframe.axes[0])) """
    colunas = [desc[0] for desc in cursor.description]
    dataframe.columns = colunas
    length_of_colummn = len(dataframe.at[0,'aluno_id']) 
    return length_of_colummn


def adjusting_cell_size(dataframe,cursor,ws):
    count = 0
    for coluna in cursor.description:
        """" cursor.description[0] """
        max_width = 0
        for linha in dataframe.axes[0]:
            """ print("passei aqui") """
            coordenada = dataframe.at[linha,coluna.name]
            if isinstance(coordenada, pd.Timestamp):
                coordenada = str(coordenada)
                """ print(coordenada) """
            
            length_of_colummn = len(coordenada) 
            if length_of_colummn > max_width:
                max_width = length_of_colummn + 1

        count = count + 1
        ws.column_dimensions[chr(count+64)].width = max_width
    return ws


conexao = ps.connect(
    database= "db_cadastro",
    user="postgres",
    password="root",
    host="localhost",
    port= "5432"
)

statement = """ select tb_aluno.nome,tb_curso.nome,tb_aluno_disciplina.nota from tb_aluno inner join tb_aluno_disciplina on tb_aluno.aluno_id = tb_aluno_disciplina.aluno_id 
inner join tb_disciplina on tb_disciplina.id = tb_aluno_disciplina.disciplina_id
inner join tb_curso on tb_curso.id_curso = tb_aluno.curso_id;"""

statement_nome_aluno = """ select nome from tb_aluno; """

cursor = conexao.cursor()



cursor.execute(statement_nome_aluno)
dataframe_nome_aluno = pd.DataFrame(cursor.fetchall())
print(cursor.description)

numero_linhas = len(dataframe_nome_aluno)

list_names = []

for i in range(0,numero_linhas):
     list_names.append(dataframe_nome_aluno[0][i])

""" print(list_names) """


cursor.execute(statement)
dataframe = pd.DataFrame(cursor.fetchall())

""" dataframe.sort_values(by=0) """

""" colunas = [desc[0] for desc in cursor.description]
dataframe.columns = colunas """


dataframe_ordenado = dataframe.sort_values(by=dataframe.columns[0]).reset_index(drop=True)
""" print(dataframe_ordenado)  """

lista_notas = []
nota_total = 0
tamanho_lista = len(dataframe_ordenado) 
nome_aluno = ""
print(dataframe_ordenado)
print(dataframe_ordenado[2][0])



for i in range (0,tamanho_lista):
    if(dataframe_ordenado[0][i] != nome_aluno):
        nome_aluno = dataframe_ordenado[0][i]
        lista_notas.append(nota_total)
        nota_total = 0
    else:
        nota_total = nota_total + dataframe_ordenado[2][i]

print(lista_notas)