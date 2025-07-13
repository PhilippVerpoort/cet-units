from pathlib import Path
from re import sub

from pint import UnitRegistry


# Define unit variants to be defined for each flow.
FLOW_UNIT_VARIANTS = {
    "mass": {
        "C": ("c_ratio", "/ ({factor})"),
        "H": ("h_ratio", "/ ({factor})"),
        "O": ("o_ratio", "/ ({factor})"),
        "N": ("n_ratio", "/ ({factor})"),
    },
    "energy": {
        "LHV": ("energycontent_LHV", "/ ({factor})"),
        "HHV": ("energycontent_HHV", "/ ({factor})"),
    },
    "volume": {
        "norm": ("density_norm", "* {factor}"),
        "std": ("density_std", "* {factor}"),
    },
}


# Define units to be extended when defining flows.
FLOW_EXTEND_UNITS = {
    "mass": [
        "gram",
        "metric_ton",
        "ton",
    ],
    "energy": [
        "joule",
        "watt_hour",  # "tonne_of_coal_equivalent",
        "british_thermal_unit",
        "international_british_thermal_unit",
        "thermochemical_british_thermal_unit",
    ],
    "volume": [
        "cubic_meter",
        "cubic_foot",
        "bcm",
        "liter",
    ],
}


class CETUnitRegistry(UnitRegistry):
    _unit_defs_path: Path | None = None
    _species: list[str] = []
    _currencies: list[str] = []

    @property
    def species(self) -> list[str]:
        return self._species

    @property
    def currencies(self) -> list[str]:
        return self._currencies

    def setup_cet_defs(self, unit_defs_path: Path):
        # Store path to unit definitions directory in registry object.
        self._unit_defs_path = unit_defs_path

        # Load list of species.
        self._species = ["CO2eq", "CO2_eq", "CO2e", "C", "Ce"]
        fpath = unit_defs_path / "generated" / "emissions" / "species.txt"
        with open(fpath) as file_handle_species:
            self._species.extend(file_handle_species.read().splitlines())

        # Load list of currencies.
        fpath = unit_defs_path / "generated" / "currencies" / "currencies.txt"
        with open(fpath) as file_handle_currencies:
            self._currencies.extend(file_handle_currencies.read().splitlines())

        # Add preprocessing to registry.
        self.preprocessors.insert(len(self.preprocessors), self._preprocess)

        # Set default print format.
        self.formatter.default_format = "~P"

        # Add postprocessing to registry.
        format_orig = self.formatter.format_quantity
        self.formatter.format_quantity = (
            lambda text, spec="": self._postprocess(format_orig(text, spec))
        )

        # Load units definitions from files.
        self._on_redefinition = "ignore"  # No warning for redefining "year".
        self.load_definitions(unit_defs_path / "plain.txt")
        self._on_redefinition = "warn"
        self.load_definitions(
            unit_defs_path / "generated" / "emissions" / "generic.txt"
        )
        for p in (unit_defs_path / "generated" / "currencies").glob("*.txt"):
            if p.stem == "currencies":
                continue
            self.load_definitions(p)

    def _preprocess(self, s: str):
        if not self._species:
            return s
        return sub(
            rf"(g|t|gram|metric_ton) ({'|'.join(self._species)})", r"\1__\2", s
        )

    def _postprocess(self, s: str):
        if not self._species:
            return s
        return sub(
            rf"(g|t|gram|metric_ton)__({'|'.join(self._species)})", r"\1 \2", s
        )

    def define_flows(self, flows: tuple | list | dict):
        if isinstance(flows, tuple | list):
            if not all(isinstance(s, str) for s in flows):
                raise Exception(
                    "Elements of list must be strings referring "
                    "to loadable flow definition files."
                )
            flows = {flow_id: flow_id for flow_id in flows}
        for flow_id, flow_specs in flows.items():
            if isinstance(flow_specs, str):
                if not self._unit_defs_path:
                    raise Exception(
                        "To load existing flow definitions, the "
                        "directory must be set as a path."
                    )
                self.load_definitions(
                    self._unit_defs_path
                    / "generated"
                    / "flows"
                    / f"{flow_specs}.txt"
                )
            elif isinstance(flow_specs, dict):
                self.define(self.generate_units_defs_flow(flow_id, flow_specs))

    def generate_units_defs_flow(
        self,
        flow_id: str,
        flow_specs: dict[str, str],
        print_defs: bool = False,
    ):
        # Temporary bugfix: compatible units are not determined correctly when
        # unit registry is loaded from cache.
        self._build_cache()

        # List of definitions that will be returned.
        defs = []

        # Define base dimension and base unit.
        bu = self.Unit("gram")
        bd = bu.dimensionality
        dim = flow_specs["name"].lower().replace(" ", "_")
        defs.append(f"{bu:P}_{flow_id} = [amount_of_{dim}] = {bu:~}_{flow_id}")
        defs.append("")

        # Define units for base dimension.
        all_units = [
            unit for units in FLOW_EXTEND_UNITS.values() for unit in units
        ]
        for u in self.get_compatible_units(bd):
            if u == bu or u not in all_units:
                continue
            conv_fac = self.Quantity(f"{u:~}/{bu:~}").to_reduced_units()
            conv_fac = conv_fac.m if conv_fac.dimensionless else conv_fac
            defs.append(
                f"{u:P}_{flow_id} = "
                f"{conv_fac:.3g} * {bu}_{flow_id} = "
                f"{u:~}_{flow_id}"
            )
        defs.append("")

        # Now define new units.
        for dim, variants in FLOW_UNIT_VARIANTS.items():
            for u in FLOW_EXTEND_UNITS[dim]:
                u = self.Unit(u)
                for var, (factor, rule) in variants.items():
                    if (
                        factor not in flow_specs
                        or self.Quantity(flow_specs[factor]).m == 0.0
                    ):
                        continue
                    pattern = rule.format(factor=flow_specs[factor])
                    conv_fac = self.Quantity(
                        f"{u:~}/{bu:~} {pattern}"
                    ).to_reduced_units()
                    conv_fac = (
                        conv_fac.m if conv_fac.dimensionless else conv_fac
                    )
                    if len(variants) == 1:
                        d = (
                            f"{u:P}_{flow_id} = "
                            f"{conv_fac:.3g} * {bu:~}_{flow_id} = "
                            f"{u:~}_{flow_id}"
                        )
                    else:
                        d = (
                            f"{u:P}_{flow_id}_{var} = "
                            f"{conv_fac:.3g} * {bu:~}_{flow_id} = "
                            f"{u:~}_{flow_id}_{var}"
                        )
                    defs.append(d)
            defs.append("")

        ret = "\n".join(defs)

        if print_defs:
            print(ret)

        return ret
