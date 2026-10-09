#!/usr/bin/env python3
"""Validate the PavedPath Code Skill and optionally package it.

Checks follow the Agent Skills specification and Anthropic's authoring
guidance: frontmatter limits, body length, links, metadata keys, eval files,
and the repository's English-only policy.

Usage:
    python3 tools/check_skill.py             # validate
    python3 tools/check_skill.py --package   # validate, then build the packages in dist/

Packages:
    dist/pavedpath-code.zip          claude.ai upload (Customize > Skills)
    dist/pavedpath-code-plugin.zip   portable Agent Plugin (ChatGPT and Codex plugins)
"""

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("anthropic", "claude")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500
CJK_RE = re.compile("[\\u3040-\\u30ff\\u3400-\\u4dbf\\u4e00-\\u9fff\\uac00-\\ud7af\\uff00-\\uffef]")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
OPENAI_KEYS = {
    "interface": {"display_name", "short_description", "icon_small", "icon_large", "brand_color", "default_prompt"},
    "policy": {"allow_implicit_invocation"},
    "dependencies": {"tools"},
}
# Files that make up the installable Skill. Everything else is for maintainers.
SKILL_PATHS = ("SKILL.md", "LICENSE", "references")
OPENAI_PATHS = ("agents",)
VERSION_RE = re.compile(r"^## (\d+\.\d+\.\d+)\b", re.MULTILINE)
REPOSITORY = "https://github.com/riprayx/pavedpath-code"

errors = []


def fail(message):
    errors.append(message)


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md frontmatter is not closed")
        return {}, text
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or line.startswith((" ", "\t")):
            fail(f"frontmatter line is not a simple 'key: value' pair: {line!r}")
            continue
        fields[key.strip()] = value.strip()
    return fields, text[end + 5 :]


def check_frontmatter(fields):
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        fail("frontmatter: name is missing")
    elif len(name) > MAX_NAME or not NAME_RE.match(name):
        fail(f"frontmatter: name {name!r} must be 1-{MAX_NAME} lowercase letters, digits, or single hyphens")
    elif any(word in name for word in RESERVED):
        fail(f"frontmatter: name {name!r} contains a reserved word")
    if not description:
        fail("frontmatter: description is missing")
    elif len(description) > MAX_DESCRIPTION:
        fail(f"frontmatter: description is {len(description)} characters (max {MAX_DESCRIPTION})")
    if "<" in description or ">" in description:
        fail("frontmatter: description must not contain XML tags or angle brackets")
    if description[:1] in "\"'":
        fail("frontmatter: write the description unquoted on one line")
    if description and (": " in description or " #" in description or description[0] in "&*!|>%@`[]{},?-"):
        fail("frontmatter: description contains characters that break an unquoted YAML value (': ', ' #', or a leading indicator)")


def check_links(path):
    text = path.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        file_part = target.split("#", 1)[0]
        if file_part and not (path.parent / file_part).exists():
            fail(f"{path.relative_to(ROOT)}: broken link {target}")


def check_skill_links(body):
    """References must be linked directly from SKILL.md (one level deep)."""
    linked = {t.split("#", 1)[0] for t in LINK_RE.findall(body)}
    for ref in sorted((ROOT / "references").glob("*.md")):
        rel = ref.relative_to(ROOT).as_posix()
        if rel not in linked:
            fail(f"SKILL.md does not link {rel}; it would never be loaded")
        if len(ref.read_text(encoding="utf-8").splitlines()) > 100 and "## Contents" not in ref.read_text(encoding="utf-8"):
            fail(f"{rel} is over 100 lines and needs a '## Contents' section")


def check_openai_yaml():
    path = ROOT / "agents" / "openai.yaml"
    if not path.exists():
        return
    section = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key = line.strip().split(":", 1)[0]
        if indent == 0:
            section = key
            if section not in OPENAI_KEYS:
                fail(f"agents/openai.yaml:{number}: unknown top-level key {key!r}")
        elif indent == 2 and section in OPENAI_KEYS and not key.startswith("-"):
            if key not in OPENAI_KEYS[section]:
                fail(f"agents/openai.yaml:{number}: unknown key {section}.{key}")


