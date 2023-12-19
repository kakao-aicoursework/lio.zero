import os

from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from dto import ChatbotRequest
import requests
import json
import logging
import openai
import vector_db

chatdata = open("./data/project_data_카카오싱크.txt", 'r').read().strip()
openai.api_key = open("./apikey.txt", 'r').read().strip()
os.environ["OPENAI_API_KEY"] = openai.api_key
TEMPLATE = """
# You are a chatbot that answers information/usage about '카카오싱크'.
# Your user is korean. So answer question in korean.
# Information about '카카오싱크' is given below
# answer should be less then 200 letters
```
{context}
```
Q: {question}
A: 
"""
logger = logging.getLogger("Callback")
vector_db = vector_db.VectorDb()


def query_to_langchain(query):
    model = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
    prompt = PromptTemplate(
        template=TEMPLATE,
        input_variables=['context', 'question']
    )
    # 아래 링크 참조
    # https://api.python.langchain.com/en/latest/chains/langchain.chains.combine_documents.base.BaseCombineDocumentsChain.html
    langchain = load_qa_chain(model, chain_type="stuff", prompt=prompt, verbose=True)
    data = vector_db.query(query)
    return langchain.run(input_documents=data, question=query)


def callback_handler(request: ChatbotRequest) -> dict:

    response = query_to_langchain(request.userRequest.utterance)

    output_text = response
    logger.log(0, "answer created : " + response)

    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }

    url = request.userRequest.callbackUrl

    requests.post(url=url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
