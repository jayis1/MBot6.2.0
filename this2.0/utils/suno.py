"""
utils/suno.py — Suno.com URL detection and audio stream resolution.

Supports URLs like:
  https://suno.com/song/<uuid>
  https://app.suno.ai/song/<uuid>

The MP3 is streamed directly from Suno's CDN.
Title and thumbnail are scraped from the page's OpenGraph meta tags.
"""

import re
import logging
import aiohttp

# Regex to match Suno song URLs and capture the song UUID
_SUNO_RE = re.compile(
    r'https?://(?:app\.suno\.ai|suno\.com)/song/([0-9a-f-]{36})',
    re.IGNORECASE
)

CDN_BASE = "https://cdn1.suno.ai"


def is_suno_url(text: str) -> bool:
    """Return True if text looks like a Suno song URL."""
    return bool(_SUNO_RE.search(text))


def _extract_song_id(url: str) -> str | None:
    m = _SUNO_RE.search(url)
    return m.group(1) if m else None


class SunoTrack:
    """Minimal track object compatible with music.py's queue/playback system."""

    def __init__(self, song_id: str, title: str, thumbnail: str | None, webpage_url: str):
        self.song_id = song_id
        self.title = title
        self.url = f"{CDN_BASE}/{song_id}.mp3"
        self.duration = 0          # Unknown — progress bar will show 0:00 / 0:00
        self.thumbnail = thumbnail
        self.webpage_url = webpage_url


async def get_suno_track(url: str) -> SunoTrack | None:
    """
    Given a Suno song URL, return a SunoTrack ready for playback.
    Returns None if the song ID cannot be extracted or the CDN is unreachable.
    """
    song_id = _extract_song_id(url)
    if not song_id:
        logging.warning(f"get_suno_track: Could not extract song ID from URL: {url}")
        return None

    webpage_url = f"https://suno.com/song/{song_id}"
    cdn_url = f"{CDN_BASE}/{song_id}.mp3"
    title = f"Suno Song ({song_id[:8]}…)"  # fallback title
    thumbnail = None

    # Try to scrape OpenGraph tags for title + thumbnail
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(webpage_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # og:title
                    m = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html)
                    if m:
                        title = m.group(1).strip()
                    else:
                        # fallback: try name="title"
                        m2 = re.search(r'<title>([^<]+)</title>', html)
                        if m2:
                            title = m2.group(1).strip()
                    # og:image
                    m3 = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
                    if m3:
                        thumbnail = m3.group(1).strip()
                else:
                    logging.warning(f"get_suno_track: Page fetch returned HTTP {resp.status} for {webpage_url}")

            # Quick HEAD check that the CDN MP3 is accessible
            async with session.head(cdn_url, timeout=aiohttp.ClientTimeout(total=8)) as cdn_resp:
                if cdn_resp.status not in (200, 206):
                    logging.error(f"get_suno_track: CDN returned HTTP {cdn_resp.status} for {cdn_url}")
                    return None

    except aiohttp.ClientError as e:
        logging.error(f"get_suno_track: HTTP error resolving {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"get_suno_track: Unexpected error for {url}: {e}")
        return None

    logging.info(f"get_suno_track: Resolved '{title}' → {cdn_url}")
    return SunoTrack(song_id=song_id, title=title, thumbnail=thumbnail, webpage_url=webpage_url)
