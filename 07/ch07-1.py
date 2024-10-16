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

prompt = "The first programming language to be invented was Plankalkül, which was de\
signed by Konrad Zuse in the 1940s, but not publicly known until 1972 (and not imple\
mented until 1998). The first widely known and successful high-level programming l\
anguage was Fortran, developed from 1954 to 1957 by a team of IBM researchers led \
by John Backus. The success of FORTRAN led to the formation of a committee of scie\
ntists to develop a universal computer language; the result of their effort was AL\
GOL 58. Separately, John McCarthy of MIT developed Lisp, the first language with o\
rigins in academia to be successful. With the success of these initial efforts, prog\
ramming languages became an active topic of research in the 1960s and beyond\n\nTweet with hashtags:"

english_tweet = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.5,
    max_tokens=20,
)

english_tweet_text = english_tweet["choices"][0]["text"].strip()
print("English Tweet:")
print(english_tweet_text)

spanish_tweet = openai.Edit.create(
    model="text-davinci-edit-001",
    input=english_tweet_text,
    instruction="Translate to Spanish",
    temperature=0.5,
)

spanish_tweet_text = spanish_tweet["choices"][0]["text"].strip()
print("Spanish Tweet:")
print(spanish_tweet_text)

###

prompt = "Determine the part of speech of the word 'light'.\n\n"

result = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    max_tokens=20,
    temperature=1,
)
print(result.choices[0]["text"].strip())

###

prompt_a = "The light is red. Determine the part of speech of the word 'light'.\n\n"
prompt_b = "This desk is very light. Determine the part of speech of the word'light'.\n\n"
prompt_c = "You light up my life. Determine the part of speech of the word 'light'\n\n"

for prompt in [prompt_a, prompt_b, prompt_c]:
    result = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=20,
        temperature=0,
    )

    print(result.choices[0]["text"].strip())

###

prompt = "Huawei:\ncompany\n\nGoogle:\ncompany\n\nMicrosoft:\ncompany\n\nApple:\n"
prompt = "Huawei:\ncompany\n\nGoogle:\ncompany\n\nMicrosoft:\ncompany\n\nApricot:\nF\ruit\n\nApple:\n"

result = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    max_tokens=20,
    temperature=0,
    stop=["\n", " "],
)

print(result.choices[0]["text"].strip())
