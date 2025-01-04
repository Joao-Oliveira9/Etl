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


""" def defining_cell_length(dataframe,cursor):
    colunas = [desc[0] for desc in cursor.description]
    dataframe.columns = colunas
    length_of_colummn = len(dataframe.at[0,'aluno_id']) 
    return length_of_colummn """


def adjusting_cell_size2(dataframe,ws):
    count = 0
    for coluna in dataframe.columns:
        max_width = 0
        """ print(coluna) """
        """ print(dataframe[coluna][0])  """
       
        for linha in range(0,len(dataframe)):
            """ print(linha) """
            dado = dataframe[coluna][linha]
            """ print(dado) """
            if isinstance(dado, float):
                dado = str(dado)


            tamanho_dado = len(dado)
            if(tamanho_dado > max_width):
                max_width = tamanho_dado
        count = count + 1
    
        ws.column_dimensions[chr(count+64)].width = max_width + 1
    return ws
        

""" def adjusting_cell_size(dataframe,cursor,ws):
    count = 0
    for coluna in cursor.description:
     
        max_width = 0
        for linha in dataframe.axes[0]:
           
            coordenada = dataframe.at[linha,coluna.name]
            if isinstance(coordenada, pd.Timestamp):
                coordenada = str(coordenada)
             
            
            length_of_colummn = len(coordenada) 
            if length_of_colummn > max_width:
                max_width = length_of_colummn + 1

        count = count + 1
        ws.column_dimensions[chr(count+64)].width = max_width
    return ws
 """

def create_dataframe2(cursor):
    statement = """ select tb_aluno.nome,tb_curso.nome,tb_aluno_disciplina.nota from tb_aluno inner join tb_aluno_disciplina on tb_aluno.aluno_id = tb_aluno_disciplina.aluno_id 
    inner join tb_disciplina on tb_disciplina.id = tb_aluno_disciplina.disciplina_id
    inner join tb_curso on tb_curso.id_curso = tb_aluno.curso_id;"""

    statement_nome_aluno = """ select nome from tb_aluno; """


    cursor.execute(statement_nome_aluno)
    dataframe_nome_aluno = pd.DataFrame(cursor.fetchall())
    dataframe_nome_aluno_sorted = dataframe_nome_aluno.sort_values(by=dataframe_nome_aluno.columns[0]).reset_index(drop=True)
    """ print(cursor.description) """

    numero_linhas = len(dataframe_nome_aluno)

    list_names = []

    for i in range(0,numero_linhas):
        list_names.append(dataframe_nome_aluno[0][i])



    cursor.execute(statement)
    dataframe = pd.DataFrame(cursor.fetchall())


    dataframe_ordenado = dataframe.sort_values(by=dataframe.columns[0]).reset_index(drop=True)
    """ print(dataframe_ordenado)  """

    lista_notas = []
    nota_total = 0
    tamanho_lista = len(dataframe_ordenado) 
    nome_aluno = dataframe_ordenado[0][0]
    count = 1

    for i in range (0,tamanho_lista):
        if(i!=tamanho_lista-1):
            if(dataframe_ordenado[0][i+1] != nome_aluno):
                nome_aluno = dataframe_ordenado[0][i+1] 
                nota_total = nota_total / count
                lista_notas.append(nota_total)
                nota_total = 0
                count = 0
            else:
                count = count + 1
                nota_total = nota_total + dataframe_ordenado[2][i]
        else:
             nota_total = nota_total + dataframe_ordenado[2][i]
             count = count + 1
             nota_total = nota_total / count
             lista_notas.append(nota_total)


    """ print(lista_notas) """

    dataframe_nome_aluno_sorted["Média das Notas"] = lista_notas
    dataframe_nome_aluno_sorted.rename(columns={dataframe.columns[0]: 'nome'}, inplace=True)
    """ print(dataframe_nome_aluno_sorted) """
    return dataframe_nome_aluno_sorted
    

