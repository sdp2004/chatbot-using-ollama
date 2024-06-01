
import getpass

from langchain_openai import AzureOpenAI
import os




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
        {"role": "user", "content": "What is the name of a Country starts with A? "},
        {"role": "assistant", "content": "There are so many countries like that. One of them is Afghanistan."},
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
db.run("SELECT * FROM countrydataset WHERE 'Country_Name' LIKE 'A%';")
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import AzureOpenAI
import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import AzureChatOpenAI
from langchain.agents.agent_types import AgentType


llm = AzureChatOpenAI(model="chatbotai",api_version="2024-02-01", azure_endpoint = os.getenv("OPENAI_ENDPOINT"),temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm,toolkit=toolkit,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,handle_parsing_errors=True)
agent_executor.invoke({"input": "what are the country names starting with A"})
