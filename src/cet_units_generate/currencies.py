from pathlib import Path
from datetime import datetime

from pydeflate import deflate, set_pydeflate_path
import pandas as pd

from . import FILE_HEADER


# Define the currencies and the country GDPs used for conversion.
currencies = {
    # US Dollar based on US purchasing power.
    "USD": "USA",
    # Euro based on EMU purchasing power (currently Germany  only, because EMU
    # does not exist yet. See: https://github.com/jm-rivera/pydeflate/issues/27
    "EUR": "DEU",
    # Chinese Yuan based on Chinese purchasing power. Currently doesn't work
    # yet.
    # "CHN": "CHN",
}


# Generate unit definitions for currencies.
def generate_units_currencies(p: Path):
    # Create currencies subdirectory.
    (p / "currencies").mkdir(exist_ok=True)

    # Define place for pydeflate to save its cache files.
    set_pydeflate_path(Path(__file__).parent)

    # Define this year and the previous. The currencies will be defined up to
    # and including the last year's.
    this_year = datetime.now().year
    base_year = this_year - 2

    # Define the base currency as the first currency in the list above. All
    # currencies will be converted to the base currency via exchange rates.
    base_currency = next(iter(currencies))

    # Create a list of currencies.
    with open(p / "currencies" / "currencies.txt", "w") as file_handle:
        file_handle.write("\n".join(list(currencies)) + "\n")

    # Define units.
    for currency, country in currencies.items():
        with open(p / "currencies" / f"{currency}.txt", "w") as file_handle:
            file_handle.write(FILE_HEADER)

            # Define currency dimension if base currency. Otherwise use
            # pydeflate to generate exchange rate to base currency.
            if currency == base_currency:
                file_handle.write(f"{currency}_{base_year} = [currency]\n\n")
            else:
                # Create an empty dataframe that pydeflate will fill with a
                # conversion factor.
                df = pd.DataFrame.from_dict(
                    {
                        "iso_code": [country],
                        "period": [base_year],
                        "value": [1.0],
                    }
                )

                # Call pydeflate to generate exchange rates.
                exchange_rates = deflate(
                    df=df,
                    base_year=base_year,
                    deflator_source="world_bank",
                    deflator_method="gdp",
                    exchange_source="world_bank",
                    exchange_method=None,
                    source_currency="LCU",  # Local currency unit.
                    target_currency=base_currency,  # Target is base currency.
                    id_column="iso_code",
                    id_type="ISO3",
                    date_column="period",
                    source_column="value",  # Where to find original data.
                    target_column="conv_factor",  # Where to store new data.
                ).astype({"period": "str"})

                fstr = (
                    f"{currency}_{{period}} = "
                    f"{base_currency}_{base_year} * "
                    f"{{conv_factor}}\n\n"
                )
                exchange = fstr.format(**exchange_rates.iloc[0].to_dict())
                file_handle.write(exchange)

            # Create an empty dataframe that pydeflate will fill with
            # conversion factors.
            df = pd.DataFrame.from_dict(
                {
                    "iso_code": country,
                    "period": range(2005, base_year),
                    "value": 1.0,
                }
            )

            # Call pydeflate to generate deflators.
            deflators = deflate(
                df=df,
                base_year=base_year,
                deflator_source="world_bank",
                deflator_method="gdp",
                exchange_source="world_bank",
                exchange_method=None,
                source_currency=currency,
                target_currency=currency,
                id_column="iso_code",
                id_type="ISO3",
                date_column="period",
                source_column="value",  # Where to find original data.
                target_column="conv_factor",  # Where to store new data.
            ).astype({"period": "str"})

            # Generate list of rows and dump into definitions file.
            fstr = (
                f"{currency}_{{period}} = "
                f"{currency}_{base_year} * "
                f"{{conv_factor}}"
            )
            deflators_list = deflators.apply(
                lambda row: fstr.format(**row), axis=1
            ).tolist()
            file_handle.write("\n".join(deflators_list) + "\n")
