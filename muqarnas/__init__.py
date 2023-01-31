from collections.abc import Iterable
from itertools import product
from numbers import Real
import numpy as np


class _Vector(np.ndarray):
    """Template class for Vectors. Do not directly use this class to create
    vector instances, use Vec2, Vec3, etc instead.
    """
    dim = 0

    def __complex__(self):
        return complex(self.x, self.y)

    def __str__(self):
        data = ', '.join(str(x) for x in self)
        return f"Vec{self.dim}({data})"

    def __new__(cls, *args):
        """
        1. Initialize by a single number: v = Vec3(1)
        2. Initialize by an array of length dim: v = Vec3([1, 2, 3])
        3. Initialize by `dim`: v = Vec3(1, 2, 3)
        """
        obj = np.empty(cls.dim).view(cls)
        if len(args) == 1:
            x = args[0]
            if isinstance(x, Real):
                obj.fill(x)
            elif isinstance(x, Iterable):
                if len(x) != cls.dim:
                    raise ValueError(f"Dimension not match: got an array-like of \
length {len(x)} for a {cls.dim}-D vector")
            else:
                raise ValueError(f"Invalid input for a vector: {x}")
        else:
            if len(args) != cls.dim:
                raise ValueError(f"Invalid number of arguments for a {cls.dim}D \
vector: {args}")
            obj[:] = args

        return obj


def gen_vector_swizzles(cls):
    """Add vector swizzle properties to a Vector class."""
    key_set = "xyzw"
    D = cls.dim
    valid_keys = key_set[:D]
    sw_patterns = []
    for k in range(2, 5):
        sw_patterns.extend(product(valid_keys, repeat=k))

    # We handle single character case seperately
    # Because we want arr[i] return a number, not an array of length 1.
    for index, attr in enumerate(valid_keys):
        def gen_property(attr_idx):
            def prop_getter(instance):
                return instance[attr_idx]

            def prop_setter(instance, value):
                instance[attr_idx] = value

            return property(prop_getter, prop_setter)

        prop = gen_property(index)
        setattr(cls, attr, prop)

    for pattern in sw_patterns:
        prop_key = ''.join(pattern)
        def gen_property(pattern):
            def property_getter(instance):
                d = len(pattern)
                vclass = globals()[f"Vec{d}"]
                v = instance[[valid_keys.index(ch) for ch in pattern]].view(vclass)
                return v

            def property_setter(instance, value):
                indices = [valid_keys.index(ch) for ch in pattern]
                instance[indices] = value

            prop = property(property_getter, property_setter)
            return prop

        prop = gen_property(pattern)
        setattr(cls, prop_key, prop)

    return cls


def make_vector_type(name, dimension):
    vtype = type(name, (_Vector,), {"dim": dimension})
    return gen_vector_swizzles(vtype)


def generate_vector_classes():
    for dimension in range(2, 6):
        v_class_name = f"Vec{dimension}"
        v_class = make_vector_type(v_class_name, dimension)
        module = __import__(__package__)
        setattr(module, v_class_name, v_class)
        globals()[v_class_name] = v_class


generate_vector_classes()


__all__ = [
    "Vec2", "Vec3", "Vec4", "Vec5", "make_vector_type"
    ]
