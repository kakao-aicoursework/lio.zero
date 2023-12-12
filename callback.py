from dto import ChatbotRequest
import aiohttp
import logging
import openai

chatdata = open("./data/project_data_카카오싱크.txt", 'r').read().strip()
openai.api_key = open("./apikey.txt", 'r').read().strip()
SYSTEM_MSG = f'''
            # You are a chatbot that answers information/usage about '카카오톡싱크'.
            # Your user is korean. So answer question in korean.
            # Information about '카카오톡싱크' is given below
            {chatdata}
            '''
logger = logging.getLogger("Callback")

async def callback_handler(request: ChatbotRequest) -> dict:

    # ===================== start =================================
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": request.userRequest.utterance},
        ],
        temperature=0,
    )
    # focus
    print(response.choices[0].message.content)
    output_text = response.choices[0].message.content

   # 참고링크 통해 payload 구조 확인 가능
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
    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

    # time.sleep(1.0)
    print(request.userRequest.callbackUrl)
    url = request.userRequest.callbackUrl

    if url:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=payload, ssl=False) as resp:
                await resp.json()
