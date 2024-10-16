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

prompt = """Input: Bitcoin
Output:
BTC was created in 2008, you can learn more about it here: https://bitcoin.org/en/ and get the latest price here: https://www.coingecko.com/en/coins/bitcoin.\
It's all-time high is $64,895.00 and it's all-time low is $67.81.

Input: Ethereum
Output:
ETH was created in 2015, you can learn more about it here: https://ethereum.org/en/\
and get the latest price here: https://www.coingecko.com/en/coins/ethereum
It's all-time high is $4,379.00 and it's all-time low is $0.43.

Input: Dogecoin
Output:
DOGE was created in 2013, you can learn more about it here: https://dogecoin.com/ and get the latest price here: https://www.coingecko.com/en/coins/dogecoin\
It's all-time high is $0.73 and it's all-time low is $0.000002.

Input: Cardano
Output:\n"""

result = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    max_tokens=200,
    temperature=0,
)

print(result.choices[0]["text"].strip())
