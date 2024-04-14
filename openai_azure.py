db_schema = ""
user_query = ""

import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_base = "https://openaihackaton2024.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.completions.create(
  model="gpt-35-turbo",
  prompt="# Write an SQL query to access data from the database. Natural language should be transformed in it. \
  The database structure is the following:\n" + db_schema + ".\n The natural language you should \
  convert into a SQL query is: \n" + user_query,
  temperature=0.2,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["#"])


generated_text = response.choices[0].text.strip()
print(generated_text)

