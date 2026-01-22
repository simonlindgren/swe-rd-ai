#!/usr/bin/env python3
"""
Download AI-related parliamentary documents from the Swedish Riksdag.

This script downloads documents matching AI-related search terms, filtered by
document type, for comparative discourse analysis.

Document types:
    - mot: Motioner (motions from individual MPs)
    - prop: Propositioner (government bills)

Usage:
    python download_corpus.py [--dry-run] [--limit N]

Author: Simon Lindgren
Date: 2026-01
"""

import httpx
import asyncio
import argparse
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


# Configuration
SEARCH_TERMS = [
    "artificiell intelligens",
    "AI",
]

DOCUMENT_TYPES = {
    "mot": "motioner",
    "prop": "propositioner",
}

DATE_FROM = "1990-01-01"  # Exclude older OCR'd documents with false positives

BASE_URL = "https://data.riksdagen.se"
DATA_DIR = Path(__file__).parent / "data"


@dataclass
class DownloadStats:
    """Track download statistics."""
    total_found: int = 0
    downloaded: int = 0
    failed: int = 0
    skipped: int = 0


def sanitise_filename(text: str, max_length: int = 30) -> str:
    """Create a safe filename from text."""
    safe = "".join(c for c in text if c.isalnum() or c in " -_")
    return safe[:max_length].strip()


async def fetch_document_list(
    client: httpx.AsyncClient,
    search_term: str,
    doc_type: str,
    page: int = 1,
    page_size: int = 100,
) -> tuple[list[dict], int]:
    """
    Fetch a page of document metadata from the Riksdag API.

    Returns:
        Tuple of (documents list, total hits)
    """
    params = {
        "sok": search_term,
        "doktyp": doc_type,
        "from": DATE_FROM,
        "utformat": "json",
        "sort": "datum",
        "sortorder": "desc",
        "p": page,
        "sz": page_size,
    }

    response = await client.get(f"{BASE_URL}/dokumentlista/", params=params)
    response.raise_for_status()
    data = response.json()

    if "dokumentlista" not in data:
        return [], 0

    doc_list = data["dokumentlista"]
    total_hits = int(doc_list.get("@traffar", 0))

    docs = doc_list.get("dokument", [])
    if isinstance(docs, dict):
        docs = [docs]

    return docs, total_hits


async def fetch_all_documents(
    client: httpx.AsyncClient,
    search_term: str,
    doc_type: str,
    limit: Optional[int] = None,
) -> list[dict]:
    """Fetch all document metadata with pagination."""
    all_docs = []
    page = 1

    while True:
        docs, total_hits = await fetch_document_list(
            client, search_term, doc_type, page
        )

        if not docs:
            break

        all_docs.extend(docs)
        print(f"      Page {page}: {len(docs)} docs (total: {len(all_docs):,}/{total_hits:,})")

        if len(docs) < 100:  # Last page
            break

        if limit and len(all_docs) >= limit:
            all_docs = all_docs[:limit]
            break

        page += 1
        await asyncio.sleep(0.1)  # Be polite to the API

    return all_docs


async def download_document_content(
    client: httpx.AsyncClient,
    doc_id: str,
) -> Optional[str]:
    """Download the full text content of a document."""
    # Try HTML format first (most complete)
    url = f"{BASE_URL}/dokument/{doc_id}"

    try:
        response = await client.get(url)
        response.raise_for_status()
        content = response.text

        # If we got XML metadata instead of content, try text format
        if "<dokumentstatus>" in content and len(content) < 5000:
            text_url = f"{BASE_URL}/dokument/{doc_id}.text"
            response = await client.get(text_url)
            response.raise_for_status()
            content = response.text

        return content

    except httpx.HTTPError:
        return None


def save_document(
    content: str,
    metadata: dict,
    search_term: str,
    output_dir: Path,
) -> Path:
    """Save document with metadata header."""
    doc_id = metadata.get("id", "unknown")
    title = metadata.get("titel", "untitled")
    date_str = metadata.get("datum", "")[:10].replace("-", "")
    doc_type = metadata.get("doktyp", "unknown")

    safe_title = sanitise_filename(title)
    filename = f"{date_str}_{doc_type}_{doc_id}_{safe_title}.txt"
    filepath = output_dir / filename

    header = f"""SEARCH TERM: {search_term}
DOCUMENT ID: {doc_id}
TITLE: {metadata.get('titel', '')}
TYPE: {doc_type}
SUBTYPE: {metadata.get('subtyp', '')}
DATE: {metadata.get('datum', '')}
PARLIAMENTARY YEAR: {metadata.get('rm', '')}
ORGANISATION: {metadata.get('organ', '')}
STATUS: {metadata.get('status', '')}
DOWNLOADED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 80}

"""

    filepath.write_text(header + content, encoding="utf-8")
    return filepath


