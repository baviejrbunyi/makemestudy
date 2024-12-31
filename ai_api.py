import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

def groq_request(prompt):
    client = Groq(
        api_key=os.getenv('API_KEY'),
    
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
                
            }
        ],
        response_format= {"type": "json_object"},
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    return json.loads(chat_completion.choices[0].message.content)
