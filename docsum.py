import os
import fulltext
from groq import Groq

# parse command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

with open(args.filename) as f:
    # text = f.read()
    text = fulltext.get(f)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': 'Summarize the input text below.',
        },
        {
            "role": "user",
            "content": text,
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)
