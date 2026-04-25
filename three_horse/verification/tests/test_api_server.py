from __future__ import annotations

import importlib
import os
import unittest
from pathlib import Path
import importlib.util
from unittest.mock import patch


class VerificationApiServerTests(unittest.TestCase):
    def test_default_reasoning_effort_is_supported(self) -> None:
        import galois.verification.service as service

        with patch.dict(os.environ, {}, clear=True):
            service = importlib.reload(service)
            self.assertEqual(service.CODEX_REASONING_EFFORT, "high")

    def test_legacy_reasoning_effort_values_are_normalized(self) -> None:
        from galois.verification.service import normalize_reasoning_effort

        self.assertEqual(normalize_reasoning_effort("xhigh"), "high")
        self.assertEqual(normalize_reasoning_effort("medium"), "medium")
        self.assertEqual(normalize_reasoning_effort("unknown"), "high")

    def test_build_prompt_pushes_direct_verification_work(self) -> None:
        from galois.verification.service import build_prompt

        prompt = build_prompt("run-1", "statement", "proof")
        self.assertIn("Do not read local SKILL.md files unless you are blocked", prompt)
        self.assertIn("Do not narrate your plan", prompt)
        self.assertIn("write the verification output immediately", prompt)

    def test_runtime_writes_can_be_separated_from_asset_root(self) -> None:
        import galois.verification.service as service

        repo_root = Path(__file__).resolve().parents[3]
        runtime_dir = repo_root / "projects" / "default" / "runs" / "test-verification-runtime"
        asset_dir = repo_root / "three_horse" / "verification"
        with patch.dict(
            os.environ,
            {
                "GALOIS_VERIFICATION_AGENT_DIR": str(asset_dir),
                "GALOIS_VERIFICATION_WORKDIR": str(asset_dir),
                "GALOIS_VERIFICATION_RUNTIME_DIR": str(runtime_dir),
                "GALOIS_VERIFICATION_RESULTS_DIR": str(runtime_dir / "results"),
            },
            clear=True,
        ):
            service = importlib.reload(service)
            self.assertEqual(service.WORK_DIR, asset_dir.resolve())
            self.assertEqual(service.RUNTIME_DIR, runtime_dir.resolve())
            self.assertEqual(service.RESULTS_ROOT, (runtime_dir / "results").resolve())

    def test_verification_mcp_keeps_schema_under_asset_root(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        runtime_dir = repo_root / "projects" / "default" / "runs" / "test-verification-runtime"
        asset_dir = repo_root / "three_horse" / "verification"
        module_path = asset_dir / "mcp" / "server.py"
        with patch.dict(
            os.environ,
            {
                "GALOIS_VERIFICATION_AGENT_DIR": str(asset_dir),
                "GALOIS_VERIFICATION_WORKDIR": str(asset_dir),
                "GALOIS_VERIFICATION_RUNTIME_DIR": str(runtime_dir),
                "GALOIS_VERIFICATION_RESULTS_DIR": str(runtime_dir / "results"),
            },
            clear=True,
        ):
            spec = importlib.util.spec_from_file_location("verification_mcp_server_test", module_path)
            assert spec is not None
            assert spec.loader is not None
            mcp_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mcp_server)
            self.assertEqual(mcp_server.REPO_ROOT, asset_dir.resolve())
            self.assertEqual(mcp_server.SCHEMA_PATH, (asset_dir / "schemas" / "verification_output.schema.json").resolve())
            self.assertEqual(mcp_server.MEMORY_ROOT, runtime_dir.resolve() / "memory")
            self.assertEqual(mcp_server.RESULTS_ROOT, runtime_dir.resolve() / "results")
            validation = mcp_server.validate_verification_output(
                {
                    "verification_report": {
                        "summary": "looks good",
                        "critical_errors": [],
                        "gaps": [],
                    },
                    "verdict": "correct",
                    "repair_hints": "",
                }
            )
            self.assertTrue(validation["valid"], validation["errors"])

    def test_agents_contract_discourages_skill_file_roundtrips_and_meta_logging(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        self.assertIn("Do not open local `SKILL.md` files just to restate their instructions.", text)
        self.assertIn("Do not narrate your plan or verification workflow.", text)
        self.assertIn("Do not emit per-lemma bookkeeping to memory unless it is needed", text)


if __name__ == "__main__":
    unittest.main()
