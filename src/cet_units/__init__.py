"""CET units package.

CET Units stands for Climate and Energy Transition Units. It is a Python
package built on top of pint. It defines units that help analysing common
problems in energy systems, industrial ecology, and climate mitigation.
"""

from pathlib import Path

from pint import set_application_registry

from .registry import CETUnitRegistry

# Define path to unit definitions.
UNIT_DEFS_PATH: Path = Path(__file__).parent / "unit_definitions"


# Create registry and load from definitions.
ureg = CETUnitRegistry()
ureg._setup_cet_defs(UNIT_DEFS_PATH)
Quantity = Q = ureg.Quantity
Unit = U = ureg.Unit


# Set application registry (e.g. used by pint_pandas).
set_application_registry(ureg)


__all__ = [
    "Q",
    "Quantity",
    "U",
    "Unit",
    "ureg",
]
