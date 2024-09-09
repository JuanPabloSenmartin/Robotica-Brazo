import time
import cv2
import streamlit as st
import speech_recognition as sr

st.title("Cobot Remote Control")
col1, col2 = st.columns([5, 2])

message_preview = ""
audio_message_preview = ""


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone(chunk_size=720) as source:
        print("Say something!")
        # todo: test mic sensitivity
        audio = recognizer.listen(source)
    try:
        return {
            'status': 'ok',
            'text': recognizer.recognize_google(audio)
        }
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return {
            'status': 'error',
            'text': 'Google Speech Recognition could not understand audio'
        }
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return {
            'status': 'error',
            'text': 'Could not request results from Google Speech Recognition service'.format(e)
        }


message_preview = col1.text_input("Enter input:", "")

pic = col1.camera_input("Camera Input")
if pic:
    print("PIC", pic)

camera_placeholder = col1.empty()
recording_text_placeholder = col1.empty()

st.session_state.recording = True
ocr_button = col1.button("Get Text")
picture_button = col1.button("Send Picture")
recording_button = col1.button("Record")

if recording_button:
    recording_text_placeholder.text("Recording...")
    result = recognize_speech()
    recording_text_placeholder.text("Recording finished.")
    audio_message_preview = result['text']
    time.sleep(2)
    recording_text_placeholder.text("")

col2.subheader("Message Preview")


def get_not_empty_preview(message_preview, audio_message_preview):
    if message_preview:
        return message_preview
    elif audio_message_preview:
        return audio_message_preview
    else:
        return ""


col2.write(get_not_empty_preview(message_preview, audio_message_preview))
