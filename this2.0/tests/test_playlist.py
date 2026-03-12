import pytest
import asyncio
from cogs.youtube import YTDLSource, YTDL_FORMAT_OPTIONS

@pytest.mark.asyncio
async def test_playlist_extraction():
    url = "https://youtube.com/playlist?list=PL7UlqC4kFPVpadgAlxqcYPhWPPJ_H2Ghi&si=acuADwYbCwY45rR5"
    
    playlist_opts = YTDL_FORMAT_OPTIONS.copy()
    playlist_opts["noplaylist"] = False
    playlist_opts["playlist_items"] = "1-2" # Just 2 items for quick test
    
    try:
        results = await YTDLSource.from_url(url, loop=asyncio.get_event_loop(), ytdl_opts=playlist_opts)
        assert isinstance(results, list)
        assert len(results) > 0
        print(f"Successfully extracted {len(results)} items from playlist.")
    except Exception as e:
        pytest.fail(f"Playlist extraction failed: {e}")

@pytest.mark.asyncio
async def test_radio_extraction():
    url = "https://youtube.com/playlist?list=PL7UlqC4kFPVpadgAlxqcYPhWPPJ_H2Ghi&si=acuADwYbCwY45rR5"
    
    radio_opts = YTDL_FORMAT_OPTIONS.copy()
    radio_opts["noplaylist"] = False
    radio_opts["playlist_items"] = "1-10" # test with 10 items
    
    try:
        results = await YTDLSource.from_url(url, loop=asyncio.get_event_loop(), ytdl_opts=radio_opts)
        assert isinstance(results, list)
        assert len(results) > 2
        print(f"Successfully extracted {len(results)} items from radio playlist.")
    except Exception as e:
        pytest.fail(f"Radio extraction failed: {e}")

@pytest.mark.asyncio
async def test_single_video_as_list():
    url = "ytsearch1:never gonna give you up"
    results = await YTDLSource.from_url(url, loop=asyncio.get_event_loop())
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].title is not None
