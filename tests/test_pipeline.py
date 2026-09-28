import unittest
from pop_context.pipeline import slugify, whisper_segments


class PipelineTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("https://example.com/a b"), "example.com-a-b")

    def test_whisper_segments(self):
        raw = {
            "transcription": [{
                "timestamps": {"from": "00:00:00,000", "to": "00:00:02,000"},
                "offsets": {"from": 0, "to": 2000},
                "text": " hello ",
            }]
        }
        result = whisper_segments(raw)
        self.assertEqual(result[0]["text"], "hello")
        self.assertEqual(result[0]["start_ms"], 0)
        self.assertEqual(result[0]["end_ms"], 2000)


if __name__ == "__main__":
    unittest.main()
