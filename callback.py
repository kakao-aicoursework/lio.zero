from dto import ChatbotRequest
import requests
import json
import logging
import openai

chatdata = open("./data/project_data_카카오싱크.txt", 'r').read().strip()
openai.api_key = open("./apikey.txt", 'r').read().strip()
SYSTEM_MSG = f'''
            # You are a chatbot that answers information/usage about '카카오톡싱크'.
            # Your user is korean. So answer question in korean.
            # Information about '카카오톡싱크' is given below
            # answer should be less then 200 letters
            {chatdata}
            '''
logger = logging.getLogger("Callback")


def callback_handler(request: ChatbotRequest) -> dict:

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": request.userRequest.utterance},
        ],
        temperature=0,
    )

    output_text = response.choices[0].message.content

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

    response = requests.post(url=url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
