"""---
tags: ["draft"]
provides: []
requires: []
---"""

from pathlib import Path
import subprocess

def test_converter_runs(tmp_path):
    # create fake source file
    src = tmp_path / "src_repo"
    src.mkdir()
    (src / "hello.py").write_text("print('hi')")
    dest = tmp_path / "dss"
    subprocess.check_call([
        "python", "meta/convert_to_dss.py",
        "--source", str(src), "--dest", str(dest)
    ])
    assert (dest / "src" / "hello.py").exists()