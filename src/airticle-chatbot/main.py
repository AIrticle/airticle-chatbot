import os
from dotenv import load_dotenv
from google import genai
import pickle

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

NOTES_FILES_DIR = "./mock_database/notes"
OUTPUT_MODELS_FILES_DIR = "./mock_database/models"

def create_article_models():
    client = genai.Client(api_key=GEMINI_API_KEY)

    for file in os.listdir(NOTES_FILES_DIR):
        file_contents = ""
        
        with open(os.path.join(NOTES_FILES_DIR, file), "r") as f:
            for line in f:
                file_contents += line
        chat = client.chats.create(model="gemini-2.0-flash")
        chat.send_message("Here are all of the notes for an article that I am writing. Please remember them so that you can help me write the article later.\n{}".format(file_contents))
        with open(os.path.join(OUTPUT_MODELS_FILES_DIR, "{}_model_history.pkl".format(file)), 'wb') as outp:
            pickle.dump(chat._curated_history, outp, pickle.HIGHEST_PROTOCOL)


def query_article_models():
    client = genai.Client(api_key=GEMINI_API_KEY)

    for file in os.listdir(OUTPUT_MODELS_FILES_DIR):
        with open(os.path.join(OUTPUT_MODELS_FILES_DIR, file), 'rb') as inp:
            history = pickle.load(inp)
        chat = client.chats.create(model="gemini-2.0-flash", history=history)
        response = chat.send_message("Please generate a 100 word summary of my article.")
        print("{} Article summary:".format(os.path.basename(file)))
        print(response.text)
        print("------------------------------")

if __name__ == "__main__":
    # create_article_models()
    query_article_models()