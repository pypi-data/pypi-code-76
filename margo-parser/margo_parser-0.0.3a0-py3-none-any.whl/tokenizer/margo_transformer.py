from lark import Lark, Transformer, Tree, Token
import json
import yaml


class MargoTransformer(Transformer):
    def block(self, b):

        statements = list(filter(lambda s: s != ["ENDBLOCK"], b))

        # every other token should be an endblock
        assert len(statements) == len(b) / 2

        # a block is made up only of statements
        for s in statements:
            assert s["TYPE"] == "STATEMENT"
            assert type(s["BODY"]) == list
            assert len(s["BODY"]) < 2

        nonempty_statements = list(filter(lambda s: len(s["BODY"]) > 0, statements))

        unwrapped_statements = list(map(lambda x: x["BODY"][0], nonempty_statements))

        return {
            "SYNTAX": "MARGO",
            "TYPE": "BLOCK",
            "VERSION": "0",
            "BODY": unwrapped_statements,
        }

    def directive(self, d):
        assert len(d) == 1
        name = str(d[0])
        return {"TYPE": "DIRECTIVE", "NAME": name}

    def evf_assignment(self, c):
        assert len(c) == 3
        key = c[0]
        lang = c[1].lower().strip()
        body = c[2]
        parsed = False
        value = None

        if lang == "raw":
            value = body
            parsed = True

        if lang == "margo":
            value = body
            parsed = True

        if lang == "yaml":
            try:
                value = yaml.load(body, Loader=yaml.FullLoader)
                parsed = True
            except Exception as e:
                print(f"Error parsing YAML {body}: {e}")

        if lang == "json":
            try:
                value = json.loads(body)
                parsed = True
            except Exception as e:
                print(f"Error parsing JSON '{body}': {e}")
                pass

        return {
            "TYPE": "DECLARATION",
            "LANGUAGE": lang,
            "PARSED": parsed,
            "BODY": body,
            "NAME": key,
            "VALUE": value,
        }

    def statement(self, s: Tree):

        # # Statements should contain two items, an expression and an endblock
        # assert len(s) == 2
        # assert s[1] == ["ENDBLOCK"]
        assert type(s) == list

        return {"TYPE": "STATEMENT", "BODY": s}

    def expression(self, e: Tree):
        return {"TYPE": "EXPRESSION", "BODY": e}

    def ENDBLOCK(self, eb):
        return ["ENDBLOCK"]

    def string(self, s):
        return s[0]

    def builtin(self, s):

        assert len(s) == 1

        return {"TYPE": "BUILTIN", "BODY": s[0]}

    # def view_statement(self, v):
    #     (keys) = v
    #     return {"NAME": "view", "VIEW_LIST": v}

    def IGNORE_CELL(self, _):
        return {"NAME": "IGNORE_CELL"}

    def function(self, f):
        return ["FUNCTION", f]

    def function_name(self, fn):
        return str(fn[0])

    def argument_list(self, al):
        (s, *vals) = al
        
        return vals

    def mvf_assignment(self, kvp):
        (k, *vals) = kvp

        return self.evf_assignment([k, "json", json.dumps(vals)])  # key

    def KEY(self, k):
        return str(k)

    def false(self, _):
        return False

    def true(self, _):
        return True

    def null(self, _):
        return None

    def QSTRING(self, s):
        if len(str(s)) < 1:
            return ""
        return str(s)[1:-1]

    def value(self, v):
        return v[0]

    def number(self, n):
        (n,) = n
        try:
            return int(n.value)
        except BaseException:
            pass
        try:
            return float(n.value)
        except BaseException:
            pass
