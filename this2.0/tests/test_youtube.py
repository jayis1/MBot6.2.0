import pytest
import asyncio
from cogs.youtube import YTDLSource

@pytest.mark.asyncio
async def test_ytdlsource_extraction():
    url = "ytsearch1:never gonna give you up"
    # Basic test to ensure yt-dlp can extract metadata
    # This might actually hit YouTube, so we want it to be a light query.
    # A real unit test would mock `yt_dlp.YoutubeDL`. For now this acts as an integration test.
    tracks = await YTDLSource.from_url(url, loop=asyncio.get_event_loop())
    assert len(tracks) > 0
    track = tracks[0]
    assert track.title is not None
    assert track.url is not None
    assert track.duration is not None
