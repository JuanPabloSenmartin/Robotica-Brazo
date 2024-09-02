import time
import cv2
import streamlit as st
import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
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


message_preview = ""
audio_message_preview = ""

st.title("Cobot Remote Control")

col1, col2 = st.columns([5, 2])

message_preview = col1.text_input("Enter input:", "")

# Create a placeholder in the first column for the camera feed
camera_placeholder = col1.empty()
recording_text_placeholder = col1.empty()

st.session_state.recording = True
recording_button_title = "Record"
recording_button = col1.button(recording_button_title)

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
#
# cap = cv2.VideoCapture(1)
# stop_button_pressed = st.button("Stop")
#
# while cap.isOpened() and not stop_button_pressed:
#     ret, frame = cap.read()
#
#     if not ret:
#         st.write("The video capture has ended.")
#         break
#
#     # Convert the frame from BGR to RGB format
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     # Display the frame in the placeholder within the first column
#     camera_placeholder.image(frame, channels="RGB")
#
#     # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
#     if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
#         break
#
# cap.release()
# cv2.destroyAllWindows()
