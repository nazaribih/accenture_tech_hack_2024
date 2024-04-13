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

text_value = response.get('text')
print(text_value)