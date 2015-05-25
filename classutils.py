from functools import wraps


class staticproperty(object):
    """A property that takes no arguments (like a staticmethod)."""
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter()


class classproperty(object):
    """A property that takes the class as an argument (like a classmethod)."""
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter(cls)


class instantiableclassproperty(object):
    """A property that takes the class as an argument if called on the class
        and the instance as an argument if called on an instance.
    """
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        if obj is not None:
            return self.getter(obj)
        else:
            return self.getter(cls)


class instantiableclassmethod(object):
    """A method that takes the class as its first argument if called on the
        class and the instance as an argument if called on an instance.
    """
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        if obj is not None:
            def wrapper(*args, **kargs):
                return self.getter(obj, *args, **kargs)
        else:
            def wrapper(*args, **kargs):
                return self.getter(cls, *args, **kargs)

        return wrapper


def methodize(dec):
    """Wraps a function decorator so it can wrap methods."""
    def adapt(f):
        @wraps(f)
        def decorated(self, request, *args, **kargs):
            @dec
            def g(r, *a, **k):
                return f(self, r, *a, **k)

            return g(request, *args, **kargs)

        return decorated

    return adapt
