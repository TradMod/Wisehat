import re
import requests
from langchain_community.document_loaders import WebBaseLoader

IMMUNEFI_BASE = "https://immunefi.com/bug-bounty"
_SLUG_PATTERN = re.compile(r'bug-bounty/([a-zA-Z0-9_.-]+)/?')
_slug_cache: set[str] | None = None


def _fetch_slugs() -> set[str]:
    global _slug_cache
    if _slug_cache is None:
        try:
            resp = requests.get(f"{IMMUNEFI_BASE}/", timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Could not fetch Immunefi program list: {e}") from e
        _slug_cache = set(_SLUG_PATTERN.findall(resp.text))
    return _slug_cache


def _resolve_slug(program_name: str) -> str:
    slugs = _fetch_slugs()
    if program_name in slugs:
        return program_name
    lowered = program_name.lower()
    for slug in slugs:
        if slug.lower() == lowered:
            return slug
    raise ValueError(
        f"Program '{program_name}' not found on Immunefi. "
        f"Browse available programs at {IMMUNEFI_BASE}/"
    )


def immunefi_data(program_name):
      program_name = program_name.strip()
      slug = _resolve_slug(program_name)
      url1 = f"{IMMUNEFI_BASE}/{slug}/information"
      url2 = f"{IMMUNEFI_BASE}/{slug}/scope"
      url3 = f"{IMMUNEFI_BASE}/{slug}/resources"

      for label, url in [("information", url1), ("scope", url2), ("resources", url3)]:
            try:
                  resp = requests.head(url, allow_redirects=True, timeout=15)
            except requests.RequestException as e:
                  raise ValueError(
                        f"Could not reach Immunefi ({label}) for '{slug}': {e}"
                  ) from e
            if resp.status_code != 200:
                  raise ValueError(
                        f"Program '{slug}' not reachable on Immunefi "
                        f"({label} returned HTTP {resp.status_code})"
                  )

      docs1 = WebBaseLoader(url1).load()
      docs2 = WebBaseLoader(url2).load()
      docs3 = WebBaseLoader(url3).load()

      information = docs1[0].page_content.strip()
      scope = docs2[0].page_content.strip()
      resources = docs3[0].page_content.strip()

      if not information or not scope or not resources:
            raise ValueError(
                  f"Program '{slug}' returned empty content from Immunefi"
            )

      return {
            "information": information,
            "scope": scope,
            "resources": resources,
      }

# program_name = input("name: ")
# result = immunefi_data(program_name)

# print(result)