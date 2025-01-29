# FAQ Chatbot with OpenAI and Fuzzy Search

This project implements an FAQ chatbot using OpenAI's API to generate answers for questions not found in predefined FAQ data. The chatbot also uses fuzzy string matching to provide answers to similar questions in case of slight variations in the input.

## Features

- **FAQ Database**: FAQ data is stored in a text file (`faq_data.txt`) with questions and answers separated by a pipe (`|`).
- **Fuzzy Matching**: The application uses the `fuzzywuzzy` library to match user queries with existing FAQ questions, even if they are not an exact match.
- **AI-generated Answers**: If no satisfactory match is found in the FAQ data, OpenAI's GPT-3.5 model is used to generate an answer based on the provided FAQ data.
- **Logging**: User queries and their corresponding answers are logged to a file (`user_queries.txt`).

## Requirements

- Python 3.x
- Flask
- OpenAI Python client
- FuzzyWuzzy (with Python-Levenshtein)
- Ensure you have your OpenAI API key set in your environment variables as `OPENAI_API_KEY`.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/PiyushVedwal7/faq.git
   cd faq
