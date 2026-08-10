import importlib.util
import unittest
from email.message import Message
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("media_gate", ROOT / "tools/media_gate.py")
MEDIA_GATE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MEDIA_GATE)


class MediaGateTests(unittest.TestCase):
    def test_asset_url_quotes_filename_and_normalizes_separator(self):
        self.assertEqual(
            "https://example.invalid/media/one%20video.mp4",
            MEDIA_GATE.asset_url("https://example.invalid/media/", "one video.mp4"),
        )

    def test_range_response_requires_partial_mp4_response(self):
        headers = Message()
        headers["Content-Range"] = "bytes 0-1023/4096"
        headers["Content-Type"] = "video/mp4"
        self.assertEqual([], MEDIA_GATE.validate_range_response(206, headers))
        self.assertTrue(MEDIA_GATE.validate_range_response(200, Message()))

    def test_probe_contract(self):
        probe = {
            "streams": [
                {"codec_type": "video", "codec_name": "h264", "width": 1280, "height": 720},
                {"codec_type": "audio", "codec_name": "aac", "channels": 2},
            ],
            "format": {"duration": "60.2"},
        }
        self.assertEqual([], MEDIA_GATE.validate_probe(probe, 60.0))


if __name__ == "__main__":
    unittest.main()
