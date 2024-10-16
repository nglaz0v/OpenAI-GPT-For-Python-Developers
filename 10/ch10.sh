
export OPENAI_API_KEY="<OPENAI_API_KEY>"

openai tools fine_tunes.prepare_data -f data.json

openai api fine_tunes.create -t "data_prepared.jsonl" -m curie
openai api fine_tunes.create -t "data_prepared.jsonl" -m <engine> --suffix "my_model_name"
openai api fine_tunes.create -t train_data.jsonl -v validation_data.jsonl -m <engine>

openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>

openai api fine_tunes.list

export FINE_TUNED_MODEL="<FINE_TUNED_MODEL>"
openai api completions.create -m $FINE_TUNED_MODEL -p <YOUR_PROMPT>

curl https://api.openai.com/v1/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"prompt": YOUR_PROMPT, "model": FINE_TUNED_MODEL}'

openai api fine_tunes.results -i <YOUR_FINE_TUNE_JOB_ID>

openai api models.delete -i <FINE_TUNED_MODEL>
curl -X "DELETE" https://api.openai.com/v1/models/<FINE_TUNED_MODEL> -H "Authorization: Bearer $OPENAI_API_KEY"
