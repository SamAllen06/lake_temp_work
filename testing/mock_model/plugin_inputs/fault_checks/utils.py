def is_positive(values: list[float]) -> bool:
    failing_values: list[float] = []

    for value in values:
        if value <= 0.0:
            failing_values.append(value)

    if failing_values:
        return False
    return True
