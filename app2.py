import os
import openai
import click

def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

init_api()

_prompt = """
Input: List all the files in the current directory
Output: ls -l

Input: List all the files in the current directory, including hidden files
Output: ls -la

Input: Delete all the files in the current directory
Output: rm *

Input: Count the number of occurrences of the word "sun" in the file "test.txt"
Output: grep -o "sun" test.txt | wc -l

Input: {}
Output:"""

while True:
        request = input(click.style("Input", fg="green"))
        prompt = _prompt.format(request)
        result = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                temperature=0.0,
                max_tokens=100,
                stop=["\n"],
        )

        command = result.choices[0].text.strip()
        click.echo(click.style("Output: ", fg="yellow") + command)
        click.echo()