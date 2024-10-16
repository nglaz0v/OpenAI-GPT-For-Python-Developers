
openai tools fine_tunes.prepare_data -f drug_malady_data.json

export OPENAI_API_KEY="<OPENAI_API_KEY>"
openai api fine_tunes.create \
    -t "drug_malady_data_prepaired_train.jsonl" \
    -v "drug_malady_data_prepaired_valid.jsonl" \
    --compute_classification_metrics \
    --classification_n_classes 3 \
    -m ada \
    --suffix "drug_malady_data"

# openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>

openai api completions.create -m <MODEL_ID> -p <YOUR_PROMPT>
