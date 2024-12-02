from dataclasses import dataclass
from typing import Callable

import starlark
from attrs import define
from pydantic import BaseModel


@dataclass
class Point:
    x: float
    y: float

@dataclass
class Test:
    a: Callable

@define
class AttrsTest:
    a: int
    b: list[str]

class User(BaseModel):
    id: int
    name: str = 'John Doe'


mod = starlark.Module()
glb = starlark.Globals.standard()

p = Point(x=1, y=2)
t = Test(lambda x: x * x)
a = AttrsTest(a=3, b=['x', 'y'])
u = User(id=123)

mod['p'] = p
mod['t'] = t
mod['a'] = a
mod['u'] = u

code = """
p.x + p.y * t.a(3) - (a.a if 'x' in a.b else 0) + u.id
"""

ast = starlark.parse("test.star", code)

# ast.lint()

print(starlark.eval(mod, ast, glb))
