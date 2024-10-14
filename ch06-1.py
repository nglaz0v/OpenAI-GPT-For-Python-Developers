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

response = openai.Edit.create(
   model="text-davinci-edit-001",
   instruction="Explain the following Golang code:",
   input="""
package main

import (
   "io/ioutil"
   "log"
   "net/http"
)

func main() {
  resp, err := http.Get("https://website.com")
  if err != nil {
    log.Fatalln(err)
  }
	
  body, err := ioutil.ReadAll(resp.Body)
  if err != nil {
    log.Fatalln(err)
  }

  sb := string(body)
  log.Printf(sb)
}	
  """
	
)

print(response['choices'][0]['text'])
