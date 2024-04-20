import builtins
from .physics_exercise_helpers.input_helpers import input_int, input_float

# input_int

builtins.input = lambda _: "2"
assert input_int("") == 2

builtins.input = lambda _: "0"
assert input_int("") == 0

builtins.input = lambda _: "-1"
assert input_int("") == -1

builtins.input = lambda _: "100000"
assert input_int("") == 100_000

# input_float

builtins.input = lambda _: "np.pi"
assert input_float("") == 3.141592653589793

builtins.input = lambda _: "0"
assert input_float("") == 0

builtins.input = lambda _: "-1.0"
assert input_float("") == -1

builtins.input = lambda _: "2"
assert input_float("") == 2

print("All assertions passed")
