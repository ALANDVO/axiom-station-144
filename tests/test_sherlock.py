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
