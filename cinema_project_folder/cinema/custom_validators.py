from django.core.exceptions import ValidationError


def non_negative_number(n: int) -> int:
    if n < 0:
        raise ValidationError("Should be positive.\n")
    return n


def non_zero_number(n: int) -> int:
    if n == 0:
        raise ValidationError("Should not be zero.\n")
    return n


def movie_year(n: int) -> int:
    if n < 1878:  # the first movie appeared in 1878
        raise ValidationError("Movie can't be that old(starting age 1878).\n")
    return n


def name_validate(s: str) -> str:
    s = s.strip()
    if not s.isalpha():
        raise ValidationError("Name and surename can contain only letters.\n")
    return s


def CNP_validate(s: str) -> str:
    s = s.strip()
    for c in s:
        try:
            c = int(c)
        except ValueError:
            raise ValidationError("CNP should contain only digits.\n")
    if len(s) != 13:
        raise ValidationError("CNP should contain 13 digits.\n")
    return s
