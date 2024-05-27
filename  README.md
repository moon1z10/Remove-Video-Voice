# Voice Removal from Video

This project is a web application that allows users to upload an MP4 video file, remove the vocal track, and download the processed video. The application uses Python's Flask framework for the backend and JavaScript for the frontend. The vocal removal is done using the Spleeter library.

## Features

- Upload MP4 video files
- Remove vocal tracks from videos using Spleeter
- Display conversion progress with a progress bar
- Download the processed video file

## Requirements

- Python 3.6+
- Flask
- MoviePy
- Spleeter
- Pydub
- ffmpeg (must be installed and available in PATH)

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Install `ffmpeg`:
    - **Ubuntu**:
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```
    - **Windows**:
        Download and install from [ffmpeg.org](https://ffmpeg.org/download.html). Add ffmpeg to your system PATH.

## Usage

1. Start the Flask server:
    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Upload an MP4 video file using the upload button.

4. The application will display a progress bar showing the conversion progress.

5. Once the conversion is complete, a download button will appear. Click the button to download the processed video file.

## Project Structure


README.md
md
코드 복사
# Voice Removal from Video

This project is a web application that allows users to upload an MP4 video file, remove the vocal track, and download the processed video. The application uses Python's Flask framework for the backend and JavaScript for the frontend. The vocal removal is done using the Spleeter library.

## Features

- Upload MP4 video files
- Remove vocal tracks from videos using Spleeter
- Display conversion progress with a progress bar
- Download the processed video file

## Requirements

- Python 3.6+
- Flask
- MoviePy
- Spleeter
- Pydub
- ffmpeg (must be installed and available in PATH)

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Install `ffmpeg`:
    - **Ubuntu**:
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```
    - **Windows**:
        Download and install from [ffmpeg.org](https://ffmpeg.org/download.html). Add ffmpeg to your system PATH.

## Usage

1. Start the Flask server:
    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Upload an MP4 video file using the upload button.

4. The application will display a progress bar showing the conversion progress.

5. Once the conversion is complete, a download button will appear. Click the button to download the processed video file.

## Project Structure
```
voice-removal-from-video/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # HTML template for the web interface
└── README.md # This README file
```

## Dependencies

- Flask: A micro web framework for Python
- MoviePy: A Python library for video editing
- Spleeter: A deep learning-based library for source separation
- Pydub: A Python library for audio manipulation
- ffmpeg: A complete, cross-platform solution to record, convert and stream audio and video


## app.py Explanation

The `app.py` file is the core of the application, handling the backend logic using Flask. Here's a breakdown of its components and functionality:

1. **Imports and Configuration**:
    - The necessary libraries (`Flask`, `moviepy`, `os`, `spleeter`, `threading`) are imported.
    - The Flask application is initialized.
    - Upload and processed folders are created if they don't exist.

2. **Helper Functions**:
    - `extract_audio_from_video(video_path, audio_path)`: Extracts the audio track from the video file.
    - `remove_vocals(audio_path, output_path)`: Uses Spleeter to separate the vocal and accompaniment tracks, and returns the path to the accompaniment track.
    - `merge_audio_with_video(video_path, audio_path, output_path)`: Merges the accompaniment audio track back with the video file using H.264 codec.
    - `process_video(video_path, output_path, progress_callback)`: Manages the entire process of extracting audio, removing vocals, and merging the audio back with the video while updating progress.

3. **Routes**:
    - `@app.route('/')`: Serves the main HTML page.
    - `@app.route('/upload', methods=['POST'])`: Handles file uploads and saves the uploaded MP4 file.
    - `@app.route('/process/<filename>', methods=['GET'])`: Starts the video processing in a separate thread and returns the status.
    - `@app.route('/progress', methods=['GET'])`: Returns the current progress of the video processing.
    - `@app.route('/download/<filename>', methods=['GET'])`: Serves the processed video file for download.

4. **Running the Application**:
    - The application runs in debug mode for development purposes.

## Dependencies

- Flask: A micro web framework for Python
- MoviePy: A Python library for video editing
- Spleeter: A deep learning-based library for source separation
- Pydub: A Python library for audio manipulation
- ffmpeg: A complete, cross-platform solution to record, convert and stream audio and video

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
