import os
import email
import email.policy
import openai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Ensure you have set your OPENAI_API_KEY in the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def preprocess_email(email_text):
    # Basic preprocessing of email text
    return email_text.strip().lower()

def analyze_sentiment(email_text):
    processed_text = preprocess_email(email_text)
    # Crafting a more detailed prompt
    prompt = (
        f"Analyze the following email text:\n\n{processed_text}\n\n"
        "Then answer these questions:\n"
        "- What is the sentiment of the text? (Positive, Negative, Neutral)\n"
        "- Analyze the sentiment of the text in more detail.\n"
        "- Does the text contain any offensive content? (Yes/No)"
    )
    # Use the chat completion endpoint for the chat model
    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #messages=[{"role": "system", "content": "Analyze the sentiment of the following text:"},
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": processed_text}]
    )
    
    # The structure of the response object might differ from the completions endpoint
    # Extract the sentiment analysis result from the response
    if response.choices:
        return response.choices[0].message['content'].strip()
    else:
        return "Sentiment analysis failed"


def parse_email_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        msg = email.message_from_file(file, policy=email.policy.default)
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()

def read_and_analyze_emails_from_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".eml"):
            file_path = os.path.join(directory_path, filename)
            email_text = parse_email_from_file(file_path)
            #print(f"Email: {filename}, Email_Text:  , {email_text}")
            sentiment = analyze_sentiment(email_text)
            print("##########################################")
            print(f"Email: {filename}, Sentiment: {sentiment}")
            print("\n")

# Specify the path to your directory containing .eml files
#directory_path = 'path_to_your_email_directory'
directory_path = 'emails/'
read_and_analyze_emails_from_directory(directory_path)
