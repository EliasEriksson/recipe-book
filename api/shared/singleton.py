class SingletonAlreadyInitializedError(Exception): ...


class Meta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        elif args or kwargs:
            raise SingletonAlreadyInitializedError()
        return cls.__instances[cls]


class Singleton(metaclass=Meta): ...
