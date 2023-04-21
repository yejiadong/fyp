
# GPT Metrics / Use (Prompt-Tuned)

In this file, we attempt to construct some metrics for the prompt-tuned GPT 3.5 model. 

Hence, there is code that will access the Open AI backend to pull predictions for supplied data. 

Take note that you will need a Google Cloud Run function / any backend that can invoke the Open AI's API. You can then change the link here in this portion:
`response = requests.post("[ADDRESS_TO_CLOUD_FUNCTION]", json=payload)`

#### GPTMetrics.ipynb
- Allows you to supply ur own data to tap GPT's output
- Also calculates some metrics for the prompt-tuned GPT 3.5 model

Rest of the csv files are all either results or training files used for the GPT model.

