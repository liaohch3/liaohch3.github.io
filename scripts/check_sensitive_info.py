#!/usr/bin/env python3
"""Fail the release if likely secrets or personal identifiers are present.

The scanner is intentionally conservative: it focuses on high-confidence secret
formats, common personal identifiers, credential-looking assignments, and image
metadata that can leak location/device details.

Add "sensitive-ok" to a line to intentionally allow a text finding.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TARGETS = [
    "content",
    "data",
    "static",
    "assets",
    "layouts",
    ".github/workflows",
    "hugo.toml",
    "README.md",
]

EXCLUDED_DIRS = {
    ".git",
    ".tmp",
    "docs",
    "node_modules",
    "public",
    "resources",
    "themes",
}

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".scss",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
ALLOW_MARKER = "sensitive-ok"


@dataclass(frozen=True)
class TextRule:
    name: str
    pattern: re.Pattern[str]
    description: str


@dataclass(frozen=True)
class Finding:
    path: Path
    rule: str
    description: str
    line: int | None = None
    excerpt: str | None = None


TEXT_RULES = [
    TextRule(
        "private_key_block",
        re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
        "private key material",
    ),
    TextRule(
        "aws_access_key",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
        "AWS access key id",
    ),
    TextRule(
        "github_token",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,255}\b"),
        "GitHub access token",
    ),
    TextRule(
        "openai_or_anthropic_key",
        re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}\b"),
        "OpenAI/Anthropic-style API key",
    ),
    TextRule(
        "google_api_key",
        re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
        "Google API key",
    ),
    TextRule(
        "slack_token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
        "Slack token",
    ),
    TextRule(
        "email_address",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "email address",
    ),
    TextRule(
        "cn_phone_number",
        re.compile(r"(?<!\d)(?:\+?86[-\s]?)?1[3-9]\d{9}(?!\d)"),
        "mainland China mobile phone number",
    ),
]

CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    \b(?P<key>
        password|passwd|secret|client_secret|private_key|
        api[_-]?key|access[_-]?token|auth[_-]?token|bearer[_-]?token
    )\b
    \s*[:=]\s*
    (?P<quote>["']?)
    (?P<value>[A-Za-z0-9_./+=:@!#$%^&*~?-]{12,})
    (?P=quote)
    """
)

CN_ID_RE = re.compile(
    r"(?<!\d)[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)"
)

IMAGE_METADATA_MARKERS = {
    b"Exif\x00\x00": "EXIF metadata",
    b"http://ns.adobe.com/xap/1.0/": "XMP metadata",
    b"GPSLatitude": "GPS metadata",
    b"GPSLongitude": "GPS metadata",
}


def rel(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def iter_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        path = (ROOT / target).resolve()
        if not path.exists():
            continue
        if path.is_file():
            if not is_excluded(path):
                files.append(path)
            continue
        for child in path.rglob("*"):
            if child.is_file() and not is_excluded(child):
                files.append(child)
    return sorted(files)


def is_excluded(path: Path) -> bool:
    parts = rel(path).parts
    return any(part in EXCLUDED_DIRS for part in parts)


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    try:
        sample = path.read_bytes()[:2048]
    except OSError:
        return False
    if b"\x00" in sample:
        return False
    try:
        sample.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def valid_cn_id(value: str) -> bool:
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checks = "10X98765432"
    body = value[:17]
    if not body.isdigit():
        return False
    checksum = checks[sum(int(ch) * weight for ch, weight in zip(body, weights, strict=True)) % 11]
    return value[-1].upper() == checksum


def redact_excerpt(line: str, start: int, end: int) -> str:
    before = line[:start].strip()
    after = line[end:].strip()
    excerpt = f"{before} [REDACTED] {after}".strip()
    return excerpt[:220]


def scan_text(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return [Finding(path=path, rule="read_error", description=str(exc))]

    for line_no, line in enumerate(text.splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue

        for rule in TEXT_RULES:
            for match in rule.pattern.finditer(line):
                findings.append(
                    Finding(
                        path=path,
                        line=line_no,
                        rule=rule.name,
                        description=rule.description,
                        excerpt=redact_excerpt(line, match.start(), match.end()),
                    )
                )

        for match in CREDENTIAL_ASSIGNMENT_RE.finditer(line):
            findings.append(
                Finding(
                    path=path,
                    line=line_no,
                    rule="credential_assignment",
                    description=f"credential-looking assignment to {match.group('key')}",
                    excerpt=redact_excerpt(line, match.start("value"), match.end("value")),
                )
            )

        for match in CN_ID_RE.finditer(line):
            value = match.group(0)
            if valid_cn_id(value):
                findings.append(
                    Finding(
                        path=path,
                        line=line_no,
                        rule="cn_identity_card",
                        description="mainland China identity card number",
                        excerpt=redact_excerpt(line, match.start(), match.end()),
                    )
                )
    return findings


def scan_image_metadata(path: Path) -> list[Finding]:
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        return []
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [Finding(path=path, rule="read_error", description=str(exc))]

    findings: list[Finding] = []
    for marker, description in IMAGE_METADATA_MARKERS.items():
        if marker in data:
            findings.append(Finding(path=path, rule="image_metadata", description=description))
    return findings


def format_finding(finding: Finding) -> str:
    location = str(rel(finding.path))
    if finding.line is not None:
        location = f"{location}:{finding.line}"
    detail = f"{location}: {finding.rule}: {finding.description}"
    if finding.excerpt:
        detail += f"\n  {finding.excerpt}"
    return detail


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan public blog sources for likely sensitive information.")
    parser.add_argument("paths", nargs="*", default=DEFAULT_TARGETS, help="Paths to scan, relative to repo root.")
    args = parser.parse_args()

    findings: list[Finding] = []
    for path in iter_files(args.paths):
        findings.extend(scan_image_metadata(path))
        if is_probably_text(path):
            findings.extend(scan_text(path))

    if findings:
        print("Sensitive information check failed:\n", file=sys.stderr)
        for finding in findings:
            print(format_finding(finding), file=sys.stderr)
        print(
            "\nRemove the data, strip image metadata, or add 'sensitive-ok' to an intentionally public text line.",
            file=sys.stderr,
        )
        return 1

    print(f"Sensitive information check passed ({len(iter_files(args.paths))} files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
