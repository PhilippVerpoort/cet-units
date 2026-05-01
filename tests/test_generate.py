"""Tests for unit generation."""

import unittest
from pathlib import Path
from shutil import rmtree


class TestsGenerate(unittest.TestCase):
    """Tests for unit generation."""

    def test_generate(self):
        """Test unit generation."""
        from cet_units_generate._currencies import generate_units_currencies
        from cet_units_generate._emissions import generate_units_emissions
        from cet_units_generate._flows import generate_units_flows

        unit_defs_path = Path("./test-generate-tmp/")
        unit_defs_path.mkdir(parents=True)

        generate_units_currencies(unit_defs_path)
        generate_units_emissions(unit_defs_path)
        generate_units_flows(unit_defs_path)

        rmtree(unit_defs_path)
