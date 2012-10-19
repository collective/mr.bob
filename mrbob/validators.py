from .configurator import ValidationError


def boolean(value):
    """Converts value to Python boolean given values:
    y, n, yes, no, true, false, 1, 0
    """
    value = value.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise ValidationError('Value must be a boolean (y/n)')
