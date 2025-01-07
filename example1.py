import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage,ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from info import pdf_database, get_weather_data


@tool
def pdf_db(question):
    """
    This tool searches a database of PDFs for the best answer to a question.
    PDF is about EMR
    """
    return pdf_database(question)

@tool
def weather_data(location_name):
    """
    This tool gets the current weather data for a location.
    """
    return get_weather_data(location_name)

tools = [pdf_db,weather_data]

PROMPT = """You are a chatbot that speaks roman urdu with english words .
You will answer every question in urdu no matter what.


"""

model = ChatOpenAI(model='gpt-4o-mini').bind_tools(tools)
messages = [SystemMessage(PROMPT)]

def chatbot(question):
    messages.append(HumanMessage(question))
    response = model.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "pdf_db":
                pdf_data = pdf_db(tool_call["args"]["question"])
                messages.append(ToolMessage(pdf_data,tool_call_id = tool_call["id"] ))
            elif tool_call["name"] == "weather_data":
                weather_data_result = weather_data(tool_call["args"]["location_name"])
                messages.append(ToolMessage(weather_data_result,tool_call_id = tool_call["id"] ))
    
        response = model.invoke(messages)
        messages.append(response)
    return response.content

