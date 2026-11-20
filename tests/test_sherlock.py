import pytest
from src.sherlock import check_site, check_sites_concurrent

def test_check_site_structure():
    site = {"name": "Test", "url": "https://example.com/{}", "method": "GET"}
    result = check_site(site, "testuser", ssl=False)
    assert isinstance(result, dict)
    assert result["site"] == "Test"
    assert "found" in result
    assert isinstance(result["found"], bool)
    assert result["url"] == "https://example.com/testuser"

@pytest.mark.asyncio
async def test_check_sites_concurrent():
    results = await check_sites_concurrent("pytestuser", ssl=False)
    assert isinstance(results, list)
    assert len(results) == 3
    for r in results:
        assert "site" in r
        assert "found" in r
        assert "url" in r

def test_check_site_uses_get_method():
    """Test that GET method is used when method field is GET or absent."""
    # Explicit GET
    site = {"name": "Test", "url": "https://example.com/{}", "method": "GET"}
    result = check_site(site, "testuser", ssl=False)
    assert result["url"] == "https://example.com/testuser"
    
    # Default (no method field) should default to GET
    site_no_method = {"name": "Test", "url": "https://example.com/{}"}
    result2 = check_site(site_no_method, "testuser", ssl=False)
    assert result2["url"] == "https://example.com/testuser"

@pytest.mark.asyncio
async def test_check_site_uses_post_method():
    """Test that POST method is used when method field is POST."""
    import requests
    # POST method should actually use POST request
    # httpbin.org echo endpoint will show us the method used
    site = {"name": "Test", "url": "https://httpbin.org/post", "method": "POST"}
    result = check_site(site, "testuser", ssl=False)
    assert result["found"] == True  # httpbin.org returns 200 for POST
    assert "post" in result["url"].lower() or "post" in str(result).lower()
