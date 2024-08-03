# Vision for the Blind
Vision for the Blind is an AI-powered application designed to assist visually impaired individuals by providing real-time audio descriptions of their surroundings. Users can take pictures of their surroundings and upload the picture, then ask questions about it. The application uses advanced AI models to understand the user's question and surroundings to produce instant, informative audio responses that answer the question. It uses Streamlit to create an interactive and accessible experience. Its aim is to make visually impaired people more independent and experience the joy we feel by seeing this beautiful world around us.

## Table of Contents

- [Features](#Features)
- [Project Structure](#Project-Structure)
- [How It Works](#How-It-Works)
- [Contact](#Contact)
- [Note](#Note)

## Features

- **Real-time Audio Recording**: Users can record their voice to ask questions about their surroundings.
- **Image Processing**: Upload an image that mimics your real-time surroudings and ask questions about it.
- **Text-to-Speech**: The application converts the model’s responses into audio, providing an auditory output making it suitable for the visually impaired.
- **Interactive Chat History**: View and interact with the history of queries and responses.

## Project Structure

```
Vision-for-the-Blind/
│
├── extra_info.py        # Contains the prompt and project description
├── st_app.py            # Main Streamlit application
├── requirements.txt     # Python dependencies
├── packages.txt         # Espeak package download
└── README.md            # Project README file
```

## How It Works

1. **Upload Image**: Upload an image and act as if it's your real-time surroundings.
2. **Audio Recording**: Start recording your voice to input a question.
3. **Speech-to-Text**: The recorded audio is converted to text using the `distil-whisper` model.
4. **Image Analysis**: The text query and uploaded image are processed by the `gemini-pro-vision` model to generate a description.
5. **Text-to-Speech**: The response from the model is converted into audio using the `elevenlabs` library.
6. **Interactive Output**: Both the text and audio responses are displayed and played within the application.

### Detailed Explanation of Key Functions:

- **Speech-to-Text**: Converts audio input to text using the `distil-whisper` model.
- **ask_model_about_surroundings**: Queries the vision model to describe the image.
- **model_response_to_audio**: Converts the model’s text response to audio.
- **autoplay_audio**: Automatically plays the generated audio response.

## Contact

For questions or suggestions, please open an issue or contact me directly:

- **Email**: adnanbarwaniwala7@gmail.com

## Note

Due to API quotas on the number of characters that can be converted into speech by the `elevenlabs` library, you maybe unable to use the text-to-speech ability if you're using the app website. In such a case, you'll have to wait until next month when the quota is renewed. Sorry for the inconvenience!!

Additionally if you face any errors while running the website, please run the code locally. It will work just fine. Sorry for the incovenience!!

---
