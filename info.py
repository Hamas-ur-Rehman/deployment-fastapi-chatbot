import os

import requests
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

def pdf_database(question):
    file_path = "files/pdf/"
    pdf_files = [os.path.join(file_path,f) for f in os.listdir(file_path) if f.endswith('.pdf')]

    pages = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        pages.extend(loader.load())

    vector_store = InMemoryVectorStore.from_documents(pages, OpenAIEmbeddings())
    documents = vector_store.similarity_search(question, 3)

    return " ".join([doc.page_content for doc in documents])


def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location_name)
    return (location.latitude, location.longitude) if location else (None, None)

def get_weather_data(location_name, exclude="minutely,hourly", units="metric"):
    lat, lon = get_lat_long(location_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        pretty_response = f"""Current temperature in {location_name} is {response['current']['temperature_2m']}°C.
        """
        return pretty_response
    else:
        response.raise_for_status()

