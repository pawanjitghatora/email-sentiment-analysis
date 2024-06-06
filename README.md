# README

## Project Title

Email Sentiment Analysis using OpenAI GPT-4

## Description

This project demonstrates how to analyze the sentiment of email texts using OpenAI's GPT-4 model. The code loads email files from a specified directory, processes the email content, and uses the GPT-4 model to determine the sentiment of each email. The analysis includes identifying the overall sentiment (positive, negative, neutral), sentiment explanation and checking for any offensive content. You can change the behavior as per your need by updating the "prompt" in the code.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/pawanjitghatora/email-sentiment-analysis.git
   ```

2. Navigate to the project directory:
   ```sh
   cd \your-directory\email-sentiment-analysis
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

1. Ensure your `.env` file contains the correct OpenAI API key.
2. Place your `.eml` email files in a directory i.e. `emails/`.
3. Run the script:
   ```sh
   python email-sentiment-analysis.py
   ```
4. The script will read each email from the specified directory, analyze its sentiment using GPT-4, and print the results.

### Example

```sh
python email-sentiment-analysis.py
```

Output:
```
##########################################
Email: example.eml, Sentiment: Positive
...

##########################################
Email: another_example.eml, Sentiment: Neutral
...
```

## Code Explanation

### Importing Necessary Libraries

The script imports essential libraries for handling environment variables, email processing, and interfacing with the OpenAI API:

```python
import os
import email
import email.policy
import openai
from dotenv import load_dotenv
```

### Loading Environment Variables

The `.env` file is loaded to fetch the OpenAI API key:

```python
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
```

### Preprocessing Email Text

A basic preprocessing function to clean up the email text:

```python
def preprocess_email(email_text):
    return email_text.strip().lower()
```

### Analyzing Sentiment

The main function to analyze the sentiment of the email text using OpenAI GPT-4:

```python
def analyze_sentiment(email_text):
    processed_text = preprocess_email(email_text)
    prompt = (
        f"Analyze the following email text:\n\n{processed_text}\n\n"
        "Then answer these questions:\n"
        "- What is the sentiment of the text? (Positive, Negative, Neutral)\n"
        "- Analyze the sentiment of the text in more detail.\n"
        "- Does the text contain any offensive content? (Yes/No)"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": processed_text}]
    )
    
    if response.choices:
        return response.choices[0].message['content'].strip()
    else:
        return "Sentiment analysis failed"
```

**You can update "prompt" in the code as per your requirements.**

### Parsing Email Files

Function to parse email content from `.eml` files:

```python
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
```

### Reading and Analyzing Emails

Function to read emails from a directory and analyze their sentiment:

```python
def read_and_analyze_emails_from_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".eml"):
            file_path = os.path.join(directory_path, filename)
            email_text = parse_email_from_file(file_path)
            sentiment = analyze_sentiment(email_text)
            print("##########################################")
            print(f"Email: {filename}, Sentiment: {sentiment}")
            print("\n")
```

### Running the Script

Specify the directory containing `.eml` files and call the function:

```python
directory_path = 'emails/'
read_and_analyze_emails_from_directory(directory_path)
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
