---
hide:
  - navigation
---

<p align="center">
  <img src="assets/logos/logo-light.svg" class="only-light" alt="CET Units Header Logo" style="max-width: 600px; width: 100%; margin-bottom: 20px;">
  <img src="assets/logos/logo-dark.svg" class="only-dark" alt="CET Units Header Logo" style="max-width: 600px; width: 100%; margin-bottom: 20px;">
</p>


# CET Units: Climate and Energy Transition Units

[![DOI](https://zenodo.org/badge/1019168167.svg)](https://doi.org/10.5281/zenodo.18166469)
[![Licence: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/PhilippVerpoort/cet-units/blob/main/LICENSE.md)
[![Documentation Status](https://img.shields.io/badge/docs-online-blue)](https://philippverpoort.github.io/cet-units/latest/)
[![CI](https://github.com/PhilippVerpoort/cet-units/actions/workflows/ci.yml/badge.svg)](https://github.com/PhilippVerpoort/cet-units/actions/workflows/ci.yml)
[![Code style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-109cf5?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
![Python versions](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)

CET Units stands for **Climate and Energy Transition Units**. It is a Python package built on top of [pint](https://github.com/hgrecco/pint). It defines units that help analysing common problems in energy systems, industrial ecology, and climate mitigation.

## Installation

Install via pip:

```bash
pip install git+https://github.com/PhilippVerpoort/cet-units.git
```

> **Note:** The package will be published on PyPI in the near future for simpler installation.

## Basic Functionality

CET Units extends pint with specialised units for climate and energy transition analysis and modelling.

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

### Emissions
Greenhouse-gas emission species can be converted according to a climate assessment, e.g. `AR6GWP100` (IPCC Assessment Report 6, 100-year warming period).

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

## Credits and Thanks

* Developed by [P.C. Verpoort](https://philipp.verpoort.online) at the [Potsdam Institute for Climate Impact Research (PIK)](https://www.pik-potsdam.de/).
* Built on top of [pint](https://github.com/hgrecco/pint). Thank you to its contributors.
* Inspired by the [iam-units](https://github.com/IAMconsortium/units/) package.
* This package was developed as part of the Ariadne project with funding from the German Federal Ministry of Research, Technology and Space (grant nos. 03SFK5A, 03SFK5A0-2).
