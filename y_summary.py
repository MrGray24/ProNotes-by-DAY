from openai import OpenAI

def initialize():
    with open("keys.txt", "r") as file:
        chatgpt_api_key = file.read().strip("\n")
        client = OpenAI(api_key=chatgpt_api_key)
    return client

def get_input():
    with open("y_input.txt", "r") as file:
        input_text = file.read()
    return input_text

def summarize(client, system_prompt: str, input_text: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=0.7,
        max_tokens=1000,
        top_p=1
    )
    return (response.choices[0].message.content, response.usage)


if __name__ == "__main__":
    client = initialize()
    #system_prompt = "Summarize content you are provided with for a second-grade student."
    system_prompt = "Summarize the content you are pr ovided into point form with the most important ideas"
    input_text = get_input()

    output = summarize(client, system_prompt, input_text)

    print(output.choices[0].message.content)
    print(output.usage)
