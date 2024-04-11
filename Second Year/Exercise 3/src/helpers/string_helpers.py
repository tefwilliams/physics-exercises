def get_comma_separated_string(strings: list[str]):
    return (
        strings[0]
        if len(strings) == 1
        else f"{', '.join(strings[:-1])}, and {strings[-1]}"
    )
