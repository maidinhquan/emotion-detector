"""Client for the Watson NLP emotion detection service."""

from typing import Any

import requests

EMOTION_DETECTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "model_id": MODEL_ID,
}
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str | None) -> dict[str, Any] | None:
    """Return the five emotion scores and the dominant emotion for text.

    An empty input or a Watson 400 response returns ``None``. Unexpected HTTP
    errors and malformed service responses are raised to the caller.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None

    response = requests.post(
        EMOTION_DETECTION_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers=HEADERS,
        timeout=30,
    )
    if response.status_code == 400:
        return None
    response.raise_for_status()

    response_data = response.json()
    emotion_predictions = response_data["emotionPredictions"]
    emotions = emotion_predictions[0]["emotion"]
    scores = {name: emotions[name] for name in EMOTION_NAMES}
    scores["dominant_emotion"] = max(EMOTION_NAMES, key=scores.__getitem__)
    return scores
