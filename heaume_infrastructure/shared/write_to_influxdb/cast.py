from abc import ABC


class CastType(ABC):
    def cast(self, value):
        """Cast a value to the correct type.

        :param value: The value to cast.
        :type value: any
        """


class CastInt(CastType):
    def cast(self, value):
        return int(value)


class CastFloat(CastType):
    def cast(self, value):
        return float(value)


class NoCast(CastType):
    def cast(self, value):
        return value


cast_mapping = {"float": CastFloat(), "int": CastInt()}
