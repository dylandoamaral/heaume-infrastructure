from heaume_infrastructure.shared.write_to_influxdb.cast import (
    CastFloat,
    CastInt,
    NoCast,
)


def describe_lambda_code_cast():
    def must_cast_int():
        assert isinstance(CastInt().cast(3.7), int)

    def must_cast_float():
        assert isinstance(CastFloat().cast(3), float)

    def must_no_cast():
        assert isinstance(NoCast().cast("hi"), str)
