import os 
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()




# simple chat service
model = ChatOpenAI(model='gpt-4o-mini')
prompt = ChatPromptTemplate.from_template(
    "You can joke and talk to the user this is the user question\n: {question}"
    )
chain = prompt | model | StrOutputParser()

