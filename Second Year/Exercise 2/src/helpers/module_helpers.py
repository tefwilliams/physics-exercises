import importlib


def get_full_module_name(module_name: str):
    match module_name:
        case "np":
            return "numpy"

        case "pd":
            return "pandas"

        case _:
            return module_name


def get_from_module(input_string: str):
    try:
        module_name, attribute_name = input_string.split(".")

    except ValueError:
        raise ValueError(f"{input_string} is not in module.attribute format")

    full_module_name = get_full_module_name(module_name)
    module = importlib.import_module(full_module_name)

    return module.__getattribute__(attribute_name)
