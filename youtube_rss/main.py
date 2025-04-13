# youtube_rss/main.py
"""
Usage:
  latest_videos.py <input_file> <output_file>
"""

from docopt import docopt
from pathlib import Path
from typing import List, Dict
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from loguru import logger
import re
import sys
from bs4 import BeautifulSoup


def extract_username(url: str) -> str:
    """Extracts the username from a YouTube channel URL.
    Raises ValueError if the URL is malformed.
    """
    match = re.match(r"https?://(www\.)?youtube\.com/user/([^/]+)$", url.strip())
    if not match:
        raise ValueError(f"Malformed YouTube URL: {url}")
    return match.group(2)


def resolve_channel_feed_url(user_url: str) -> str:
    """Fetches the main channel page and extracts the RSS feed URL from the HTML."""
    logger.info(f"Resolving RSS feed URL from {user_url}")
    response = requests.get(user_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    link_tag = soup.find('link', rel='alternate', type='application/rss+xml')
    if not link_tag or not link_tag.get('href'):
        raise ValueError(f"RSS feed URL not found on page: {user_url}")
    return link_tag['href']


def fetch_rss_feed(feed_url: str) -> List[Dict]:
    """Fetches and parses RSS feed from a feed URL."""
    logger.info(f"Fetching RSS feed from {feed_url}")
    response = requests.get(feed_url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    videos = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text
        link = entry.find('atom:link', ns).attrib['href']
        published = entry.find('atom:published', ns).text
        videos.append({
            'title': title,
            'link': link,
            'published': datetime.strptime(published, "%Y-%m-%dT%H:%M:%S+00:00")
        })
    return videos


def generate_html(videos: List[Dict], output_file: Path) -> None:
    """Generates an HTML page from a list of videos."""
    html_content = [
        "<html>",
        "<head><title>Latest YouTube Videos</title></head>",
        '<body style="background-color:lightblue; color:darkblue; font-family:sans-serif;">',
        "<h1>Latest YouTube Videos</h1>"
    ]

    for video in sorted(videos, key=lambda x: x['published'], reverse=True):
        video_id = video['link'].split('v=')[-1]
        iframe = f"""
        <div style='margin-bottom: 30px;'>
            <h3>{video['title']}</h3>
            <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
            <p><small>Published: {video['published'].strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </div>
        """
        html_content.append(iframe)

    html_content.append("</body></html>")
    output_file.write_text('\n'.join(html_content))


def main() -> None:
    args = docopt(__doc__)
    input_file = Path(args['<input_file>'])
    output_file = Path(args['<output_file>'])

    if not input_file.exists():
        logger.error(f"Input file does not exist: {input_file}")
        sys.exit(1)

    urls = input_file.read_text().splitlines()
    all_videos = []
    for url in urls:
        if not url.strip():
            continue
        try:
            feed_url = resolve_channel_feed_url(url)
            videos = fetch_rss_feed(feed_url)
            all_videos.extend(videos)
        except Exception as e:
            logger.error(f"Failed to process URL '{url}': {e}")

    generate_html(all_videos, output_file)


if __name__ == "__main__":
    main()
