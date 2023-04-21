
# Google Cloud Function

The Google Cloud Function is needed to make API calls to the OpenAI endpoint for you to be able to obtain GPT services. 

### Prequisites
- Valid Open AI API key (that gives you access to Open AI services). This key can be obtained from Open AI's console.
- Valid Google Cloud Function service (billing and payments set up, with cloud functions enabled)


### Set-up
1. Install the Open AI API key as a secret in Google's Secret Manager. You should name the key as "OPENAI_API_KEY". Then you will be able to access this key in the Google Cloud Function)
2. Set up a Google Cloud Function for your project. (https://cloud.google.com/functions) Configure the cloud function to be unauthenticated, and also ensure that the permissions allow anyone from outside to access. Refer to https://cloud.google.com/functions/docs/securing/managing-access-iam for details on how to set up public access. Make sure the Open AI's API key is also referenced as a secret in this cloud function. All this is configured as part of the setup process.

### Creating the Google Cloud Function
- A sample cloud function code is provided for you to use to gain access to Open AI services. Make sure that the API key is already added as a secret in Google's Secret Manager and referenced in the project. 
- Open the cloud function code editor and paste the code in, together with the requirements txt file. A screenshot is added for your reference. 

    Ensure that in the POST request to the cloud function, include the following fields in the payload:
    - **claim:** the claim that needs to be compared against the evidence 
    - **evidence:** the evidence that is used to fact-check the claim

The code simply sends a specified prompt to the Open AI endpoint. It returns a json object with the following format:
```json  
    final_output = {
        "same_entity_label": same_entity_label,
        "same_entity_justification": same_entity_justification,
        "general_facts_label": general_facts_label,
        "general_facts_justification": general_facts_justification,
        "time_label": time_label,
        "time_justification": time_justification,
        "topic": topic,
        "claim_temporal": claim_temporal,
        "evidence_temporal": evidence_temporal,
        "relevant_evidence": relevant_evidence
    }
```
