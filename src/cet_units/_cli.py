#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import sys

from cet_units import Q


class FromToParser(ArgumentParser):
    def _parse_known_args(self, arg_strings, *args, **kwargs):
        # Extract optional flags first.
        remaining_args = []
        skip_next = False
        context_value = None

        for i, arg in enumerate(arg_strings):
            if skip_next:
                skip_next = False
                continue
            if arg == "--context":
                if i + 1 >= len(arg_strings):
                    self.error("--context requires a value")
                context_value = arg_strings[i + 1]
                skip_next = True
            else:
                remaining_args.append(arg)

        # Expect the format: from X to Y.
        if (
            len(remaining_args) < 4
            or remaining_args[0] != "from"
            or "to" not in remaining_args
        ):
            self.error("Usage: from X to Y [--context CONTEXT]")

        from_index = remaining_args.index("from")
        to_index = remaining_args.index("to")

        if (
            from_index != 0
            or to_index <= from_index + 1
            or to_index >= len(remaining_args) - 1
        ):
            self.error("Usage: from X to Y [--context CONTEXT]")

        unit_from = " ".join(remaining_args[from_index + 1 : to_index])
        unit_to = " ".join(remaining_args[to_index + 1 :])

        ns = Namespace(
            unit_from=unit_from,
            unit_to=unit_to,
            context=context_value,
        )
        return ns, []


def convert():
    # Create parser.
    parser = FromToParser(
        prog="units_convert",
        description="Potsdam units converter",
        epilog="For further details, please consult the code documentation or "
        "source code.",
    )

    # Parse the arguments.
    args = parser.parse_args(sys.argv[1:])

    # Convert quantities.
    q_out = (
        Q(args.unit_from).to(args.unit_to, args.context)
        if args.context
        else Q(args.unit_from).to(args.unit_to)
    )

    # Print output.
    print(q_out)