def check_evals():
    evals_path = ROOT / "evals" / "evals.json"
    if evals_path.exists():
        data = json.loads(evals_path.read_text(encoding="utf-8"))
        ids = set()
        for case in data.get("evals", []):
            for field in ("id", "prompt", "expected_output", "assertions"):
                if field not in case:
                    fail(f"evals.json case {case.get('id')}: missing {field}")
            if case.get("id") in ids:
                fail(f"evals.json: duplicate id {case.get('id')}")
            ids.add(case.get("id"))
            for fixture in case.get("files", []):
                if not (ROOT / fixture).exists():
                    fail(f"evals.json case {case.get('id')}: missing fixture {fixture}")
    trigger_path = ROOT / "evals" / "trigger-evals.json"
    if trigger_path.exists():
        queries = json.loads(trigger_path.read_text(encoding="utf-8"))
        positives = sum(1 for q in queries if q.get("should_trigger") is True)
        negatives = sum(1 for q in queries if q.get("should_trigger") is False)
        if positives + negatives != len(queries) or not positives or not negatives:
            fail("trigger-evals.json: every entry needs should_trigger, with both true and false cases")


def tracked_text_files():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        files = [ROOT / line for line in out.splitlines()]
    except (OSError, subprocess.CalledProcessError):
        files = list(ROOT.rglob("*"))
    return [f for f in files if f.is_file() and f.suffix in {".md", ".yaml", ".yml", ".json", ".py", ".txt"}]


def check_english_only():
    for path in tracked_text_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if CJK_RE.search(line):
                fail(f"{path.relative_to(ROOT)}:{number}: CJK characters found (English-only policy)")


def release_version():
    match = VERSION_RE.search((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
    if not match:
        fail("CHANGELOG.md needs a '## X.Y.Z' heading for the current release")
        return None
    return match.group(1)


def add_tree(archive, entries, prefix):
    for entry in entries:
        source = ROOT / entry
        paths = [source] if source.is_file() else sorted(p for p in source.rglob("*") if p.is_file())
        for path in paths:
            archive.write(path, f"{prefix}{path.relative_to(ROOT).as_posix()}")


def short_description(fallback):
    path = ROOT / "agents" / "openai.yaml"
    match = re.search(r'^\s+short_description:\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.MULTILINE) if path.exists() else None
    return match.group(1) if match else fallback


def package(name, description, version):
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)

    # claude.ai expects one folder named after the Skill at the zip root.
    skill_zip = dist / f"{name}.zip"
    with zipfile.ZipFile(skill_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        add_tree(archive, SKILL_PATHS, f"{name}/")

    # Portable Agent Plugins layout: plugin.json at the root, the Skill under skills/<name>/.
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": version,
        "description": short_description(description),
        "author": {"name": "PavedPath Code contributors", "url": REPOSITORY},
        "homepage": REPOSITORY,
        "repository": REPOSITORY,
        "license": "MIT",
        "keywords": ["debugging", "github", "open-source", "research", "software-engineering"],
    }
    plugin_zip = dist / f"{name}-plugin.zip"
    with zipfile.ZipFile(plugin_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{name}/plugin.json", json.dumps(manifest, indent=2) + "\n")
        add_tree(archive, SKILL_PATHS + OPENAI_PATHS, f"{name}/skills/{name}/")

    for target in (skill_zip, plugin_zip):
        print(f"packaged {target.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", action="store_true", help="build dist/<name>.zip after validating")
    args = parser.parse_args()

    fields, body = parse_frontmatter(SKILL.read_text(encoding="utf-8"))
    check_frontmatter(fields)
    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES:
        fail(f"SKILL.md body is {body_lines} lines (max {MAX_BODY_LINES})")
    check_skill_links(body)
    for path in [SKILL, *sorted(ROOT.glob("*.md")), *sorted((ROOT / "references").glob("*.md")), *sorted(ROOT.glob("evals/*.md")), *sorted(ROOT.glob("docs/*.md"))]:
        check_links(path)
    check_openai_yaml()
    check_evals()
    check_english_only()
    version = release_version()

    if errors:
        for message in dict.fromkeys(errors):
            print(f"error: {message}")
        return 1
    print(f"ok: name={fields['name']} version={version} description={len(fields['description'])} chars body={body_lines} lines")
    if args.package:
        package(fields["name"], fields["description"], version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
