import pytest
import aioresponses
from utils.suno import is_suno_url, get_suno_track

@pytest.mark.asyncio
async def test_is_suno_url():
    assert is_suno_url("https://suno.com/song/0b65f620-32b0-40db-b09a-e455e3adb2c9") is True
    assert is_suno_url("https://app.suno.ai/song/0b65f620-32b0-40db-b09a-e455e3adb2c9") is True
    assert is_suno_url("https://suno.com/invalid/0b65f620-32b0-40db-b09a-e455e3adb2c9") is False
    assert is_suno_url("https://youtube.com/watch?v=123") is False

@pytest.mark.asyncio
async def test_get_suno_track_success():
    song_id = "0b65f620-32b0-40db-b09a-e455e3adb2c9"
    url = f"https://suno.com/song/{song_id}"
    cdn_url = f"https://cdn1.suno.ai/{song_id}.mp3"
    
    html_content = '''
    <html>
        <head>
            <meta property="og:title" content="Test Song Title" />
            <meta property="og:image" content="https://example.com/thumb.jpg" />
        </head>
    </html>
    '''
    
    with aioresponses.aioresponses() as m:
        m.get(url, status=200, body=html_content)
        m.head(cdn_url, status=200)
        
        track = await get_suno_track(url)
        assert track is not None
        assert track.song_id == song_id
        assert track.title == "Test Song Title"
        assert track.thumbnail == "https://example.com/thumb.jpg"
        assert track.url == cdn_url

@pytest.mark.asyncio
async def test_get_suno_track_invalid_url():
    track = await get_suno_track("https://suno.com/not-a-song")
    assert track is None

@pytest.mark.asyncio
async def test_get_suno_track_cdn_unreachable():
    song_id = "0b65f620-32b0-40db-b09a-e455e3adb2c9"
    url = f"https://suno.com/song/{song_id}"
    cdn_url = f"https://cdn1.suno.ai/{song_id}.mp3"
    
    with aioresponses.aioresponses() as m:
        m.get(url, status=200, body='<html><head><title>Test</title></head></html>')
        m.head(cdn_url, status=404)
        
        track = await get_suno_track(url)
        assert track is None
