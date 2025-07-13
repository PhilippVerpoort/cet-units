import unittest
from pathlib import Path
from shutil import rmtree


class TestGenerate(unittest.TestCase):
    def test_generate(self):
        from cet_units_generate.currencies import generate_units_currencies
        from cet_units_generate.emissions import generate_units_emissions
        from cet_units_generate.flows import generate_units_flows

        unit_defs_path = Path("./test-generate-tmp/")
        unit_defs_path.mkdir(parents=True)

        generate_units_currencies(unit_defs_path)
        generate_units_emissions(unit_defs_path)
        generate_units_flows(unit_defs_path)

        rmtree(unit_defs_path)
