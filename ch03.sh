#!/bin/bash -x

source .env

curl https://api.openai.com/v1/models \
    -H 'Authorization: Bearer '$API_KEY'' \
    -H 'OpenAI-Organization: '$ORG_ID''

curl https://api.openai.com/v1/models \
    -H 'Authorization: Bearer xxxx' \
    -H 'OpenAI-Organization: xxxx'

curl https://api.openai.com/v1/models -H 'Authorization: Bearer xxxx'
