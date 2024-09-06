import streamlit as st
from st_audiorec import st_audiorec
from streamlit_chat import message
from streamlit_player import st_player
from PIL import Image
from pydub import AudioSegment
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from extra_info import vision_model_system_prompt, description
from groq import Groq

google_api_key = st.secrets["general"]["google_api_key"]
groq_api_key = st.secrets['general']['groq_api_key']

st.set_page_config(
    page_title='Vision for the Blind',
    page_icon=':eyes:'
)

st.title('Vision for the Blind :eyes:')
with st.expander('Project Description'):
    st.markdown(f"_{description.strip()}_")


def del_msgs():
    if 'messages' in st.session_state:
        del st.session_state['messages']


def speech_to_text(path):
    with st.spinner('Converting audio to text...'):
        # Initialize the Groq client
        client = Groq(api_key=groq_api_key)
        # Open the audio file
        with open(path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(path, file.read()), 
                model="distil-whisper-large-v3-en",  
                prompt="Specify context or spelling",  
                response_format="json",
                temperature=0.0
            )
    st.markdown("_USER QUERY:_")
    st.markdown(f"**_{transcription.text.strip()}_**")
    st.write(f"{'*' * 80}")
    return transcription.text


def ask_model_about_surroundings(query, image_url):
    with st.spinner('Querying vision model...'):
        llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=google_api_key)
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
    import io
    from elevenlabs.client import ElevenLabs
    client = ElevenLabs(api_key=st.secrets['general']['elevenlabs_api_key'])
    with st.spinner('Converting response to audio...'):
        try:
            audio_generator = client.generate(text=response, voice="Jessica", model="eleven_multilingual_v2")
            audio_buffer = io.BytesIO()
            for chunk in audio_generator:
                audio_buffer.write(chunk)
        except Exception:
            st.write("The text-to-speech (tts) API character quota has been reached. Unfortunately you'll only be",
                     "to use the tts ability of the app next month now. Sorry for the inconvenience!!")
            return "error"
    st.markdown("**AUDIO GENERATED**")
    st.write(f"{'*' * 80}")
    audio_buffer.seek(0)
    return audio_buffer


def autoplay_audio(audio_buffer):
    if audio_buffer != "error":
        import base64
        with st.spinner('Final audio processing...'):
            audio_bytes = audio_buffer.read()
            base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay>'
        st.markdown("**PLAYING RESPONSE:**")
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        return


with st.sidebar:
    if 'last_image' not in st.session_state:
        st.session_state.last_image = ''

    img = st.file_uploader('Upload an image:', type=['png', 'jpg'])
    st_player('https://youtu.be/f1m0RJwif8Q')
    
    if img and st.session_state.last_image != img.name:
        del_msgs()
        st.session_state['last_image'] = img.name
        st.session_state.img_changed = True
        img = Image.open(img)
        img.save('user_img.png', 'PNG')
    else:
        st.session_state.img_changed = False

if st.session_state.last_image != '':
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

            autoplay_audio(model_response_to_audio(model_response))

    with col2:
        st.subheader('Chat History')
        with st.spinner('Displaying chat history...'):
            for i, msg in enumerate(st.session_state.messages):
                if i % 2 == 0:
                    message(msg, is_user=True, key=f'{i}+ :nerd_face:')
                else:
                    message(msg, is_user=False, key=f'{i} + :robot_face:')
