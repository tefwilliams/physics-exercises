from typing import Iterable


def get_comma_separated_string(strings: Iterable[str]):
    strings = list(strings)

    return (
        strings[0]
        if len(strings) == 1
        else f"{', '.join(strings[:-1])}, and {strings[-1]}"
    )
