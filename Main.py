from Etl import *

statement = "Select * from tb_aluno"
file_name = "df_tabela.xlsx"

cursor = connection_with_database("db_cadastro","postgres","root","localhost","5432")
dataframe = create_dataframe2(cursor)
""" length_cell = defining_cell_length(dataframe,cursor) """
write_into_excel(file_name,dataframe)



wb = load_workbook("df_tabela.xlsx")
ws = wb["Sheet1"] 

ws = adjusting_cell_size2(dataframe,ws)

wb.save("df_tabela.xlsx")
 

