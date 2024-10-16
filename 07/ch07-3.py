import os
import openai


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


init_api()

prompt = """
Input: List all the files in the current directory
Output: ls -l

Input: List all the files in the current directory, including hidden files
Output: ls -la

Input: Delete all the files in the current directory
Output: rm *

Input: Count the number of occurrences of the word "sun" in the file "test.txt"
Output: grep -o "sun" test.txt | wc -l
Input:{}
Output:
"""

result = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt.format("Count the number of files in the current directory"),
    max_tokens=200,
    temperature=0,
)

print(result.choices[0]["text"].strip())
