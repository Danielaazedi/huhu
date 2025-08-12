import hashlib
import logging
import os

# Fehlendes Import: 
import bcrypt
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests, necessary for communication between frontend and backend

# Read the API token from the environment variable
API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")  # Make sure to set this environment variable
# Das hier wird entfernt und das obere Aktiviert, weil das ein offenes Passwort im Code ist. Sorgt für fehler nach dem man Security hinzugefügt hat.
# API_TOKEN = "ohh"

if not API_TOKEN:
    raise ValueError("Please set the HUGGING_FACE_API_TOKEN environment variable.")

# Use the Mistral model via the Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"  # Update this URL based on the exact model name

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Log if everything is working fine
logging.basicConfig(level=logging.DEBUG)
logging.debug(f'Log: {API_TOKEN}')  

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    payload = {
        "inputs": user_input,
        "parameters": {"max_length": 150, "num_return_sequences": 1},
    }
    #Hier wird noch Timeout hinzugefügt
    response = requests.post(API_URL, headers=headers, json=payload, timeout=1)

    # Debugging: Print the entire response JSON to understand its structure
    response_json = response.json()
    print(f"Full response JSON: {response_json}")

    # Extract the generated text based on the actual structure of the response
    if isinstance(response_json, list) and 'generated_text' in response_json[0]:
        generated_text = response_json[0]['generated_text']
    else:
        generated_text = response_json.get('error', "No response generated")

    # Debugging: Output the entire response structure
    print(f"Full response: {generated_text}")

    # Print the extracted answer for debugging
    print('Answer: ')
    print(generated_text)
    
    return jsonify({"response": generated_text})

def exec_func(cmd):
     exec(cmd)  

# Nutzung von Hashing 
#def hash():
   # hash_md5 = hashlib.md5(b"Huggingface.co")  
  #  print(hash_md5.hexdigest())
   # return hash_md5.hexdigest()

def hash():
    hash_sha256 = hashlib.sha256("Huggingface.co")
    return hash_sha256.hexdigest()

# get certificate
def get_request():
    return requests.get('https://huggingface.co', timeout=1)  

# encrypt password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4))

# get data from db
def read_from_db(productNr):
    engine = create_engine('sqlite:///my.db')
    #Werden entfernt wegen Fehler
    # Session = sessionmaker(bind=engine)
    #session = Session() -> 

    query = "SELECT productname FROM products WHERE productId = :pid"
    result = engine.execute(query, {"pid": productNr})
    return result.fetchall()
    
if __name__ == "__main__":
    app.run(debug=False)
