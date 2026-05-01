"""Tests for unit definitions."""

import unittest


class TestsDefinitions(unittest.TestCase):
    """Tests for unit definitions."""

    def test_definitions(self):
        """Test definitions."""
        # Check that importing works without failure.
        from cet_units import Q, U, ureg

        # Check that defining flows works without failure.
        ureg.define_flows(["H2", "NG", "NH3", "MeOH"])

        # Check that currency units are defined correctly.
        U("USD_2005")

        # Check that conversion give correct result.
        q = Q("1 USD_2020 / kg_H2").to("EUR_2024 / MWh_H2_LHV")
        self.assertAlmostEqual(q.m, 33.0, places=0)
