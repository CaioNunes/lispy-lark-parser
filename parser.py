import re
import math
from lark import Lark, InlineTransformer
from typing import NamedTuple

class Symbol(NamedTuple):
    value: str


grammar = Lark(r"""
?start : expr+

?quote_rule : "\'" expr+

?expr : quote start
      | STRING -> string 
      | NUMBER -> number
      | sequence
      | array
      | KEYWORD -> keyword
      | BOOLEAN -> boolean
      | CHARACTER -> character
      | ATOM -> atom

?sequence : array ((WS)? array)+

array : "(" ( expr ((" ")* expr)* )? ")"

quote: /[\']{1,2}/
KEYWORD: /(cmd|and|begin|case|cond|define|delay|do|if|else|lambda|let|let\*|letrec|or|quasiquote|quote|set!|unquote|unquote-splicing)/
NUMBER : /[-+]?\d+(\.\d*)?/
STRING: /"(([^\\"\b\n\r\f])+|\\(["\\bfnrt\/]|u[0-9a-fA-F]{4}))*"/
BOOLEAN : /(\#t|\#f)/
CHARACTER: /\#\\[\w]*/
ATOM: /[a-zA-Z_+\-.<>=\?\*\/!:$%&~^\t\\\"][a-zA-Z_0-9+\-.<>=\?\*\/!:$%&~^\t\\\"]*/
WS: /(?:\s)/
%ignore /\s+/
""")


class LispyTransformer(InlineTransformer):
    CHARS = {
        "altmode": "\x1b",
        "backnext": "\x1f",
        "backspace": "\b",
        "call": "SUB",
        "linefeed": "\n",
        "page": "\f",
        "return": "\r",
        "rubout": "\xc7",
        "space": " ",
        "tab": "\t"
    }

    def number(self, token):
        return float(token)

    def string(self, string):
        return eval(string)

    def boolean(self, token):
        if (token == '#t'):
            return True
        elif (token == '#f'):
            return False

    def atom(self, token):
        return Symbol(token)

    def quote(self, quote):
        return Symbol('quote')

    def array(self, *itens):
        return list(itens)

    def sequence(self, *itens):
        l = list(itens)
        l.insert(0, Symbol('begin'))
        return l

    def character(self, token):
        t = str(token)[2:]
        # key_list = list(self.chars.keys())
        # val_list = list(self.chars.values())
        return str(self.chars.get(t))
        # return str(token)
    
    def keyword(self, token):
        return Symbol(token)