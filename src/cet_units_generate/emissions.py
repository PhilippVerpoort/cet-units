from pathlib import Path
from re import sub

import globalwarmingpotentials as gwp

from . import FILE_HEADER


GENERIC_DEFS = """
gram__CO2 = [ghg_emission] = g__CO2
metric_ton__CO2 = 1E+6 gram__CO2 = t__CO2

gram__CO2eq = gram__CO2 = g__CO2eq = gram__CO2_eq = g__CO2_eq = gram__CO2e = g__CO2e
metric_ton__CO2eq = 1E+6 gram__CO2eq = t__CO2eq = metric_ton__CO2_eq = t__CO2_eq = metric_ton__CO2e = t__CO2e
gram__C = gram__CO2eq * 3.6667 = g__C = gram__Ce = g__Ce
metric_ton__C = 1E+6 gram__C = t__C = metric_ton__Ce = t__Ce


"""  # noqa: E501


def _safe_ghg_label(s: str):
    return sub(r"[()-]", r"_", s).strip("_")


def generate_units_emissions(p: Path):
    # Create emissions subdirectory.
    (p / "emissions").mkdir(exist_ok=True)

    # Create list of all species.
    all_species = sorted(
        {
            _safe_ghg_label(s)
            for _, species in gwp.data.items()
            for s in species
        }
    )

    # Create generic file.
    with open(p / "emissions" / "generic.txt", "w") as file_handle_generic:
        file_handle_generic.write(FILE_HEADER)
        file_handle_generic.write(GENERIC_DEFS)

        # Write emissions data into individual files for each assessment type.
        for assessment_id, assessment_values in gwp.data.items():
            fpath = p / "emissions" / f"{assessment_id}.txt"
            with open(fpath, "w") as file_handle:
                file_handle.write(FILE_HEADER)
                file_handle.write(f"@context {assessment_id}\n")
                for species_name, species_value in assessment_values.items():
                    species_name_safe = _safe_ghg_label(species_name)
                    file_handle.write(
                        "    "  # Add indentation inside context.
                        f"gram__{species_name_safe} = "
                        f"gram__CO2eq * {species_value}\n"
                    )
                file_handle.write("@end\n")

        # Add all species to generic.
        for species_name_safe in all_species:
            file_handle_generic.write(
                f"gram__{species_name_safe} = "
                f"NaN gram__CO2 = "
                f"g__{species_name_safe}\n"
            )
            file_handle_generic.write(
                f"metric_ton__{species_name_safe} = "
                f"1E+6 gram__{species_name_safe} = "
                f"t__{species_name_safe}\n\n"
            )

        # Add import statements for all assessments.
        for assessment_id in gwp.data:
            file_handle_generic.write(f"@import {assessment_id}.txt\n")

    # Create species file.
    with open(p / "emissions" / "species.txt", "w") as file_handle_species:
        for species_name_safe in all_species:
            file_handle_species.write(species_name_safe + "\n")
