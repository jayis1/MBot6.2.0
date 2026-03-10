import pytest
import asyncio
from cogs.youtube import YTDLSource, YTDL_FORMAT_OPTIONS

@pytest.mark.asyncio
async def test_playlist_extraction():
    # Using a known small playlist or a search query that returns a playlist
    # For testing purposes, we can try a search query with 'playlist' keyword if we don't have a stable URL
    url = "https://www.youtube.com/playlist?list=PL3v6uIu7mXjrU6P8x_9_P7mXv6t_8g6r0" # Just an example, might need a real one
    
    # Alternatively, use a search query that should return a playlist-like structure if we remove 'noplaylist'
    # Actually, let's just test that the options are passed correctly
    
    playlist_opts = YTDL_FORMAT_OPTIONS.copy()
    playlist_opts["noplaylist"] = False
    playlist_opts["playlist_items"] = "1-2" # Just 2 items for quick test
    
    # We'll use a search query that might return multiple results if noplaylist is false
    # But usually search results are 'entries' anyway.
    
    # Let's use a real public playlist URL if possible or just mock it.
    # For now, let's just attempt a small one.
    
    try:
        results = await YTDLSource.from_url(url, loop=asyncio.get_event_loop(), ytdl_opts=playlist_opts)
        assert isinstance(results, list)
        assert len(results) > 0
        print(f"Successfully extracted {len(results)} items from playlist.")
    except Exception as e:
        pytest.fail(f"Playlist extraction failed: {e}")

@pytest.mark.asyncio
async def test_single_video_as_list():
    url = "ytsearch1:never gonna give you up"
    results = await YTDLSource.from_url(url, loop=asyncio.get_event_loop())
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].title is not None
