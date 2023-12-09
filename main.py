#python -m streamlit run main.py

import streamlit as st
from openai import OpenAI
import y_summary as summary
import OpenAIAudio as aud
from y_vision import detect_document

if 'sum_notes' not in st.session_state:
    st.session_state['sum_notes'] = None

if "transcript" not in st.session_state:
    st.session_state["transcript"] = None

if 'notes_text' not in st.session_state:
    st.session_state['notes_text'] = None
        
def summarize_audio(transcript_text: str):
    #ChatGPT instructions
    system_prompt = "The content provided is a lesson. Summarize the important ideas of the lesson into dot jots."
    output = summary.summarize(client, system_prompt, transcript_text)
    print(output[1])
    return output[0]


def transcriptAudio():
    if uploaded_audio and uploaded_audio.name.endswith('.mp3') == True:
        transcript_text = aud.audioTranscription(uploaded_audio, client)
        summarized_audio = summarize_audio(transcript_text)

        st.session_state['transcript'] = transcript_text
        st.session_state['sum_notes'] = summarized_audio
        
        return summarized_audio
    else:
        #warning issue
        pass


def translateNotes():
    print("test image to text")
    if uploaded_jpg and (uploaded_jpg.name.endswith('.jpg') or uploaded_jpg.name.endswith('.png'))== True:
        notes_text = detect_document(uploaded_jpg)
        st.session_state['notes_text'] = notes_text
    else:
        pass


def compareNotes(sum_lesson, notes):
    notes = notes.replace("\n", "")
    compare_text = sum_lesson + notes
    print("Compare Text", compare_text)
    system_prompt = "The content provided is a lesson, and the passagea after, separated by the |, are the notes. Are there any key ideas missing from the notes that appear in the lesson, in dot jot form?."
    output = summary.summarize(client, system_prompt, compare_text)
    print(output[1])
    return output[0]
    

if __name__ == "__main__":
    client = summary.initialize()

    st.title("ProNotes")

    
    st.write("**The future of retaining information**")
    uploaded_audio = st.file_uploader("Choose a mp3 file")

    summary_button = st.button("Create Notes")
    if summary_button:
        summarized_audio = transcriptAudio()

    if st.session_state['transcript']:
        st.text_area("Transcript:", st.session_state['transcript'])
    
    if st.session_state['sum_notes']:
        st.text_area("Summary:", st.session_state['sum_notes'])


    st.write("**Upload handwritten notes and compare with the lesson**")
    uploaded_jpg = st.file_uploader("Choose a jpg file")

    image_to_text_button = st.button("Convert Image to Text")
    if image_to_text_button:
        translateNotes()

    if st.session_state['notes_text']:
        st.text_area("Notes:", st.session_state['notes_text'])    
    
    compare_button = st.button("Compare Notes to Lesson")
    if compare_button:
        comparison = compareNotes(st.session_state['sum_notes'], st.session_state['notes_text'])
        comparison = "You should consider adding the following ideas to your notes: \n" + comparison
        st.text_area("Comparison:", comparison)

    