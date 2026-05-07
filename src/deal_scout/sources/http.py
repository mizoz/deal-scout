from __future__ import annotations

import requests


def fetch_text(url: str, *, user_agent: str, timeout: int = 20) -> str:
    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    return response.text


def fetch_json(url: str, *, user_agent: str, timeout: int = 20):
    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=timeout)
    response.raise_for_status()
    return response.json()

