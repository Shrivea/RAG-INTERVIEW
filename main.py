import pandas as pd
import tensorflow as tf
import numpy as np      
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
import time
import datetime
import json
import requests
import urllib.request
import urllib.parse
import urllib.error

import torch
import langchain
from openai import OpenAI
#we want to build the openai chat comletion casll
from dotenv import load_dotenv
load_dotenv()
import os                           
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def get_openai_vector_embeddings(email_body, subject):
    response = client.embeddings.create(
        input="",
        model="text-embedding-3-small"  # or "text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()  # Return the content of the response message
if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"
    response = generate_response(prompt)
    #emb = get_openai_vector_embeddings()
    print("Response:", response)
    print("Vector Embedding:", emb)