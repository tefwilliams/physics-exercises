def differences(list1: list[float], list2: list[float]):
    return [abs(item1 - item2) for item1, item2 in zip(list1, list2)]
