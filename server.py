"""Flask web application for Watson NLP emotion detection."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def render_index_page() -> str:
    """Render the emotion detector interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion() -> tuple[str, int] | str:
    """Analyze the query string text and return a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze")
    if text_to_analyze is None or not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)
    if result is None:
        return "Invalid text! Please try again!", 400

    emotion_summary = ", ".join(
        f"'{emotion}': {result[emotion]}" for emotion in (
            "anger",
            "disgust",
            "fear",
            "joy",
            "sadness",
        )
    )
    dominant_emotion = result["dominant_emotion"]
    return (
        f"For the given statement, the system response is {emotion_summary}. "
        f"The dominant emotion is {dominant_emotion}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
