from flask import Flask, request, send_file, jsonify, render_template
import moviepy.editor as mp
import os
from spleeter.separator import Separator
from multiprocessing import Process, Manager
import shutil
from pydub import AudioSegment
from pydub.effects import normalize, high_pass_filter, low_pass_filter
from gevent.pywsgi import WSGIServer

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and file.filename.endswith('.mp4'):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            return jsonify({'filename': file.filename})
        return jsonify({'error': 'Invalid file format'})

    @app.route('/process/<filename>', methods=['GET'])
    def process_file(filename):
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(PROCESSED_FOLDER, 'no_vocals_' + filename)

        global progress_dict
        progress_dict['progress'] = 0

        processing_process = Process(target=process_video, args=(video_path, output_path, progress_dict))
        processing_process.start()
        return jsonify({'status': 'processing'})

    @app.route('/progress', methods=['GET'])
    def progress():
        global progress_dict
        return jsonify({'progress': progress_dict['progress']})

    @app.route('/download/<filename>', methods=['GET'])
    def download_file(filename):
        output_path = os.path.join(PROCESSED_FOLDER, 'no_vocals_' + filename)
        return send_file(output_path, as_attachment=True)

    return app


def extract_audio_from_video(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def remove_vocals(audio_path, output_path, progress_dict):
    separator = Separator('spleeter:2stems', stft_backend='librosa')
    separator.separate_to_file(audio_path, output_path)
    accompaniment_path = os.path.join(output_path, os.path.splitext(os.path.basename(audio_path))[0],
                                      'accompaniment.wav')
    progress_dict['progress'] = 66
    return accompaniment_path


def post_process_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    audio = normalize(audio)  # Normalize audio to have consistent volume
    audio = high_pass_filter(audio, cutoff=80)  # Apply high-pass filter
    audio = low_pass_filter(audio, cutoff=15000)  # Apply low-pass filter
    audio.export(audio_path, format="wav")


def merge_audio_with_video(video_path, audio_path, output_path, progress_dict):
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(audio_path)
    new_video = video.set_audio(audio)
    new_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    progress_dict['progress'] = 100


def process_video(video_path, output_path, progress_dict):
    temp_audio_path = os.path.join(PROCESSED_FOLDER, 'temp_audio.wav')
    temp_output_dir = os.path.join(PROCESSED_FOLDER, 'output')
    extract_audio_from_video(video_path, temp_audio_path)
    progress_dict['progress'] = 33
    instrumental_path = remove_vocals(temp_audio_path, temp_output_dir, progress_dict)
    post_process_audio(instrumental_path)
    merge_audio_with_video(video_path, instrumental_path, output_path, progress_dict)
    os.remove(temp_audio_path)
    os.remove(instrumental_path)
    shutil.rmtree(temp_output_dir)


if __name__ == '__main__':
    manager = Manager()
    progress_dict = manager.dict()
    progress_dict['progress'] = 0

    app = create_app()
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
