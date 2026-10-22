# Emotion Detector

A Flask application that uses the Watson NLP EmotionPredict service to return
anger, disgust, fear, joy, and sadness scores, along with the dominant emotion.

## Run locally

1. Create and activate a Python virtual environment.
2. Install the dependencies with `python -m pip install -r requirements.txt`.
3. Start the web application with `python server.py`.
4. Open `http://127.0.0.1:5000/` in a browser and enter text to analyze.

The API is available at `/emotionDetector?textToAnalyze=your%20text`. Empty
input and a Watson HTTP 400 response produce an invalid-input message.

## Run tests

Run `python -m unittest -v test_emotion_detection.py`. The service calls are
mocked, so the tests do not require network access or a Watson service account.

Run pylint across the Python files with:

```powershell
python -m pylint server.py EmotionDetection\emotion_detection.py EmotionDetection\__init__.py test_emotion_detection.py
```

The current score is 10.00/10.

## Package layout

- `EmotionDetection/emotion_detection.py`: Watson API client and output formatter.
- `EmotionDetection/__init__.py`: package export.
- `server.py`: Flask interface and input validation.
- `test_emotion_detection.py`: unit tests.
