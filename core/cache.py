import hashlib
import json
from datetime import date, datetime
from functools import wraps
from pathlib import Path


_CACHE_DIR = Path("cache")
_enabled = False
_ttl_days = 7
_mem: dict = {}  # in-process layer — survives for the duration of the run


def configure(enabled: bool, ttl_days: int = 7, cache_dir: str = "cache") -> None:
    global _enabled, _ttl_days, _CACHE_DIR
    _enabled = enabled
    _ttl_days = ttl_days
    _CACHE_DIR = Path(cache_dir)


def clear() -> None:
    _mem.clear()
    if _CACHE_DIR.exists():
        for f in _CACHE_DIR.rglob("*.json"):
            f.unlink()
        print(f"[cache] cleared {_CACHE_DIR}")


def cached(namespace: str):
    """Decorator. In-process memory layer first, then file cache, then live call."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not _enabled:
                return fn(*args, **kwargs)

            key = _make_key(namespace, args, kwargs)

            if key in _mem:
                return _mem[key]

            file_val = _read(namespace, key)
            if file_val is not None:
                _mem[key] = file_val
                return file_val

            result = fn(*args, **kwargs)
            _mem[key] = result
            _write(namespace, key, result)
            return result
        return wrapper
    return decorator


def _make_key(namespace: str, args, kwargs) -> str:
    raw = json.dumps({"a": [_serialize(a) for a in args], "k": {k: _serialize(v) for k, v in kwargs.items()}}, sort_keys=True)
    return hashlib.sha256(f"{namespace}:{raw}".encode()).hexdigest()[:16]


def _path(namespace: str, key: str) -> Path:
    return _CACHE_DIR / namespace / f"{key}.json"


def _read(namespace: str, key: str):
    p = _path(namespace, key)
    if not p.exists():
        return None
    age_days = (datetime.now().timestamp() - p.stat().st_mtime) / 86400
    if age_days > _ttl_days:
        p.unlink()
        return None
    return _deserialize(json.loads(p.read_text()))


def _write(namespace: str, key: str, value) -> None:
    p = _path(namespace, key)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_serialize(value)))


def _serialize(obj):
    from decimal import Decimal
    if isinstance(obj, dict):
        return {str(k): _serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(i) for i in obj]
    if isinstance(obj, date):
        return {"__date__": obj.isoformat()}
    if isinstance(obj, Decimal):
        return {"__decimal__": str(obj)}
    return obj


def _deserialize(obj):
    from decimal import Decimal
    if isinstance(obj, dict):
        if "__date__" in obj:
            return date.fromisoformat(obj["__date__"])
        if "__decimal__" in obj:
            return Decimal(obj["__decimal__"])
        return {k: _deserialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deserialize(i) for i in obj]
    return obj
