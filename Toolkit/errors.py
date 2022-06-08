class InternalError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class NothingFoundError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class DummyError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class NotImplemented(Exception):
    def __init__(self, *args, **kwargs):
        pass


class NotActivated(Exception):
    def __init__(self, *args, **kwargs):
        pass


class InvalidAuth(Exception):
    def __init__(self, *args, **kwargs):
        pass


class NonExsistant(Exception):
    def __init__(self, *args, **kwargs):
        pass


class IndexOutOfItems(Exception):
    def __init__(self, *args, **kwargs):
        pass


class ItemNotFound(Exception):
    def __init__(self, *args, **kwargs):
        pass


class MissingArgument(Exception):
    def __init__(self, *args, **kwargs):
        pass


class FormatError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class InvalidArgument(Exception):
    def __init__(self, *args, **kwargs):
        pass


class InvalidType(Exception):
    def __init__(self, *args, **kwargs):
        pass
