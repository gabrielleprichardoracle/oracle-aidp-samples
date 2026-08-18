from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SAMPLE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SAMPLE_ROOT))

from aidp_debug import DebugLog, debug  # noqa: E402


class DebugChannelTests(unittest.TestCase):
    def setUp(self):
        DebugLog._local.entries = []

    def test_debug_output_is_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            result = {"messages": [{"type": "ai", "content": "ok"}]}
            debug("hidden diagnostic")
            DebugLog.embed(result)
        self.assertEqual([{"type": "ai", "content": "ok"}], result["messages"])

    def test_debug_output_can_be_enabled_explicitly(self):
        with patch.dict(os.environ, {"AIDP_DEBUG_ENABLED": "true"}, clear=True):
            result = {"messages": [{"type": "ai", "content": "ok"}]}
            debug("diagnostic")
            DebugLog.embed(result)
        self.assertEqual("system", result["messages"][-1]["type"])
        self.assertTrue(result["messages"][-1]["content"].startswith("[__aidp_debug__:"))


if __name__ == "__main__":
    unittest.main()
