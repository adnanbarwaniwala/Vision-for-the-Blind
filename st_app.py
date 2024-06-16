import streamlit as st
from st_audiorec import st_audiorec
from streamlit_chat import message
from PIL import Image
from transformers import pipeline, VitsModel, AutoTokenizer
import torch
import soundfile as sf
import numpy as np
import wave
import librosa
from pydub import AudioSegment
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from extra_info import vision_model_system_prompt, description
import subprocess

# Setting the page title
st.set_page_config(
    page_title='Vision for the Blind',
    page_icon=':eyes:'
)

st.title('Vision for the Blind :eyes:')
with st.expander('Project Description'):
    st.markdown(f"_{description.strip()}_")

google_api_key = st.secrets['general']['google_api_key']

def del_msgs():
    if 'messages' in st.session_state:
        del st.session_state['messages']


def speech_to_text(path):
    with st.spinner('Converting audio to text...'):
        audio, sampling_rate = sf.read(path)
        asr = pipeline(task="automatic-speech-recognition",
                       model="distil-whisper/distil-small.en")
        audio_transposed = np.transpose(audio)
        audio_mono = librosa.to_mono(audio_transposed)
        user_query = asr(audio_mono)
    st.markdown("_USER QUERY:_")
    st.markdown(f"**_{user_query['text'].strip()}_**")
    st.write(f"{'*' * 80}")
    return user_query['text']


def ask_model_about_surroundings(query, image_url):
    with st.spinner('Querying vision model...'):
        llm = ChatGoogleGenerativeAI(model='gemini-pro-vision', google_api_key=google_api_key)
        messages = [
            HumanMessage(content=[
                {'type': 'text', 'text': vision_model_system_prompt.format(user_query=query)},
                {'type': 'image_url', 'image_url': image_url}
            ])
        ]
        response = llm.invoke(messages).content
    st.markdown("_MODEL RESPONSE:_")
    st.markdown(f"**_{response.strip()}_**")
    st.write(f"{'*' * 80}")
    return response


def model_response_to_audio(response):
    with st.spinner('Converting response to audio...'):
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
    # Set the library path dynamically (you might need to adjust the path based on your environment)
        result = subprocess.run(['which', 'espeak'], stdout=subprocess.PIPE)
        espeak_path = result.stdout.decode('utf-8').strip()
        EspeakWrapper.set_library(espeak_path)
        model = VitsModel.from_pretrained("kakao-enterprise/vits-ljs")
        tokenizer = AutoTokenizer.from_pretrained("kakao-enterprise/vits-ljs")
        inputs = tokenizer(response, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs).waveform

        output_numpy = output.cpu().numpy()
        # Scale the data to 16-bit PCM format
        output_numpy = np.int16(output_numpy / np.max(np.abs(output_numpy)) * 32767)
        sample_rate = model.config.sampling_rate
        # Save the generated audio to a file using the wave library
        with wave.open('model_response.wav', 'w') as wf:
            wf.setnchannels(1)  # Set the number of channels
            wf.setsampwidth(2)  # Set the sample width to 2 bytes (16 bits)
            wf.setframerate(sample_rate)  # Set the sample rate
            wf.writeframes(output_numpy.tobytes())  # Write the audio data to the file
    st.markdown("**AUDIO GENERATED**")
    st.write(f"{'*' * 80}")


def autoplay_audio(file_path):
    import base64
    with st.spinner('Final audio processing...'):
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        audio_html = f'<audio src="data:audio/wav; base64, {base64_audio}" controls autoplay>'
    st.markdown("**PLAYING RESPONSE:**")
    st.markdown(audio_html, unsafe_allow_html=True)


# Setting up image uploading
with st.sidebar:
    if 'last_image' not in st.session_state:
        st.session_state.last_image = ''

    img = st.file_uploader('Upload an image:', type=['png', 'jpg'])
    if img and st.session_state.last_image != img.name:
        del_msgs()
        st.session_state['last_image'] = img.name
        st.session_state.img_changed = True
        img = Image.open(img)
        img.save('user_img.png', 'PNG')
    else:
        st.session_state.img_changed = False

if st.session_state.last_image != '':
    # Recording user query audio and storing it in a file
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Talk to your Vision Assistant')
        input_audio = st_audiorec()
        if input_audio is not None and not st.session_state.img_changed:
            st.audio(input_audio, format='audio/wav')
            with st.spinner('Loading and saving audio....'):
                with open("temp.wav", "wb") as file:
                    file.write(input_audio)
                # Loads the audio file and resamples to 16kHz
                audio = AudioSegment.from_wav("temp.wav")
                audio = audio.set_frame_rate(16000)
                audio.export("user_input.wav", format="wav")
            st.write(f"{'*' * 80}")
            st.markdown("**AUDIO SAVED**")
            st.write(f"{'*' * 80}")

            user_query = speech_to_text(path='user_input.wav')
            st.session_state.messages.append(user_query)

            model_response = ask_model_about_surroundings(user_query, image_url='user_img.png')
            st.session_state.messages.append(model_response)

            model_response_to_audio(model_response)
            autoplay_audio(file_path='model_response.wav')

    with col2:
        st.subheader('Chat History')
        with st.spinner('Displaying chat history...'):
            for i, msg in enumerate(st.session_state.messages):
                if i % 2 == 0:
                    message(msg, is_user=True, key=f'{i}+ :nerd_face:')
                else:
                    message(msg, is_user=False, key=f'{i} + :robot_face:')


