
#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai


openai.api_type = "azure"
openai.api_base = "https://openaihackaton2024.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = '89652dc9313147ac8aa7e074dca1e07c'

response = openai.Completion.create(
  engine="gpt-35-sample",
  prompt="Give me a simple SQL query",
  temperature=1,
  max_tokens=100,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)