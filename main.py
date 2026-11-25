#!/usr/bin/env python3
"""Deploy entry.png to the MakeFun output directory.

Standard library only, Python 3.13.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
DEFAULT_OUTPUT_DIR = "/output"
IMAGE_NAME = "entry.png"


def fail(message: str) -> "None":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_NAME)

    if not os.path.isfile(source):
        fail(f"{IMAGE_NAME} not found beside {os.path.abspath(__file__)}")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail(f"cannot read {source}: {exc}")

    if not data.startswith(PNG_SIGNATURE):
        fail(f"{source} does not start with the 8-byte PNG signature")

    if len(data) > MAX_BYTES:
        fail(f"{source} is {len(data)} bytes, over the {MAX_BYTES}-byte limit")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    target = os.path.join(output_dir, IMAGE_NAME)

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {output_dir}: {exc}")

    staged = None
    try:
        fd, staged = tempfile.mkstemp(dir=output_dir, prefix=f".{IMAGE_NAME}.", suffix=".tmp")
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(staged, 0o644)
        os.replace(staged, target)
        staged = None
    except OSError as exc:
        fail(f"cannot deploy to {target}: {exc}")
    finally:
        if staged is not None:
            try:
                os.unlink(staged)
            except OSError:
                pass

    try:
        deployed_size = os.path.getsize(target)
    except OSError as exc:
        fail(f"cannot stat deployed file {target}: {exc}")

    if deployed_size != len(data):
        fail(f"deployed size {deployed_size} != source size {len(data)}")

    try:
        with open(target, "rb") as handle:
            deployed = handle.read()
    except OSError as exc:
        fail(f"cannot read deployed file {target}: {exc}")

    if deployed != data:
        fail(f"deployed bytes in {target} do not match {source}")

    digest = hashlib.sha256(deployed).hexdigest()
    print(target)
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
