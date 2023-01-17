import numpy as np
from collections.abc import Iterable


_epsilon = 1e-12


def make_vector_type(dim , dtype):
    def _gen_vector(*args):
        # initialize by a scalar or an array-like
        if len(args) == 1:
            x = args[0]
            if np.isscalar(x):
                arr = [x] * dim
            else:
                arr = x
        # initialize by a list of scalars or array-like objects
        else:
            arr = []
            for x in args:
                if isinstance(x, Iterable):
                    arr.extend(x)
                else:
                    arr.append(x)

            if len(arr) != dim:
                raise RuntimeError(f"Invalid input for a {dim}-dimensional vector: {args}")

        return np.array(arr, dtype=dtype)
    return _gen_vector


vec2 = make_vector_type(2, float)

vec3 = make_vector_type(3, float)

vec4 = make_vector_type(4, float)

ivec2 = make_vector_type(2, int)

ivec3 = make_vector_type(3, int)

ivec4 = make_vector_type(4, int)


__all__ = ['vec2', 'vec3', 'vec4', 'ivec2', 'ivec3', 'ivec4']