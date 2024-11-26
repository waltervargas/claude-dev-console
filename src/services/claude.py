import os
import anthropic

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def call_claude_sonnet_3_5(system, prompt, assistant, max_tokens=8192, temperature=0, top_p=1, frequency_penalty=0, presence_penalty=0):
    """
    Calls the Claude Sonnet 3.5 model with the given system, prompt, and assistant messages.
    
    Parameters:
    system (str): The system prompt for the Claude model.
    prompt (str): The user prompt for the Claude model.
    assistant (str): The assistant's previous response.
    max_tokens (int): The maximum number of tokens to generate (default 8192).
    temperature (float): The temperature parameter for the model (default 0).
    top_p (float): The top-p parameter for the model (default 1).
    frequency_penalty (float): The frequency penalty parameter for the model (default 0).
    presence_penalty (float): The presence penalty parameter for the model (default 0).
    
    Returns:
    str: The generated response from the Claude Sonnet 3.5 model.
    """
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    response = client.message.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": assistant
                    }
                ]
            }
        ]
    )

    return response.choices[0].text.strip()
