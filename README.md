[![DOI](https://zenodo.org/badge/1019168167.svg)](https://doi.org/10.5281/zenodo.18166469)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Documentation Status](https://img.shields.io/badge/docs-online-blue)](https://philippverpoort.github.io/cet-units/latest/)
[![CI](https://github.com/PhilippVerpoort/cet-units/actions/workflows/ci.yml/badge.svg)](https://github.com/PhilippVerpoort/cet-units/actions/workflows/ci.yml)
[![Code style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-109cf5?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
![Python versions](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)

![CET Units Logo](docs/assets/logos/logo-light.svg)

# CET Units: Climate and Energy Transition Units

CET Units stands for **Climate and Energy Transition Units**. It is a Python package built on top of [pint](https://github.com/hgrecco/pint) that defines units commonly used in energy systems, industrial ecology, and climate mitigation analysis.

## Installation

You can install CET Units via `pip` directly from GitHub:

```bash
pip install git+https://github.com/PhilippVerpoort/cet-units.git
````

Or clone and install locally:

```bash
git clone https://github.com/PhilippVerpoort/cet-units.git
cd cet-units
pip install .
```

> **Note:** The package will be published on PyPI in the near future for simpler installation.

## Examples

### Currencies
Deflators and exchange rates are defined to conveniently convert currencies from current (nominal) to constant (real) values and between currencies (e.g. USD and EUR).

```python
>>> from cet_units import ureg
>>>
>>> unit_from = ureg("1 USD_2020")
>>> unit_to = unit_from.to("EUR_2024")
>>> print(f"{unit_to:.3f}")
1.098 EUR_2024
```
The deflators and exchange rates are obtained from the World Bank using the [pydeflate](https://pydeflate.readthedocs.io/) package.

### Emissions
Greenhouse-gas emission species can be converted according to a climate assessment, e.g. `ARG6GWP100` (IPCC Assessment Report 6, 100-year warming period).

```python
>>> from cet_units import ureg
>>>
>>> unit_from = ureg("1 Mt CH4")
>>> unit_to = unit_from.to("Mt CO2eq", "AR6GWP100")
>>> print(f"{unit_to:.3f}")
27.9 Mt CO2eq
```
The global-warming potentials for the different species have been taken from [globalwarmingpotentials](https://github.com/openclimatedata/globalwarmingpotentials/).

### Energy carriers
This package defines additional units for converting amounts of energy carriers between different dimensions.

```python
>>> from cet_units import ureg
>>>
>>> # Load definitions for hydrogen, natural gas, ammonia, and methanol.
>>> ureg.define_flows(["H2", "NG", "NH3", "MeOH"])
>>> unit_from = ureg("1 kg_H2")
>>> unit_to = unit_from.to("kWh_H2_LHV")
>>> print(f"{unit_to:.3f}")
33.333 kWh_H2_LHV
```

The possible dimensions for conversion are:

* `[mass]`
* `[energy]` — lower-heating value (`LHV`) and higher-heating value (`HHV`)
* `[volume]` — normal (`norm`) and standard (`std`) temperature and pressure

The conversion factors and bibliographic information for their sources are stored in [`src/cet_units_generate/data`](src/cet_units_generate/data/).

## Credits and Thanks

* Built on top of [pint](https://github.com/hgrecco/pint). Thank you to its contributors.
* Inspired by the [iam-units](https://github.com/IAMconsortium/units/) package.
* This package was developed as part of the Ariadne project with funding from the German Federal Ministry of Research, Technology and Space (grant nos. 03SFK5A, 03SFK5A0-2).

## How to cite

* To cite a release (recommended), please refer to a specific version archived on [Zenodo](https://zenodo.org/doi/10.5281/zenodo.18166469).
* To cite a specific commit, please refer to the citation information in [`CITATION.cff`](CITATION.cff) and include the commit hash.

## Licence

This project is licensed under the [MIT Licence](LICENSE).

## Documentation

Full documentation is available on [GitHub Pages](https://philippverpoort.github.io/cet-units/).
