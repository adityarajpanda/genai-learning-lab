from euriai.langchain import create_chat_model
# import os
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv(usecwd=True)) 

# api_key=os.environ["EURI_API_KEY"]

# temperature: closer to 0 means less hallucinations, closer to 1 means more hallucinations
# closer to 0 range is from 0 to 0.3, closer to 1 range is from 0.7 to 1
# 0.7 is the default

# def get_chat_model(model_name: str = "gpt-4", temperature: float = 0.7, api_key: str = api_key):

#     return create_chat_model(
#         model_name = model_name,
#         temperature = temperature,
#         api_key = api_key
#     )

# temperature: closer to 0 means less hallucinations, closer to 1 means more hallucinations
# closer to 0 range is from 0 to 0.3, closer to 1 range is from 0.7 to 1
# 0.7 is the default
API_KEY = None
# MODEL = "gpt-4.1-nano" # this model did not work, that's why we used gemini-2.5-flash
MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.7

def get_chat_model(api_key: str = None):
    return create_chat_model(
        api_key=api_key or API_KEY,
        model=MODEL,
        temperature=TEMPERATURE
    )

def ask_chat_model(chat_model, prompt: str):
    response = chat_model.invoke(prompt)
    return response.content 
