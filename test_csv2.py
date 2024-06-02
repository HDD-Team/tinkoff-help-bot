import json

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from parser import get_data
from template import template2
from convertizator import vectorstore

import os

from dotenv import load_dotenv
import re
import time

load_dotenv("api.env")

proxy_login = os.getenv('PROXY_LOGIN')
proxy_password = os.getenv('PROXY_PASS')

original_http_proxy = os.environ.get('HTTP_PROXY')
original_https_proxy = os.environ.get('HTTPS_PROXY')

os.environ['HTTP_PROXY'] = f'http://{proxy_login}:{proxy_password}@186.65.123.153:8000'
os.environ['HTTPS_PROXY'] = f'http://{proxy_login}:{proxy_password}@186.65.123.153:8000'

name, embeddings_model = vectorstore()
db = FAISS.load_local(name, embeddings_model, allow_dangerous_deserialization=True)
prompt = ChatPromptTemplate.from_template(template2)
retriever = db.as_retriever()

secret_key = os.getenv('OPEN_API_KEY')
prompt = PromptTemplate.from_template(template2)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=secret_key,
)
llm_2 = ChatOllama(model="mistral", format="json", temperature=0)


def model_query(question):
    question = question
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    result = chain.invoke(question)

    print(result)
    return result


os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)


def output_api(question):
    start = time.time()
    output = model_query(question)
    llm = llm_2
    messages = [
        HumanMessage(
            content=f"""You are a bank assistant bote. Make an simple very short answer on Russian language for user question: {question} based on provided information: {get_data(output)}"""
        )
    ]
    chat_model_response = llm.invoke(messages)
    print(str(chat_model_response))
    json_match = re.search(r"content='({.*?})'\s*response_metadata", str(chat_model_response), re.DOTALL)
    print('NORMALIZE TEXT TO ANSWER')
    if json_match:
        json_str = json_match.group(1)
        print(f"Extracted JSON string: {json_str}")
        json_str = json_str.replace("\\n", "\n").replace("\\'", "'")
        try:
            json_data = json.loads(json_str)
            # Объединение всех значений в одну строку
            combined_text = " ".join(json_data.values())
            print('done')
            print(combined_text)
            stop = time.time()
            all_time = stop - start
            print(all_time)
            return (output, combined_text)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Problematic JSON string: {json_str}")
    else:
        print('ERRRRROOOOOORRRRRRR!')
