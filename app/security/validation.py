def validate_age(age):

    if age is None:
        return False

    return (
        isinstance(age, int)
        and 0 <= age <= 120
    )


def validate_income(income):

    if income is None:
        return False

    return (
        isinstance(income, (int, float))
        and income >= 0
    )