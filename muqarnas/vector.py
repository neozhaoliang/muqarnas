from collections.abc import Iterable
from itertools import product
from numbers import Real
import numpy as np


def gen_vector_swizzles(cls):
    """Add vector swizzle properties to a Vector class."""
    key_set = "xyzwt"
    D = cls.dim
    valid_keys = key_set[:D]
    sw_patterns = []
    for k in range(1, D + 1):
        sw_patterns.extend(product(valid_keys, repeat=k))

    for pattern in sw_patterns:

        def gen_property(pattern):
            prop_key = ''.join(pattern)

            def property_getter(instance):
                return instance[[valid_keys.index(ch) for ch in pattern]]

            def property_setter(instance, value):
                indices = [valid_keys.index(ch) for ch in pattern]
                instance[indices] = value

            prop = property(property_getter, property_setter)
            return prop_key, prop

        prop_key, prop = gen_property(pattern)
        setattr(cls, prop_key, prop)

    return cls


def VectorType(dimension, dt):

    @gen_vector_swizzles
    class Vector(np.ndarray):
        """Template class for Vectors. Do not directly use this class to create
        vector instances, use Vec2, Vec3, etc instead.
        """
        dim = dimension

        def __new__(cls, *args):
            if len(args) == 1:
                x = args[0]
                if isinstance(x, Real):
                    arr = [x] * dimension
                elif isinstance(x, Iterable):
                    if len(x) != dimension:
                        raise ValueError("Dimension not match: Cannot use the \
array-like object {x} of length {len(x)} to initialize a \
{dimension}-D vector")
                    arr = x
                else:
                    raise ValueError(f"Unrecognized argument for Vector: {x}")

            else:
                arr = []
                for x in args:
                    if isinstance(x, Iterable):
                        arr.extend(x)
                    elif isinstance(x, Real):
                        arr.append(x)
                    else:
                        raise ValueError(f"Unrecognized argument for Vector: {x}")

                if len(arr) != dimension:
                    raise RuntimeError(f"Dimension not match: got {len(arr)} \
input for {dimension}-D Vector")

            return np.array(arr, dt).view(cls)

    return Vector


Vec2 = VectorType(2, float)
Vec3 = VectorType(3, float)
Vec4 = VectorType(4, float)
Vec5 = VectorType(5, float)


__all__ = ["Vec2", "Vec3", "Vec4", "Vec5"]
