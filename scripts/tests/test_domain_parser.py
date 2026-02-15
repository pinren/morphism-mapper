#!/usr/bin/env python3

from __future__ import annotations

import sys
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "references"

sys.path.insert(0, str((ROOT / "scripts").resolve()))
from dynamic_agent_generator import DynamicAgentGenerator  # noqa: E402


class TestDomainParser(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = DynamicAgentGenerator(str(REFERENCES))

    def test_parse_all_domain_files(self) -> None:
        files = sorted(REFERENCES.glob("*_v2.md")) + sorted((REFERENCES / "custom").glob("*_v2.md"))
        self.assertGreaterEqual(len(files), 30)

        for file_path in files:
            content = file_path.read_text(encoding="utf-8")
            domain = file_path.stem.replace("_v2", "")
            knowledge = self.generator.extract_knowledge(content, domain)

            self.assertTrue(knowledge.domain_file_path.startswith("references/"))
            self.assertEqual(len(knowledge.domain_file_hash), 64)
            self.assertTrue(knowledge.fundamentals.strip())
            self.assertTrue(knowledge.core_objects.strip())
            self.assertTrue(knowledge.core_morphisms.strip())
            self.assertTrue(knowledge.theorems.strip())
            self.assertGreaterEqual(len(re.findall(r"^\s*-\s+\*\*", knowledge.core_objects, re.MULTILINE)), 10)
            self.assertGreaterEqual(len(re.findall(r"^\s*-\s+\*\*", knowledge.core_morphisms, re.MULTILINE)), 10)
            self.assertGreaterEqual(len(re.findall(r"^###\s+\d+\.\s+", knowledge.theorems, re.MULTILINE)), 10)

    def test_missing_section_raises(self) -> None:
        bad_content = """# Domain: bad\n\n## Fundamentals\n\n### 导语\nfoo\n\n## Core Objects\n\n- **A**: x\n\n## Core Morphisms\n\n- **B**: y\n"""
        with self.assertRaises(ValueError):
            self.generator.extract_knowledge(bad_content, "bad")

    def test_heading_anchor_parse_is_order_sensitive(self) -> None:
        path = sorted(REFERENCES.glob("*_v2.md"))[0]
        content = path.read_text(encoding="utf-8")
        domain = path.stem.replace("_v2", "")
        knowledge = self.generator.extract_knowledge(content, domain)

        self.assertIn("## Fundamentals", knowledge.fundamentals)
        self.assertIn("## Core Objects", knowledge.core_objects)
        self.assertIn("## Core Morphisms", knowledge.core_morphisms)
        self.assertIn("## Theorems", knowledge.theorems)


if __name__ == "__main__":
    unittest.main()