async def download_corpus(
    dry_run: bool = False,
    limit: Optional[int] = None,
) -> dict[str, DownloadStats]:
    """
    Download the complete corpus for all document types and search terms.

    Args:
        dry_run: If True, only count documents without downloading
        limit: Maximum documents per type/term combination (for testing)

    Returns:
        Dictionary of stats per document type
    """
    stats = {doc_type: DownloadStats() for doc_type in DOCUMENT_TYPES}

    async with httpx.AsyncClient(timeout=60.0) as client:
        for doc_type, folder_name in DOCUMENT_TYPES.items():
            output_dir = DATA_DIR / folder_name
            output_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n{'=' * 60}")
            print(f"Document type: {doc_type} -> {folder_name}/")
            print(f"{'=' * 60}")

            type_docs = []

            for search_term in SEARCH_TERMS:
                print(f"\n  Searching for '{search_term}'...")

                docs = await fetch_all_documents(
                    client, search_term, doc_type, limit
                )

                # Track unique documents (avoid duplicates across search terms)
                for doc in docs:
                    doc["_search_term"] = search_term
                    if not any(d["id"] == doc["id"] for d in type_docs):
                        type_docs.append(doc)

            stats[doc_type].total_found = len(type_docs)
            print(f"\n  Total unique documents: {len(type_docs):,}")

            if dry_run:
                print("  [DRY RUN - skipping downloads]")
                continue

            # Download content
            print(f"  Downloading content...")

            for i, doc in enumerate(type_docs, 1):
                doc_id = doc.get("id", "")
                if not doc_id:
                    stats[doc_type].skipped += 1
                    continue

                # Check if already downloaded
                existing = list(output_dir.glob(f"*_{doc_id}_*.txt"))
                if existing:
                    stats[doc_type].skipped += 1
                    continue

                content = await download_document_content(client, doc_id)

                if content:
                    save_document(
                        content,
                        doc,
                        doc["_search_term"],
                        output_dir,
                    )
                    stats[doc_type].downloaded += 1
                else:
                    stats[doc_type].failed += 1

                if i % 50 == 0 or i == len(type_docs):
                    print(f"    Progress: {i:,}/{len(type_docs):,}")

                await asyncio.sleep(0.05)  # Rate limiting

    return stats


def print_summary(stats: dict[str, DownloadStats]) -> None:
    """Print download summary."""
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)

    total_found = 0
    total_downloaded = 0
    total_failed = 0
    total_skipped = 0

    for doc_type, folder_name in DOCUMENT_TYPES.items():
        s = stats[doc_type]
        print(f"\n{folder_name}/ ({doc_type}):")
        print(f"  Found:      {s.total_found:,}")
        print(f"  Downloaded: {s.downloaded:,}")
        print(f"  Skipped:    {s.skipped:,}")
        print(f"  Failed:     {s.failed:,}")

        total_found += s.total_found
        total_downloaded += s.downloaded
        total_failed += s.failed
        total_skipped += s.skipped

    print(f"\nTOTAL:")
    print(f"  Found:      {total_found:,}")
    print(f"  Downloaded: {total_downloaded:,}")
    print(f"  Skipped:    {total_skipped:,}")
    print(f"  Failed:     {total_failed:,}")

    # Calculate disk usage
    print(f"\nDisk usage:")
    for folder_name in DOCUMENT_TYPES.values():
        folder = DATA_DIR / folder_name
        if folder.exists():
            files = list(folder.glob("*.txt"))
            size_mb = sum(f.stat().st_size for f in files) / (1024 * 1024)
            print(f"  {folder_name}/: {len(files):,} files, {size_mb:.1f} MB")


async def main():
    parser = argparse.ArgumentParser(
        description="Download AI-related documents from Riksdagen"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count documents without downloading",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit documents per type/term (for testing)",
    )

    args = parser.parse_args()

    print("Riksdagen AI Discourse Corpus Downloader")
    print(f"Search terms: {SEARCH_TERMS}")
    print(f"Document types: {list(DOCUMENT_TYPES.keys())}")
    print(f"Date range: {DATE_FROM} onwards")
    print(f"Output directory: {DATA_DIR}")

    if args.dry_run:
        print("\n[DRY RUN MODE - no files will be downloaded]")

    stats = await download_corpus(
        dry_run=args.dry_run,
        limit=args.limit,
    )

    print_summary(stats)


if __name__ == "__main__":
    asyncio.run(main())
