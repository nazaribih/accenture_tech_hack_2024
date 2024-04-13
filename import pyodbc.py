import pyodbc 

# Set up connection details
server = 'hackaton-gr10-sqlserverskfpe.database.windows.net'
database = 'hackaton-gr10-sqldb'
username = 'hacksqlusr012993'
password = 'hacksqlusrP@ssw00rd'
driver= '{ODBC Driver 18 for SQL Server}'

# Construct the connection string
conn_str = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

connection = pyodbc.connect(conn_str)

cursor = connection.cursor()
cursor.execute("SELECT TABLE_SCHEMA,TABLE_NAME FROM information_schema.tables WHERE table_type IN ('BASE TABLE', 'VIEW')")
rows = cursor.fetchall()
data = []
db_scheme = ""

for row in rows:
    data += [row]
    
for elem in data:
    db_scheme+=elem[0]+","+elem[1]+';'



# connection with the model

import openai

 
openai.api_base = "https://openaihackaton2024.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = '89652dc9313147ac8aa7e074dca1e07c'

user_query = "Give us aggregated data about sales of the last year"
db_scheme = "SELECT TABLE_SCHEMA,TABLE_NAME FROM information_schema.tables WHERE table_type IN ('BASE TABLE', 'VIEW')--ORDER BY type_desc, name;"
 
to_pass = "\
           You have access to several databases and a user provides a query in natural language. Your task is to generate the corresponding SQL query to access the data from the database.\
User Query: " + user_query + " Return only SQL query as an answer \n. The database scheme is: \n" + db_scheme

response = openai.Completion.create(
  engine="gpt-35-sample",
  prompt= to_pass,
  temperature=1,
  max_tokens=100,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
 
# text_value = response.get('text')
# print(text_value)

print(response)





   
