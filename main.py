
import getpass

from azure.identity import ChainedTokenCredential, ManagedIdentityCredential, AzureCliCredential
from langchain_openai import AzureOpenAI
import os
from azure.identity import DefaultAzureCredential



#Note: The openai-python library support for Azure OpenAI is in preview.
import os


from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("OPENAI_ENDPOINT"), 
  api_key=os.getenv("OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="chatbotai", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi, How can i help you?"},
          ]
)

from click import prompt
import pandas as pd

df = pd.read_csv("countrydataset.csv")
print(df.shape)
print(df.columns.tolist())
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

engine = create_engine("sqlite:///countrydataset.db")
#df.to_sql("countrydataset", engine, index=False)
db = SQLDatabase(engine=engine)
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM countrydataset WHERE Country_Name LIKE 'A%';")
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import AzureOpenAI
import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import AzureChatOpenAI



llm = AzureChatOpenAI(model="chatbotai",api_version="2024-02-01", azure_endpoint = os.getenv("OPENAI_ENDPOINT"),temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm,toolkit=toolkit,agent_type='',verbose=False,handle_parsing_errors=True)
agent_executor.invoke({"input": "what are country names starting with A"})