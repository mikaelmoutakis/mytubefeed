from youtube_rss.main import extract_username, fetch_rss_feed
import pytest
from unittest.mock import patch, Mock


def test_extract_username_valid():
    url = "https://www.youtube.com/user/darbinorvar"
    assert extract_username(url) == "darbinorvar"


def test_extract_username_invalid():
    with pytest.raises(ValueError):
        extract_username("https://www.youtube.com/c/darbinorvar")


# @patch("youtube_rss.main.requests.get")
# def test_fetch_rss_feed_parses_correctly(mock_get):
#     mock_response = Mock()
#     mock_response.content = b\"\"\"\n        <feed xmlns=\"http://www.w3.org/2005/Atom\">\n            <entry>\n                <title>Test Video</title>\n                <link href=\"https://www.youtube.com/watch?v=abc123\"/>\n                <published>2023-04-12T15:00:00.000Z</published>\n            </entry>\n        </feed>\n    \"\"\"\n    mock_response.raise_for_status = Mock()\n    mock_get.return_value = mock_response\n\n    videos = fetch_rss_feed(\"darbinorvar\")\n    assert len(videos) == 1\n    assert videos[0]['title'] == \"Test Video\"\n    assert videos[0]['link'] == \"https://www.youtube.com/watch?v=abc123\"\n    assert videos[0]['published'].isoformat() == \"2023-04-12T15:00:00\"\n```
