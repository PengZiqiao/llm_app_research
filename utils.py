
import requests
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def chat_completion(messages, 
                    model=config['model'], 
                    url=config['api_url'],
                    api_key=config['api_key']):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def chat_invoke(user_content, history=[]):
    messages = [
        *history,
        {"role": "user", "content": user_content}
    ]

    response = chat_completion(messages)
    return response["choices"][0]["message"]["content"]



from string import Template
from pathlib import Path

def template_substitute(template_name, **variables):
    template_text = Path(f'templates/{template_name}.txt').read_text()
    template=Template(template_text)
    return template.substitute(**variables)


import json
import re

def json_loads(text):
    pattern = re.compile(r'```json\n(.*)\n```', re.DOTALL)
    match = pattern.search(text)
    return json.loads(match.group(1))