import os
import PyPDF2
import fulltext
import chardet
from groq import Groq
import time

# parse command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

def pdf_to_text(pdf_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

if args.filename.endswith(".pdf"):
    text = pdf_to_text(args.filename)
else:    
    with open(args.filename, 'rb') as f:
        result = chardet.detect(f.read())
        charenc = result['encoding']
        if charenc == 'utf-8' and not(args.filename.endswith(".txt")):
            with open(args.filename) as f:
                text = fulltext.get(f)
        else:
            with open(args.filename, 'r', encoding=charenc) as f:
                text = f.read()


while len(text) > 20000:
    textList = text.split('\n')
    tempList = [textList[0]]
    wordCounter = len(textList[0])
    for i in range(1, len(textList)):
        length = len(textList[i])
        if wordCounter + length < 20000:
            tempList[-1] += "\n" + textList[i]
            wordCounter += length
        else:
            tempList.append(textList[i])
            wordCounter = length
    textList = tempList
    newText = ""
    for paragraph in textList:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': 'Summarize the input text below. Output in English.',
                },
                {
                    "role": "user",
                    "content": paragraph,
                }
            ],
            model="llama3-8b-8192",
        )
        newText += chat_completion.choices[0].message.content + "\n\n"
    text = newText

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': 'Summarize the input text below. Output in English.',
        },
        {
            "role": "user",
            "content": text,
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)

    
