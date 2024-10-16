from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
generator("Hello, I'm a language model", max_length=30, num_return_sequences=3)
## [{'generated_text': "Hello, I'm a language modeler. So while writing this, when I went out to meet my wife or come home she told me that my"},
## {'generated_text': "Hello, I'm a language modeler. I write and maintain software in Python. I love to code, and that includes coding things that require writing"}, {...}]
