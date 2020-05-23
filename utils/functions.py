# DEPRECATED, changed to NOT operator
def nope(func):
    def not_func(*args, **kwargs):
        return not func(*args, **kwargs)
    return not_func
