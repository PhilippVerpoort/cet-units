from typing import Final
from pathlib import Path
from csv import reader as csv_reader

from cet_units import ureg
from cet_units_generate import FILE_HEADER


FLOWS_DATA_PATH: Final[Path] = Path(__file__).parent / "data" / "flows"

if not FLOWS_DATA_PATH.is_dir():
    raise Exception("Directory containing flow properties could not be found.")


def generate_units_flows(p: Path):
    # Create emissions subdirectory.
    (p / "flows").mkdir(exist_ok=True)

    # Load flows from files.
    for flow_path in FLOWS_DATA_PATH.glob("*.csv"):
        flow_id = flow_path.stem

        if flow_id not in ["H2", "NG", "NH3", "MeOH", "H2O"]:
            continue

        with open(flow_path) as file_stream:
            read = csv_reader(
                file_stream,
                delimiter=",",
                quotechar='"',
                strict=True,
            )
            next(read)  # Skip header line.
            flow_specs = {row[0]: row[1] for row in read}
            defs = ureg.generate_units_defs_flow(flow_id, flow_specs)

            # Create generic file.
            with open(p / "flows" / f"{flow_id}.txt", "w") as file_handle:
                file_handle.write(FILE_HEADER)
                file_handle.write(defs)
