"""MkDocs build hook that packages ``cet_units`` for the browser calculator.

The calculator page (docs/calculator.md) runs `cet_units` fully client-side
via Pyodide. Since `cet_units` is not published on PyPI, a wheel is built
from the checked-out source tree at documentation-build time and injected
into the site output, together with a small generated JS file that tells
`calculator.js` which wheel file to install via micropip.
"""

import json
import subprocess
import tempfile
from pathlib import Path

from mkdocs.structure.files import File

_wheel_path: Path | None = None


def on_pre_build(*, config, **kwargs):
    global _wheel_path
    project_root = Path(config.config_file_path).parent
    out_dir = Path(tempfile.mkdtemp(prefix="cet-units-wheel-"))
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(out_dir)],
        cwd=project_root,
        check=True,
    )
    wheels = list(out_dir.glob("cet_units-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(
            f"Expected exactly one built cet_units wheel, found: {wheels}"
        )
    _wheel_path = wheels[0]


def on_files(files, /, *, config, **kwargs):
    if _wheel_path is None:
        raise RuntimeError("cet_units wheel was not built; on_pre_build did not run.")

    files.append(
        File.generated(
            config,
            f"assets/dist/{_wheel_path.name}",
            abs_src_path=str(_wheel_path),
        )
    )
    files.append(
        File.generated(
            config,
            "assets/javascripts/calculator-config.js",
            content=(
                f"window.CET_UNITS_WHEEL_FILENAME = {json.dumps(_wheel_path.name)};\n"
            ),
        )
    )
    return files
