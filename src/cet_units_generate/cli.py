import argparse
from pathlib import Path

from .emissions import generate_units_emissions
from .currencies import generate_units_currencies
from .flows import generate_units_flows


# Get default path to unit definitions.
UNIT_DEFS_PATH_DEFAULT = (
    Path(__file__).parent.parent
    / "cet_units"
    / "unit_definitions"
    / "generated"
)


def generate():
    parser = argparse.ArgumentParser(description="Generate unit definitions.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(UNIT_DEFS_PATH_DEFAULT),
        help="Directory to contain generated unit definitions (optional). "
        "Will try to determine data path of units package if no other "
        "path is provided.",
    )
    args = parser.parse_args()

    # Check that directory exists.
    unit_defs_path = Path(args.path).resolve()
    if not unit_defs_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {unit_defs_path}")

    generate_units_currencies(unit_defs_path)
    generate_units_emissions(unit_defs_path)
    generate_units_flows(unit_defs_path)
