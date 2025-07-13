import unittest


class TestUnits(unittest.TestCase):
    # using the unit registry to create some standard units
    def test(self):
        # Check that importing works without failure.
        from cet_units import ureg, Q, U

        # Check that defining flows works without failure.
        ureg.define_flows(["H2", "NG", "NH3", "MeOH"])

        # Check that units can be defined without failure.
        U("USD_2005")

        # Check that conversion give correct result.
        q = Q("1 USD_2020 / kg_H2").to("EUR_2024 / MWh_H2_LHV")
        self.assertAlmostEqual(q.m, 33.0, places=0)
