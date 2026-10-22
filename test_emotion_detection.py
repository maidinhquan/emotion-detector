"""Unit tests for the emotion detection package and Flask application."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector
from server import app


class EmotionDetectorTests(unittest.TestCase):
    """Tests for Watson response parsing and error handling."""

    @staticmethod
    def make_response(scores: dict[str, float], status_code: int = 200) -> Mock:
        """Create a mock Watson API response."""
        response = Mock()
        response.status_code = status_code
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}],
        }
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_scores_and_dominant_emotion(self, post: Mock) -> None:
        """Return scores in the documented format."""
        scores = {
            "anger": 0.02,
            "disgust": 0.01,
            "fear": 0.03,
            "joy": 0.91,
            "sadness": 0.04,
        }
        post.return_value = self.make_response(scores)

        result = emotion_detector("I am very happy")

        self.assertEqual(result, {**scores, "dominant_emotion": "joy"})
        post.assert_called_once()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input_does_not_call_service(self, post: Mock) -> None:
        """Reject blank input without making an HTTP request."""
        self.assertIsNone(emotion_detector("  "))
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request_returns_none(self, post: Mock) -> None:
        """Convert a Watson HTTP 400 response to None."""
        post.return_value = self.make_response({}, status_code=400)

        self.assertIsNone(emotion_detector("invalid"))


class FlaskApplicationTests(unittest.TestCase):
    """Tests for web routes and blank-input handling."""

    def test_homepage_renders_detector(self) -> None:
        """Render the web application's home page."""
        app.testing = True
        response = app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detector", response.data)

    @patch("server.emotion_detector")
    def test_detector_route_returns_scores(self, detector: Mock) -> None:
        """Return the emotion scores and dominant result from the API route."""
        detector.return_value = {
            "anger": 0.02,
            "disgust": 0.01,
            "fear": 0.03,
            "joy": 0.91,
            "sadness": 0.04,
            "dominant_emotion": "joy",
        }
        app.testing = True
        response = app.test_client().get(
            "/emotionDetector?textToAnalyze=I%20am%20happy"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("dominant emotion is joy", response.get_data(as_text=True))
        detector.assert_called_once_with("I am happy")

    def test_blank_text_returns_client_error(self) -> None:
        """Return a readable client error for blank input."""
        app.testing = True
        response = app.test_client().get("/emotionDetector?textToAnalyze=%20")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main()
