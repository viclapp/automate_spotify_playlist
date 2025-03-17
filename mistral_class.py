#Import class 
import os
from mistralai import Mistral
import json
from prompt import prompt

class MistralAgent:

    def __init__(self, prompt, api_key, model="mistral-tiny"):
        self.prompt = prompt
        self.api_key = api_key
        self.model = model

    def ask_le_chat(self):
        model = self.model
        client = Mistral(api_key=self.api_key)
        chat_res = client.chat.complete(
            model=model,
            messages=[
                {
                    "role":"user",
                    "content":self.prompt
                }
            ]
        )
        try:
            chat_res = chat_res.json()
            chat_res_json = json.loads(chat_res)
            res = chat_res_json['choices'][0]['message']['content']
            start_index = res.find('[')
            end_index = res.find(']')
            res_json = res[start_index:end_index+1].strip()
            res_json = json.loads(res_json)
            return res_json
        except ValueError:
            print("JSON format is not valid")