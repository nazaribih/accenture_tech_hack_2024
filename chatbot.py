import streamlit as st
import pyodbc
import os
import openai
from dotenv import load_dotenv
import re
import pandas as pd
load_dotenv()

server = 'hackaton-gr10-sqlserverskfpe.database.windows.net'
database = 'hackaton-gr10-sqldb'
username = 'hacksqlusr012993'
password = 'hacksqlusrP@ssw00rd'
driver = '{ODBC Driver 18 for SQL Server}'
# Construct the connection string
conn_str = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

def extract_query(text):
    # Find the substring between 'SELECT' and ';'
    match = re.search(r'SELECT.*?;', text, re.DOTALL)
    if match:
        query = match.group(0)
        # Replace '\n' with ' '
        query = query.replace('\n', ' ')
        return query
    else:
        return None

# Title for your chatbot
st.title("Chat about your data")

# Function to generate bot response
def get_bot_response(user_input):
    # You can replace this with your actual chatbot logic
    # For simplicity, I'm just echoing back what the user inputs
    st.subheader("Your data:")

    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()

    # Get the list of table names without schema prefixes
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    table_names = [row[0] for row in cursor.fetchall()]

    # Get the schema information for each table
    schema_string = ""
    for table_name in table_names:
        if (table_name != 'ErrorLog' and table_name != 'BuildVersion'):
            schema_string += f"Table: '[SalesLT].[" + table_name + "]'\n"
        else:
            schema_string += f"Table: '[dbo].[" + table_name + "]'\n"
        cursor.execute(
            f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = cursor.fetchall()
        for column_name, data_type in columns:
            schema_string += f"  - {column_name}: {data_type}\n"

    # OpenAI connection - get the query

    openai.api_type = "azure"
    openai.api_base = "https://openaihackaton2024.openai.azure.com/"
    openai.api_version = "2023-09-15-preview"
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.completions.create(
        model="gpt-35-turbo",
        prompt="# Write an SQL query to access data from the database. Natural language should be transformed in it. \
      The database structure is the following (each table name is given in between single quotation marks. Note, it is very important to use all symbols between single quotation marks as a table name:\n" + schema_string + ".\n The natural language you should \
      convert into a SQL query is: \n" + user_input + "\n Give your answer as a code snippet. Be sure to put a semicolon at the end",
        temperature=0.2,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["#"])

    generated_text = response.choices[0].text.strip()
    query = extract_query(generated_text)
    print(query)

    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    df = pd.DataFrame.from_records(rows, columns=[col[0] for col in cursor.description])
    st.write(df)

    connection.close()
    return query



# Text input box for user to enter messages
user_input = st.text_input("Enter your request here:")

# Button to submit user input
submit_button = st.button("Send")

# Display bot response when user clicks submit
if submit_button:
    bot_response = get_bot_response(user_input)
    st.text_area("SQL query for the request:", value=bot_response, height=100)