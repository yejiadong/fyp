import os
import json
import openai

# Configure OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def analyze_claim_and_evidence(request):
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
            "content": "You are an knowledgeable AI language model that can analyze claims and evidences, and provide information about whether the evidence supports, refutes, or does not have enough information on the claim."
        },
        {
            "role": "user",
            "content": f"You are provided with a claim and evidence sentence, each of which is a string of text. Perform text classification to determine whether the evidence might support, refute, or not have enough information on the claim. Ignore irrelevant elements of the evidence when making judgments about both the temporal and general aspects of the evidence. When making temporal judgments, consider only explicit temporal references in the evidence and do not infer any additional temporal information from other parts of the text. Only base your decisions on the information explicitly stated in the claim and evidence. Do not assume any information that is not provided. Please return the following information in JSON format: * SAME_ENTITY_LABEL: A boolean value indicating whether the main subject of the claim and evidence refer to the same entity. An entity can be a person, place, or thing. If the claim and evidence refer to the same entity, even if there are coreferences that make it unclear, the SAME_ENTITY_LABEL should be true. * SAME_ENTITY_JUSTIFICATION: A brief justification for your SAME_ENTITY_LABEL. * GENERAL_FACTS_LABEL: Either 'SUPPORTS', 'REFUTES', or 'NOT ENOUGH INFO' indicating whether the the non-temporal information in the evidence supports, refutes, or has not enough information to address the claim. If the entire evidence is irrelevant to the claim, does not address all key aspects of the claim or does not provide any information related to the claim then the returned label should be 'NOT ENOUGH INFORMATION'. If the evidence directly contradicts any key aspect of the claim, the returned label should be “REFUTES”. Do not make assumptions. * GENERAL_FACTS_JUSTIFICATION: An explanation of which part of the evidence supports, refutes, or provides insufficient information for the claim in terms of non-temporal information. If the evidence does not address all aspects of the claim, mention that fact and provide an explanation for why the evidence is insufficient. * TIME_LABEL: Either 'SUPPORTS', 'REFUTES', or 'NOT ENOUGH INFO' indicating whether the date or time information (including exact years) in the evidence exactly matches the date or time stated in the claim, ignoring general facts and any irrelevant information in the evidence. If the entire evidence is irrelevant to the claim or does not provide any information related to the claim's time, date or duration, then the returned label should be 'NOT ENOUGH INFORMATION'. Do not make assumptions. * TIME_JUSTIFICATION: An explanation for the TIME_LABEL decision. * TOPIC: The most likely topic that the claim and evidence is referring to. If the claim and evidence are referring to entirely different topics, then return both topics separately. * CLAIM_TEMPORAL: Extract all temporal phrases that are present in the exact phrase of the claim, including phrases that imply a specific time duration, year-based phrases and adverbs or phrases that imply a duration or time period. Temporal phrases can be time, date, or duration. Return a list of strings. Note that each string in the list should be an exact phrase taken directly from the claim. * EVIDENCE_TEMPORAL: Extract all temporal phrases that are present in the exact phrase of the evidence, including phrases that imply a specific time duration, year-based phrases and adverbs or phrases that imply a duration or time period. Temporal phrases can be time, date, duration, or other phrases that convey a specific point in time or time interval. Return a list of strings. Note that each string in the list should be an exact phrase taken directly from the evidence. * RELEVANT_EVIDENCE: Extract all relevant phrases from the evidence that exactly match any portion of the claim or are semantically similar to any portion of the claim. Relevant parts should be any phrases from the evidence that have the same meaning or convey similar information as the claim or any phrases in the evidence that refer to the same entity as mentioned in the claim, even if they are not exact matches. Return a list of strings. Note that each string in the list must be an exact phrase or sentence taken directly from the evidence. Claim: {request_json['claim']} Evidence: {request_json['evidence']}"
        }
    ]

    # Make the API request
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        max_tokens=1024,
        n=2,
        temperature=0.5,
    )

    # Parse the response and extract the relevant output
    output = response['choices'][0]['message']['content']
    # Assume that `output` is the JSON string returned by the API
    output_dict = json.loads(output)

    # Extract the relevant fields using dictionary keys
    same_entity_label = output_dict["SAME_ENTITY_LABEL"]
    same_entity_justification = output_dict["SAME_ENTITY_JUSTIFICATION"]
    general_facts_label = output_dict["GENERAL_FACTS_LABEL"]
    general_facts_justification = output_dict["GENERAL_FACTS_JUSTIFICATION"]
    time_label = output_dict["TIME_LABEL"]
    time_justification = output_dict["TIME_JUSTIFICATION"]
    topic = output_dict["TOPIC"]
    claim_temporal = output_dict["CLAIM_TEMPORAL"]
    evidence_temporal = output_dict["EVIDENCE_TEMPORAL"]
    relevant_evidence = output_dict["RELEVANT_EVIDENCE"]


    # Construct the output JSON object
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

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    return final_output, 200, headers
