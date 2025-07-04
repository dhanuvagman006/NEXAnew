import os
from groq import Groq

# It's recommended to use an environment variable for your API key.
# Make sure you have set the GROQ_API_KEY environment variable.
api_key ="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"
if not api_key:
    raise ValueError("The GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)
completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/LPU-v1-die.jpg"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)
print(completion)
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
