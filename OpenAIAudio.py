from openai import OpenAI

def initialize():
    with open("keys.txt", "r") as file:
        chatgpt_api_key = file.read().strip("\n")
        client = OpenAI(api_key=chatgpt_api_key)
    return client


temp_write_file = "TempTranscript.txt"

def get_input():
    audio_file= open("EarthScienceAudio.mp3", "rb")
    return audio_file

def audioTranscription(a_file, client):
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=a_file,
    response_format="text"
    )

    f = open(temp_write_file, "w")
    f.write(transcript)
    f.close()

    return transcript

if __name__ == "__main__":
    client = initialize()
    system_prompt = "Summarize content you are provided with for a second-grade student."
    audio_file = get_input()

    output = audioTranscription(audio_file) 

    print(output.choices[0].message.content)
    print(output.usage)
