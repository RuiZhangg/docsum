## Docsum ![](https://github.com/RuiZhangg/docsum/workflows/tests/badge.svg)
This project uses GROQ's API to summarize input text file.

To use this file, get your GROQ_API_KEY and add it to your environment, then run 
```{bash}
python3 docsum.py {file path}
```
For example, 
```{bash}
python3 docsum_split.py docs/declaration
The text is the United States Declaration of Independence, adopted by the Continental Congress on July 4, 1776. It declares the 13 American colonies' independence from Great Britain and establishes the United States of America as a sovereign nation. ......
```
