"""
Core module for checking username existence across sites.
"""

import asyncio
import requests
from typing import List, Dict, Any
import typer
from fastapi import FastAPI, Query

# Exported functions for testing
__all__ = ["check_site", "check_sites_concurrent"]

# Typer CLI app
cli_app = typer.Typer(help="Check username across social media sites")

# FastAPI app for HTTP API
fastapi_app = FastAPI(title="axiom-station-144 Username Checker")

SITES = [
    {"name": "Twitter", "url": "https://twitter.com/{}", "method": "GET"},
    {"name": "Instagram", "url": "https://www.instagram.com/{}", "method": "GET"},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "method": "GET"},
]

def check_site(site: Dict[str, Any], username: str, ssl: bool) -> Dict[str, Any]:
    """
    Check a single site for username presence.
    Returns dict with site name, found status, and URL.
    """
    url = site["url"].format(username)
    try:
        response = requests.get(url, verify=ssl, timeout=5)
        if response.status_code == 200:
            # simplistic detection: assume found if status 200
            found = True
        else:
            found = False
    except Exception:
        found = False
    return {"site": site["name"], "found": found, "url": url}


async def check_sites_concurrent(username: str, ssl: bool) -> List[Dict[str, Any]]:
    """
    Asynchronously check all sites.
    """
    tasks = [asyncio.to_thread(check_site, site, username, ssl) for site in SITES]
    results = await asyncio.gather(*tasks)
    return results


@cli_app.command()
def check(
    username: str,
    ssl: bool = typer.Option(True, "--ssl/--no-ssl", help="Enable or disable SSL verification")
):
    """
    CLI command to check username across configured sites.
    """
    import json
    results = asyncio.run(check_sites_concurrent(username, ssl))
    typer.echo(json.dumps(results, indent=2))


# FastAPI endpoint
@fastapi_app.get("/check")
async def check_fastapi(username: str = Query(..., description="Username to check"), ssl: bool = Query(True, description="Enable SSL verification")):
    """
    Check username across configured sites.
    """
    results = await check_sites_concurrent(username, ssl)
    return {"username": username, "results": results}


# Health check endpoint
@fastapi_app.get("/")
def health():
    return {"status": "ok", "service": "axiom-station-144"}


if __name__ == "__main__":
    # Run CLI when executed directly
    cli_app()
