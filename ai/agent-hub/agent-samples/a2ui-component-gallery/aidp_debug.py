import base64
import json
import os
import threading


def _debug_enabled():
    """Keep embedded diagnostics opt-in so they never appear to end users."""
    return os.getenv("AIDP_DEBUG_ENABLED", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


class DebugLog:
    _local = threading.local()

    @classmethod
    def _entries(cls):
        if not hasattr(cls._local, "entries"):
            cls._local.entries = []
        return cls._local.entries

    @classmethod
    def log(cls, message, level="INFO", **data):
        if not _debug_enabled():
            return
        cls._entries().append({"level": level, "msg": str(message), "data": data})

    @classmethod
    def embed(cls, result):
        entries = cls._entries()
        cls._local.entries = []
        if entries:
            encoded = base64.urlsafe_b64encode(
                json.dumps(entries).encode()
            ).decode().rstrip("=")
            result.setdefault("messages", []).append(
                {"type": "system", "content": "[__aidp_debug__:" + encoded + "]"}
            )


def debug(message, **data):
    DebugLog.log(message, **data)


def debug_warn(message, **data):
    DebugLog.log(message, "WARN", **data)


def debug_error(message, **data):
    DebugLog.log(message, "ERROR", **data)
