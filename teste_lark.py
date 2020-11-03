import re
import math
from lark import Lark, InlineTransformer
from typing import NamedTuple

class Symbol(NamedTuple):
    value: str


grammar = Lark(r"""
?start : expr

?expr : STRING -> string 
      | NUMBER -> number
      | ATOM -> atom
      | CHARACTER -> character
      | parent_expr
      | LPAR
      | RPAR

parent_expr : "(" ( expr ((" ")* expr)* )? ")"

NUMBER : /[-+]?\d+(\.\d*)?/
STRING: /"(([^\\"\b\n\r\f])+|\\(["\\bfnrt\/]|u[0-9a-fA-F]{4}))*"/
ATOM: /[a-zA-Z_+\-.<>=\?\*\/!:$%&~^\t\\\"][a-zA-Z_0-9+\-.<>=\?\*\/!:$%&~^\t\\\"]*/
CHARACTER: /\#\\[\w]*/
LPAR: "("
RPAR: ")"
%ignore /\s+/
%ignore LPAR
%ignore RPAR
""")


class LispyTransformer(InlineTransformer):

    def number(self, token):
        return float(token)

    def string(self, string):
        return eval(string)

    def atom(self, token):
        return Symbol(token)

exprs = [
    "(define fat (lambda (n))"
]

transformer = LispyTransformer()

for src in exprs:
    print(src)
    
    tree = grammar.parse(src)
    print(tree.pretty())
    
    result = transformer.transform(tree)
    print(result)
    
    print('-' * 40)