# Vision for the Blind

Vision for the Blind is an innovative application designed to prototype, on a much simpler scale, AI systems in glasses for visually impaired users that provide audio responses about the user's surroundings. This project leverages the power of AI models and Streamlit to create an interactive and accessible experience.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Real-time Audio Recording**: Users can record their voice to ask questions about their surroundings.
- **Image Processing**: Upload an image that mimics your real-time surroudings and ask questions about it.
- **Text-to-Speech**: The application converts the model’s responses into audio, providing an auditory output making it suitable for the visually impaired.
- **Interactive Chat History**: View and interact with the history of queries and responses.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/adnanbarwaniwala/Vision-for-the-Blind.git
    cd Vision-for-the-Blind
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the following command:
```bash
streamlit run st_app.py
```

Navigate to `http://localhost:8501` in your web browser to access the application.

## Project Structure

```
vision-for-the-blind/
│
├── extra_info.py        # Contains the prompt, project description and API key
├── st_app.py            # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md            # Project README file
└── images/              # Directory for storing images
```

## How It Works

1. **Upload Image**: Upload an image and act as if it's your real-time surroundings.
2. **Audio Recording**: Start recording your voice to input a question.
3. **Speech-to-Text**: The recorded audio is converted to text using the `distil-whisper` model.
4. **Image Analysis**: The text query and uploaded image are processed by the `gemini-pro-vision` model to generate a description.
5. **Text-to-Speech**: The response from the model is converted into audio using the `VitsModel`.
6. **Interactive Output**: Both the text and audio responses are displayed and played within the application.

### Detailed Explanation of Key Functions:

- **Speech-to-Text**: Converts audio input to text using the `distil-whisper` model.
- **ask_model_about_surroundings**: Queries the vision model to describe the image.
- **model_response_to_audio**: Converts the model’s text response to audio.
- **autoplay_audio**: Automatically plays the generated audio response.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue or contact me directly:

- **Email**: adnanbarwaniwala7@gmail.com

---
