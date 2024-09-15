import os
import PyPDF2
import fulltext
import chardet
from groq import Groq


def pdf_to_text(pdf_path):
    '''
    Read a pdf file into text
    '''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def text_split(text, sizeLimit):
    '''
    Split the input text according to line break, and reorganize the sentences
    into paragraph with in sizeLimit to reduce the number of requests
    >>> text_split("AAB\nDGF", 4)
        ["AAB", "DGF"]
    >>> text_split("AAB\nDGF", 10)
        ["AAB\nDGF"]
    '''
    textList = text.split('\n')
    tempList = [textList[0]]
    wordCounter = len(textList[0])
    for i in range(1, len(textList)):
        length = len(textList[i])
        if wordCounter + length < sizeLimit:
            tempList[-1] += "\n" + textList[i]
            wordCounter += length
        else:
            tempList.append(textList[i])
            wordCounter = length
    return tempList


def recursive_summary(text, sizeLimit):
    '''
    Split the whole text to smaller sizes and use LLM to summary to get shorter
    result. Repeating until the whole length is with in the sizeLimit
    '''
    while len(text) > sizeLimit:
        textList = text_split(text, sizeLimit)
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
    return text


if __name__ == "__main__":
    # parse command line args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Open the input file
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

    # Using recursive summary if needed
    text = recursive_summary(text, 20000)

    # Summary result
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'Summarize the input text below, output in English.',
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion.choices[0].message.content)