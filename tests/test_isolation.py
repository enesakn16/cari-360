from __future__ import annotations

import ast
from pathlib import Path

from demo_data import build_demo_data

ROOT = Path(__file__).resolve().parents[1]


def source_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in ROOT.glob("*.py"))


def test_no_remote_client_or_network_library() -> None:
    forbidden = {"supabase", "requests", "httpx", "urllib3", "socket", "websocket"}
    imported: set[str] = set()
    for path in ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
    assert imported.isdisjoint(forbidden)


def test_no_database_url_or_secret_markers() -> None:
    text = source_text().casefold()
    for marker in ["supabase_url", "service_role", "anon_key", "api_key", "postgresql://", "update_manifest"]:
        assert marker not in text


def test_no_branch_or_company_identity_from_production() -> None:
    text = source_text().casefold()
    for marker in ["turkmopet", "lastikgezegeni", "inegöl", "yenişehir"]:
        assert marker not in text


def test_demo_data_is_synthetic_and_stable_shape() -> None:
    data = build_demo_data()
    assert len(data["suppliers"]) >= 4
    assert len(data["customers"]) >= 4
    assert len(data["transactions"]) >= 5
    assert "branch" not in data


def test_source_compiles() -> None:
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
