import os
import json
import openai

# Configure OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def paraphrase(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    request_json = request.get_json(silent=True)

    # Set up the parameters for the API request
    model_engine = "gpt-3.5-turbo"
    messages = [
        {
            "role": "system",
            "content": "You are an AI language model that can paraphrase sentences."
        },
        {
            "role": "user",
            "content": f"Paraphrase the following sentence five times, ensuring that each paraphrase has the same meaning as the original sentence but is not identical, and that the length of each paraphrase is roughly the same. Sentence: {request_json['sentence']}"
        }
    ]

    # Make the API request
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=1024,
        n=1,
        temperature=0.6,
    )

    generated_messages = [choice.message for choice in response.choices[:5]]

    # Construct the output JSON object
    final_output = {
        "generated_texts": generated_messages,
    }

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    return final_output, 200, headers
