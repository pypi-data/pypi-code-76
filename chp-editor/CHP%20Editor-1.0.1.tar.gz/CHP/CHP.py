import string
import os
from math import e, atan2, cos, sin, log, tan, radians, degrees
global cmd
global INPUT
INPUT = False

#####TYPES########################
INT        = 'INT'
FLOAT      = 'FLOAT'
STRING     = 'STRING' 
#####KEYWORDS AND IDENTIFIERS#####
IDENTIFIER = 'IDENTIFIER'
KEYWORD    = 'KEYWORD'
PLUS       = 'PLUS'
MINUS      = 'MINUS'
DIV        = 'DIV'
MUL        = 'MUL'
POW        = 'POW'
ROOT       = 'ROOT'
EQUAL      = 'EQUAL'
NEWLINE    = 'NEWLINE'
LPAREN     = 'LPAREN'
RPAREN     = 'RPAREN'
RBRACKET   = 'RBRACKET'
LBRACKET   = 'LBRACKET'
COMMA      = 'COMMA'
ARROW      = 'ARROW'
END        = 'END'
EE         = 'EE'
NE         = 'NE'
GT         = 'GT'
GTE        = 'GTE'
LT         = 'LT'
LTE        = 'LTE'
EOF        = 'EOF'
#####FUNCTIONS AND STATEMENTS#####
FUN        = 'DEF'
VAR        = 'VAR'
MOD        = 'MOD'
WHILE      = 'WHILE'
FOR        = 'FOR'
IF         = 'IF'
AND        = 'AND'
OR         = 'OR'
NOT        = 'NOT'
ELIF       = 'ELIF'
ELSE       = 'ELSE'
THEN       = 'THEN'
STEP       = 'STEP' 
RETURN     = 'RETURN'
BREAK      = 'BREAK'
CONTINUE   = 'CONTINUE'
END        = 'END' 
DIGITS     = '0123456789'
LETTERS    = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

SYMBOLS = {
    '<-': END,
    '->': ARROW,
    '==': EE,
    '!=': NE,
    '<=': LTE,
    '>=': GTE,
    '<': LT,
    '>': GT,
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': DIV,
    '^': POW,
    '#': ROOT,
    '%': MOD,
    ',': COMMA,
    '=': EQUAL,
    ';': NEWLINE,
    '(': LPAREN,
    ')': RPAREN,
    '[': LBRACKET,
    ']': RBRACKET,
    ':': THEN,
    '\n': NEWLINE
}

OPERS = '+-*/#^%<>()[]=:,;!'

KEYWORDS = [
    VAR, AND, OR, NOT,
    IF, ELIF, ELSE, THEN,
    FOR, WHILE, STEP, END,
    FUN, BREAK, CONTINUE,
    RETURN
]

def prettify(lists, headers = False, center = False):
    if headers:
        for l in range(1, len(lists)):
            lists[l].insert(0, lists[0][l - 1])
    fill = ' '
    len_lists = [len(a) for a in lists]
    len_lists.sort(reverse = True)
    max_len = len_lists[0]
    for l in range(len(lists)):
        len_cont = [len(str(a)) for a in lists[l]]
        len_cont.sort(reverse = True)
        max_cont = len_cont[0]
        for n in range(len(lists[l])):
            diff = max_cont - len(str(lists[l][n]))
            a = diff//2 if center == True else 0
            b = diff-a if center == True else diff
            lists[l][n] = fill * a + str(lists[l][n]) + fill * b
        for n in range(max_len - len(lists[l])):
            lists[l].append(fill * max_cont)
    
    for m in range(max_len):
        for l in range(len(lists)):
            print(lists[l][m], ' ', end = '')
        print('')

def string_with_arrows(text, start, end):
    result = ''
    index_start = max(text.rfind('\n', 0, start.index), 0)
    index_end = text.find('\n', index_start + 1)
    if index_end < 0: index_end = len(text)
    line_count = end.ln - start.ln + 1
    for i in range(line_count):
        line = text[index_start:index_end]
        col_start = start.col if i == 0 else 0
        col_end = end.col if i == line_count - 1 else len(line) - 1
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)
        index_start = index_end
        index_end = text.find('\n', index_start + 1)
        if index_end < 0: index_end = len(text)
    return result.replace('\t', '')

class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.return_value = None
        self.should_continue = False
        self.should_break = False

    def register(self, res):
        if res.error: self.error = res.error
        self.return_value = res.return_value
        self.should_continue = res.should_continue
        self.should_break = res.should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.return_value = value
        return self
    
    def success_continue(self):
        self.reset()
        self.should_continue = True
        return self
    
    def success_break(self):
        self.reset()
        self.should_break = True
        return self

    def should_return(self):
        return (
            self.error or
            self.return_value or
            self.should_break or 
            self.should_continue
        )

    def failure(self, error):
        self.reset()
        self.error = error
        return self
    
    def __repr__(self):
        return f'({self.value})'

class Context:
    def __init__(self, name, parent = None, parent_pos = None):
        self.name = name
        self.parent = parent
        self.parent_pos = parent_pos
        self.symbol_table = None

class SymbolTable:
    def __init__(self, parent = None):
        self.symbols = {}
        self.parent = parent
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]

class Interpreter:
    def visit(self, node, context):
        name = f'visit_{type(node).__name__}'
        method = getattr(self, name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []
        for element in node.elements:
            elements.append(res.register(self.visit(element, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.start, node.end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.start, node.end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()
        name = node.name.value if node.name else None
        body = node.body
        args = [arg.value for arg in node.args]
        func = Function(name, body, args, node.auto_return).set_context(context).set_pos(node.start, node.end)
        if node.name:
            context.symbol_table.set(name, func)
        return res.success(func)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []
        value = res.register(self.visit(node.node, context))
        if res.should_return(): return res
        value = value.copy().set_pos(node.start, node.end)
        for arg in node.args:
            args.append(res.register(self.visit(arg, context)))
            if res.should_return(): return res
        return_value = res.register(value.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.start, node.end).set_context(context)
        return res.success(return_value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        name = node.name.value
        value = res.register(self.visit(node.node, context))
        if res.should_return(): return res
        context.symbol_table.set(name, value)
        return res.success(value)

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        name = node.name.value
        value = context.symbol_table.get(name)
        if not value:
            return res.failure(
                RunTimeError(
                    node.start, node.end,
                    f"'{name}' is not defined",
                    context
                )
            )
        value = value.copy().set_pos(node.start, node.end).set_context(context)
        return res.success(value)
        
    def visit_IfNode(self, node, context):
        res = RTResult()
        for condition, expr, return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res
            if condition_value.isTrue():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if return_null else expr_value)
        if node.else_case:
            expr, return_null = node.else_case
            else_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if return_null else else_value)
        return res.success(Number.null)

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(
                node.tok.value
            ).set_context(context).set_pos(node.start, node.end)
        )
    
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []
        start = res.register(self.visit(node.start_value, context))
        if res.should_return(): return res
        end = res.register(self.visit(node.end_value, context))
        if res.should_return(): return res
        if node.step:
            step = res.register(self.visit(node.step, context))
            if res.should_return(): return res
        else:
            step = Number(1)
        i = start.value
        if step.value >= 0:
            condition = lambda: i < end.value
        else:
            condition = lambda: i > end.value

        while condition():
            context.symbol_table.set(node.name.value, Number(i))
            i += step.value
            value = res.register(self.visit(node.body, context))
            if res.should_return() and res.should_continue == False and res.should_break == False: return res
            if res.should_continue:
                continue
            if res.should_break:
                break
            elements.append(value)
        return res.success(
            Number.null if node.return_null else
            List(elements).set_context(context).set_pos(node.start, node.end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []
        while True:
            condition = res.register(self.visit(node.condition, context))
            if res.should_return(): return res
            if not condition.isTrue(): break
            value = res.register(self.visit(node.body, context))
            if res.should_return() and res.should_continue == False and res.should_break == False: return res
            if res.should_continue:
                continue
            if res.should_break:
                break
            elements.append(value)
        return res.success(
            Number.null if node.return_null else
            List(elements).set_context(context).set_pos(node.start, node.end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right, context))
        if res.should_return(): return res
        op = node.op.type
        if op == PLUS:
            result, error = left.add(right)
        elif op == MINUS:
            result, error = left.sub(right)
        elif op == MUL:
            result, error = left.mul(right)
        elif op == DIV:
            result, error = left.div(right)
        elif op == POW:
            result, error = left.exp(right)
        elif op == ROOT:
            result, error = right.exp(
                Number(1 / left.value)
            )
        elif op == MOD:
            result, error = left.mod(right)
        elif op == EE:
            result, error = left.eq(right)
        elif op == NE:
            result, error = left.ne(right)
        elif op == LT:
            result, error = left.lt(right)
        elif op == GT:
            result, error = left.gt(right)
        elif op == LTE:
            result, error = left.lte(right)
        elif op == GTE:
            result, error = left.gte(right)
        elif node.op.matches(KEYWORD, 'AND'):
            result, error = left.anded(right)
        elif node.op.matches(KEYWORD, 'OR'):
            result, error = left.ored(right)
        if error:
            return res.failure(error)
                
        return res.success(
            result.set_pos(
                node.start, node.end
            )
        )

    def visit_UniOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res
        error = None
        op = node.op.type
        if op == MINUS:
            number, error = number.mul(Number(-1))
        elif node.op.matches(KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        return res.success(
            number.set_pos(
                node.start, node.end
            )
        )

    def visit_ReturnNode(self, node, context):
        res = RTResult()
        if node.return_node:
            value = res.register(self.visit(node.return_node, context))
            if res.should_return(): return res
        else:
            value = Number.null
        return res.success_return(value)
    
    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()
    
    def visit_BreakNode(self, node, context):
        return RTResult().success_break()

class Position:
    def __init__(self, index, ln, col, fn, ftxt):
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char = None):
        self.index += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last = 0
        self.reverse_count = 0
        self.count = 0

    def register(self, res):
        self.last = res.count
        self.count += res.count
        if res.error: self.error = res.error
        return res.node
    
    def try_register(self, res):
        if res.error:
            self.reverse_count = res.count
            return None
        return self.register(res)

    def register_advance(self):
        self.count += 1
        self.last = 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.count == 0:
            self.error = error
        return self
    
    def __repr__(self):
        return f"ERROR: '{self.error}', NODE: '{self.node}'"

class Parser:
    def __init__(self, tokens):
        self.index = -1
        self.tokens = tokens
        self.advance()

    def advance(self):
        self.index += 1
        self.update_token()
        return self.current_token
    
    def reverse(self, amount = 1):
        self.index -= amount
        self.update_token()
        return self.current_token

    def update_token(self):
        if self.index >= 0 and self.index < len(self.tokens):
            self.current_token = self.tokens[self.index] 

    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    'Expected an OPERATOR'
                )
            )
        return res

    def statement(self):
        res = ParseResult()
        start = self.current_token.end.copy()

        if self.current_token.matches(KEYWORD, RETURN):
            res.register_advance()
            self.advance()
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.reverse_count)
            return res.success(ReturnNode(expr, start, self.current_token.start.copy()))
        
        if self.current_token.matches(KEYWORD, CONTINUE):
            res.register_advance()
            self.advance()
            return res.success(ContinueNode(start, self.current_token.start.copy()))

        if self.current_token.matches(KEYWORD, BREAK):
            res.register_advance()
            self.advance()
            return res.success(BreakNode(start, self.current_token.start.copy()))
        
        expr = res.register(self.expr())
        if res.error: 
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    'Expected INT, FLOAT, OPERATOR, VAR, NOT or STATEMENT'
                )
            )
        return res.success(expr)

    def statements(self):
        res = ParseResult()
        statements = []
        start = self.current_token.start.copy()
        while self.current_token.type == NEWLINE:
            res.register_advance()
            self.advance()
        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)
        more = True
        while True:
            newline_count = 0
            while self.current_token.type == NEWLINE:
                res.register_advance()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more = False
            if not more: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.reverse_count)
                more = False
                continue
            statements.append(statement)
        return res.success(
            ListNode(
                statements, 
                start,
                self.current_token.end.copy()
            )
        )

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(KEYWORD, VAR):
            res.register_advance()
            self.advance()
            if self.current_token.type != IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        'Expected Identifier'
                    )
                )
            name = self.current_token
            res.register_advance()
            self.advance()
            if self.current_token.type != EQUAL:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected '='"
                    )
                )
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(
                VarAssignNode(name, expr)
            )
        elif self.current_token.type == IDENTIFIER:
            name = self.current_token
            res.register_advance()
            self.advance()
            if self.current_token.type == EQUAL:
                res.register_advance()
                self.advance()
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(
                    VarAssignNode(name, expr)
                )
            else:
                self.reverse()
        node = res.register(self.bin_op(self.compr, ((KEYWORD, 'AND'), (KEYWORD, 'OR'))))
        if res.error: 
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    'Expected INT, FLOAT, OPERATOR, VAR, NOT or STATEMENT'
                )
            )
        return res.success(node)

    def arith(self):
        return self.bin_op(self.term, (PLUS, MINUS))

    def compr(self):
        res = ParseResult()
        if self.current_token.matches(KEYWORD, 'NOT'):
            op = self.current_token
            res.register_advance()
            self.advance()

            node = res.register(self.compr())
            if res.error: return res

            return res.success(
                UniOpNode(op, node)
            )
        node = res.register(self.bin_op(self.arith, (EE, NE, LT, GT, LTE, GTE)))
        if res.error: 
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    'Expected INT, FLOAT, IDENTIFIER or OPERATOR or NOT'
                )
            )
        return res.success(node)

    def bin_op(self, func, ops, func_b = None):
        if func_b == None:
            func_b = func
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op = self.current_token
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op, right)
        return res.success(left)

    def term(self):
        return self.bin_op(self.factor, (MUL, DIV, MOD))

    def for_expr(self):
        res = ParseResult()
        if not self.current_token.matches(KEYWORD, FOR):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    f"Expected '{FOR}'"
                )
            )
        res.register_advance()
        self.advance()
        if self.current_token.type != IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected 'IDENTIFIER'"
                )
            )
        name = self.current_token
        res.register_advance()
        self.advance()
        if self.current_token.type != EQUAL:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected '='"
                )
            )
        res.register_advance()
        self.advance() 
        start = res.register(self.expr())
        if res.error: return res
        if not self.current_token.matches(KEYWORD, THEN):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected ':'"
                )
            )
        res.register_advance()
        self.advance()
        end = res.register(self.expr())
        if self.current_token.matches(KEYWORD, THEN):
            res.register_advance()
            self.advance()
            if self.current_token.matches(KEYWORD, STEP):
                res.register_advance()
                self.advance()
                step = res.register(self.expr())
                if res.error: return res
                if self.current_token.matches(KEYWORD, THEN):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            f"Expected '{STEP}'"
                        )
                    )
            else:
                step = None
        else:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected ':'"
                )
            )
        if self.current_token.type == NEWLINE:
            res.register_advance()
            self.advance()
            body = res.register(self.statements())
            if res.error: return res
            if not self.current_token.matches(KEYWORD, END):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        f"Expected '{END}'"
                    )
                )
            res.register_advance()
            self.advance()
            return res.success(
                ForNode(
                    name, start, end, step, body, True
                )
            )
        body = res.register(self.statement())
        if res.error: return res
        return res.success(
                    ForNode(
                        name, start, end, step, body, False
                    )
                )
    
    def while_expr(self):
        res = ParseResult()  
        if not self.current_token.matches(KEYWORD, WHILE):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    f"Expected '{WHILE}'"
                )
            )
        res.register_advance()
        self.advance()
        condition = res.register(self.expr())
        if res.error: return error
        if not self.current_token.matches(KEYWORD, THEN):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected ':'"
                )
            )
        res.register_advance()
        self.advance()
        if self.current_token.type == NEWLINE:
            res.register_advance()
            self.advance()
            body = res.register(self.statements())
            if res.error: return res
            if not self.current_token.matches(KEYWORD, END):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        f"Expected '{END}'"
                    )
                )
            res.register_advance()
            self.advance()
            return res.success(
                WhileNode(
                    condition, body, True
                )
            )
        body = res.register(self.statement())
        if res.error: return res
        return res.success(
            WhileNode(condition, body, False)
        )

    def if_elif(self):
        return self.if_cases(ELIF)

    def if_else(self):
        res = ParseResult()
        else_case = None
        if self.current_token.matches(KEYWORD, ELSE):
            res.register_advance()
            self.advance()
            if self.current_token.type == NEWLINE:
                res.register_advance()
                self.advance()
                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)
                if self.current_token.matches(KEYWORD, END):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            f"Expected '{END}'"
                        )
                    )
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)
        return res.success(else_case)

    def elif_or_else(self):
        res = ParseResult()
        cases, else_case = [], None
        if self.current_token.matches(KEYWORD, ELIF):
            all_cases = res.register(self.if_elif())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_else())
            if res.error: return res
        return res.success((cases, else_case))

    def if_cases(self, keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(KEYWORD, keyword):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    f"Expected '{keyword}'"
                )
            )
        res.register_advance()
        self.advance()
        condition = res.register(self.expr())
        if res.error: return res
        if not self.current_token.matches(KEYWORD, THEN):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected ':'"
                )
            )
        res.register_advance()
        self.advance()
        if self.current_token.type == NEWLINE:
            res.register_advance()
            self.advance()
            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))
            if self.current_token.matches(KEYWORD, 'END'):
                res.register_advance()
                self.advance()
            else:
                all_cases = res.register(self.elif_or_else())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))
            all_cases = res.register(self.elif_or_else())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)
        return res.success((cases, else_case))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_cases(IF))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(
            IfNode(cases, else_case)
        )

    def list_expr(self):
        res = ParseResult()
        elements = []
        start = self.current_token.start.copy()
        if not self.current_token.type == LBRACKET:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    "Expected '['"
                )
            )
        res.register_advance()
        self.advance()
        if self.current_token.type == RBRACKET:
            res.register_advance()
            self.advance()
        else:
            elements.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected ']', INT, FLOAT, IDENTIFIER or STATEMENT"
                    )
                )
            while self.current_token.type == COMMA:
                res.register_advance()
                self.advance()
                elements.append(res.register(self.expr()))
                if res.error: return res
            if self.current_token.type != RBRACKET:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected ',' or ']'"
                    )
                )
            res.register_advance()
            self.advance()
        return res.success(ListNode(elements, start, self.current_token.end.copy()))

    def func_def(self):
        res = ParseResult()
        if not self.current_token.matches(KEYWORD, FUN):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    f"Expected '{FUN}'"
                )
            )
        res.register_advance()
        self.advance()
        if self.current_token.type == IDENTIFIER:
            name = self.current_token
            res.register_advance()
            self.advance()
            if self.current_token.type != LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected '('"
                    )
                )
        else:
            name = None
            if self.current_token.type != LPAREN:
                return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            "Expected identifier or '('"
                        )
                    )
        res.register_advance()
        self.advance()
        args = []
        if self.current_token.type == IDENTIFIER:
            args.append(self.current_token)
            res.register_advance()
            self.advance()
            while self.current_token.type == COMMA:
                res.register_advance()
                self.advance()
                if self.current_token.type != IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            "Expected 'IDENTIFIER'"
                        )
                    )
                args.append(self.current_token)
                res.register_advance()
                self.advance()
            if self.current_token.type != RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected ',' or ')'"
                    )
                )
        else:
            if self.current_token.type != RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected identifier or ')'"
                    )
                )
        res.register_advance()
        self.advance()
        if self.current_token.matches(KEYWORD, THEN):
            res.register_advance()
            self.advance()
            if self.current_token.type == NEWLINE:
                res.register_advance()
                self.advance()
                body = res.register(self.statements())
                if res.error: return res
                if not self.current_token.matches(KEYWORD, END):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            f"Expected {END}"
                        )
                    )
                res.register_advance()
                self.advance()
                return res.success(
                    FuncDefNode(name, args, body, False)
                )
            else:
                body = res.register(self.expr())
                if res.error: return res
                return res.success(
                    FuncDefNode(name, args, body, True)
                )
        else:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.start, self.current_token.end,
                    f"Expected '{THEN}'"
                )
            )

    def atom(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in (INT, FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(tok))
        elif tok.type == IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(tok))
        elif tok.type == LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                res.failure(
                    InvalidSyntaxError(
                        self.current_token.start, self.current_token.end,
                        "Expected ')' or OPERATOR"
                    )
                )
        elif tok.type == LBRACKET:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        elif tok.matches(KEYWORD, IF):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(KEYWORD, FOR):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        
        elif tok.matches(KEYWORD, WHILE):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(KEYWORD, FUN):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(
            InvalidSyntaxError(
                tok.start, tok.end,
                'Expected INT, FLOAT, OPERATOR, IDENTIFIER or STATEMENT'
            )
        )
        
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res
        if self.current_token.type == LPAREN:
            res.register_advance()
            self.advance()
            args = []
            if self.current_token.type == RPAREN:
                res.register_advance()
                self.advance()
            else:
                args.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            "Expected ')', INT, FLOAT, IDENTIFIER or STATEMENT"
                        )
                    )
                while self.current_token.type == COMMA:
                    res.register_advance()
                    self.advance()
                    args.append(res.register(self.expr()))
                    if res.error: return res
                if self.current_token.type != RPAREN:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.start, self.current_token.end,
                            "Expected ',' or ')'"
                        )
                    )
                res.register_advance()
                self.advance()
            return res.success(CallNode(atom, args))
        return res.success(atom)

    def power(self):
        return self.bin_op(self.call, (POW, ROOT), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in (PLUS, MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UniOpNode(tok, factor))

        return self.power()

class Token:
    def __init__(self, type_, value = None, start = None, end = None):
        self.type = type_
        self.value = value
        if start:
            self.start = start.copy()
            self.end = start.copy()
            self.end.advance()
        if end:
            self.end = end.copy()

    def matches(self, type_, value):
        return self.value == value and self.type == type_

    def __repr__(self):
        if self.value != None: return f'{self.type}: {self.value}'
        return f'{self.type}'

###########ERRORS##################

class Error:
    def __init__(self, start, end, name, details):
        self.name = name
        self.details = details
        self.start = start
        self.end = end

    def as_string(self):
        result = f'{self.name}: {self.details} \n'
        result += f'File {self.start.fn}, line {self.start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.start.ftxt, self.start, self.end)
        return result
    
class IllegalCharError(Error):
    def __init__(self, start, end, details):
        super().__init__(start, end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, start, end, details):
        super().__init__(start, end, 'Invalid Syntax', details)

class InvalidOperator(Error):
    def __init__(self, start, end, details):
        super().__init__(start, end, 'Invalid Operator', details)

class RunTimeError(Error):
    def __init__(self, start, end, details, context):
        super().__init__(start, end, 'Runtime Error', details)
        self.context = context

    def traceback(self):
        result = ''
        pos = self.start
        ctx = self.context
        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.name}\n' + result
            pos = ctx.parent_pos
            ctx = ctx.parent
        return 'Traceback (most recent call last):\n' + result

    def as_string(self):
        result = self.traceback()
        result += f'{self.name}: {self.details} \n'
        result += '\n\n' + string_with_arrows(self.start.ftxt, self.start, self.end)
        return result

##########VALUES##################

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, start = None, end = None):
        self.start = start
        self.end = end
        return self

    def set_context(self, context = None):
        self.context = context
        return self
    
    def add(self, other):
        return None, self.illegal_operation(other)

    def sub(self, other):
        return None, self.illegal_operation(other)

    def mul(self, other):
        return None, self.illegal_operation(other)

    def div(self, other):
        return None, self.illegal_operation(other)
    
    def mod(self, other):
        return None, self.illegal_operation(other)

    def eq(self, other):
        return None, self.illegal_operation(other)
    
    def ne(self, other):
        return None, self.illegal_operation(other)
    
    def lt(self, other):
        return None, self.illegal_operation(other)

    def lte(self, other):
        return None, self.illegal_operation(other)
    
    def gt(self, other):
        return None, self.illegal_operation(other)

    def gte(self, other):
        return None, self.illegal_operation(other)
    
    def anded(self, other):
        return None, self.illegal_operation(other)

    def ored(self, other):
        return None, self.illegal_operation(other)

    def exp(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def isTrue(self):
        return False

    def execute(self, args):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception('No Copy Method defined')

    def illegal_operation(self, other = None):
        if not other: other = self
        return RTResult(
            self.start, self.end,
            'Illegal Operation',
            self.context
        )

    def __repr__(self):
        return str(self.value)

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        elif isinstance(other, Complex):
            return Complex(self.value + other.real, other.imag).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        elif isinstance(other, Complex):
            return Complex(self.value - other.real, -other.imag).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        elif isinstance(other, Complex):
            return Complex(self.value * other.real, self.value * other.imag).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.start, other.end,
                    'Division By Zero', self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        elif isinstance(other, Complex):
            if other.real == 0 and other.imag == 0:
                return None, RunTimeError(
                    other.start, other.end,
                    'Division By Zero', self.context
                )
            a = (other.real * self.value) / (other.real ** 2 + other.imag ** 2)
            b = (-other.imag * self.value) / (other.real ** 2 + other.imag ** 2)
            return Complex(a, b).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def mod(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def eq(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value == other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def ne(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value != other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def lt(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value < other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def lte(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value <= other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def gt(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value > other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def gte(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value >= other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)
    
    def anded(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value and other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def ored(self, other):
        if isinstance(other, Number):
            return Number(
                int(self.value or other.value)
            ).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def exp(self, other):
        if isinstance(other, Number):
            if self.value == 0 and other.value == 0:
                return None, RunTimeError(
                    other.start, other.end,
                    'Indeterminated Result', self.context
                )
            return Number(self.value ** other.value).set_context(self.context), None
        elif isinstance(other, Complex):
            if other.real != 0 and other.imag != 0:
                return None, RunTimeError(
                    other.start, other.end,
                    'Indeterminated Result', self.context
                )
            else:
                a = Complex(self.value, 0)
                result = a.exp(other)[0]
                return result.copy().set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.start, other.end)

    def notted(self):
        return Number(
            1 if self.value == 0 else 0
        ).set_context(self.context), None

    def isTrue(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.start, self.end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def add(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            None, self.illegal_operation(other)
    
    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            None, self.illegal_operation(other)
    
    def div(self, other):
        if isinstance(other, Number):
            try:
                return String(self.value[other.value]), None
            except:
                return None, RunTimeError(
                    other.start, other.end,
                    f'Can´t return value at index {other.value} because is out of bounce',
                    self.context
                )
        else:
            None, self.illegal_operation(self, other)
    
    def isTrue(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.start, self.end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def add(self, other):
        new = self.copy()
        if isinstance(other, Number):
            new.elements.append(other.value)
            return new, None
        elif isinstance(other, List):
            new.elements.extend(other.elements)
            return new, None
        else:
            None, self.illegal_operation(self, other)
    
    def mul(self, other):
        if isinstance(other, Number):
            new = self.copy()
            new.elements *= other.value
            return new, None
        else:
            None, self.illegal_operation(self, other)
    
    def sub(self, other):
        if isinstance(other, Number):
            new = self.copy()
            try:
                new.elements.pop(other.value)
                return new, None
            except:
                return None, RunTimeError(
                    other.start, other.end,
                    f'Can´t remove because index {other.value} is out of bounce',
                    self.context
                )
        else:
            None, self.illegal_operation(self, other)
    
    def div(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(
                    other.start, other.end,
                    f'Can´t return value at index {other.value} because is out of bounce',
                    self.context
                )
        else:
            None, self.illegal_operation(self, other)

    
    def isTrue(self):
        return len(self.value) > 0

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.start, self.end)
        copy.set_context(self.context)
        return copy

    # def __str__(self):
    #     return f'{", ".join([str(x) for x in self.elements])}'

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

##########FUNCTIONS###############

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or '<Lambda>'
    
    def generate_context(self):
        new_context = Context(self.name, self.context, self.start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    def check_args(self, names, args):
        res = RTResult()
        if len(args) > len(names):
            return res.failure(
                RunTimeError(
                    self.start, self.end,
                    f"{len(args) - len(names)} too many args passed into {self.name}"
                )
            )
        if len(args) < len(names):
            return res.failure(
                RunTimeError(
                    self.start, self.end,
                    f"{len(names) - len(args)} too few args passed into {self.name}"
                )
            )
        return res.success(None)
    
    def populate(self, names, args, context):
        for i in range(len(args)):
            name = names[i]
            value = args[i]
            value.set_context(context)
            context.symbol_table.set(name, value)
    
    def check_and_populate(self, names, args, context):
        res = RTResult()
        res.register(self.check_args(names, args))
        if res.should_return(): return res
        self.populate(names, args, context)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body, args, auto_return):
        super().__init__(name)
        self.body = body
        self.args = args
        self.auto_return = auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        context = self.generate_context()

        res.register(self.check_and_populate(self.args, args, context))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body, context))
        if res.should_return() and res.return_value == None: return res
        return_value = (value if self.auto_return else None) or res.return_value or Number.null
        return res.success(return_value)
    
    def copy(self):
        copy = Function(self.name, self.body, self.args, self.auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.start, self.end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, args):
        res = RTResult()
        context = self.generate_context()
        name = f'execute_{self.name}'
        method = getattr(self, name, self.no_visit_method)
        res.register(self.check_and_populate(method.names, args, context))
        if res.should_return(): return res
        return_value = res.register(method(context))
        if res.should_return(): return res
        return res.success(return_value)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.start, self.end)
        return copy

    def __repr__(self):
        return f"<Built-in function {self.name}>"
    
    def execute_print(self, context):
        print(str(context.symbol_table.get('value')))
        return RTResult().success(Number.null)
    execute_print.names = ['value']

    def execute_input(self, context):
        if cmd:
            text = input()
        else:
            global INPUT
            INPUT = True
            text = 'INPUT'
        return RTResult().success(String(text))
    execute_input.names = []

    def execute_int(self, context):
        value = context.symbol_table.get('value')
        if isinstance(value, Number):
            return RTResult().success(Number(int(value.value)))
        elif isinstance(value, String):
            return RTResult().success(Number(int(float(value.value))))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    F"Cannot convert to {INT}",
                    context
                )
            )
    execute_int.names = ['value']

    def execute_dir(self, context):
        if cmd:
            n = 5
            columns = [[] for _ in range(n)]
            for f in range(len(FUNCTIONS)):
                columns[f % n] += [FUNCTIONS[f]]
            prettify(columns)
            return RTResult().success(String(''))
        else:
            result = f"PRETTIFY:{','.join(FUNCTIONS)}"
            return RTResult().success(String(result))
    execute_dir.names = []

    def execute_help(self, context):
        value = context.symbol_table.get('value')
        type_ = type(value).__name__
        if isinstance(value, Function):
            if cmd:
                print('_'*50)
                print(f"HELP: FUNCTION '{value.name}'")
                print(f"FUNCTION {value.name} takes {value.args} as arguments")
                print(f"FUNCTION {value.name} returns {value.body}")
                print('_'*50)
                return RTResult().success(String(''))
            else:
                result = f"{'_'*50}\nHELP: FUNCTION '{value.name}'\nFUNCTION {value.name} takes {value.args} as arguments\nFUNCTION {value.name} returns {value.body}\n{'_'*50}"
                return RTResult().success(String(result))
        try:
            if value.value in KEYWORDS:
                script = os.path.dirname(os.path.realpath(__file__)) + '\\HELP\\STATEMENTS\\'
                name = value.value
        except:
            if isinstance(value, (Number, String, List)):
                script = os.path.dirname(os.path.realpath(__file__)) + '\\HELP\\TYPES\\'
                name = type_
            elif isinstance(value, BuiltInFunction):
                script = os.path.dirname(os.path.realpath(__file__)) + '\\HELP\\FUNCTIONS\\'
                name = value.name
        Help = script + f'{name}.txt'
        with open(Help, 'r') as f:
            lines = f.readlines()
        result = []
        for line in lines:
            if cmd:
                print(line[:-1])
            else:
                result += [line[:-1]]
        if cmd:
            return RTResult().success(String(''))
        else:
            return RTResult().success(String('\n'.join(result)))
    execute_help.names = ['value']

    def execute_float(self, context):
        value = context.symbol_table.get('value')
        if isinstance(value, Number):
            return RTResult().success(Number(float(value.value)))
        elif isinstance(value, String):
            return RTResult().success(Number(float(value.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    F"Cannot convert to {FLOAT}",
                    context
                )
            )
    execute_float.names = ['value']

    def execute_str(self, context):
        value = context.symbol_table.get('value')
        if isinstance(value, Number):
            return RTResult().success(String(str(value.value)))
        elif isinstance(value, String):
            return RTResult().success(value)
        if isinstance(value, List):
            return RTResult().success(String(str(value.elements)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    F"Cannot convert to {FLOAT}",
                    context
                )
            )
    execute_str.names = ['value']

    def execute_cls(self, context):
        os.system('cls')
        return RTResult().success(String(''))
    execute_cls.names = []

    def execute_len(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, List):
            return RTResult().success(Number(len(variable.elements)))
        elif isinstance(variable, String):
            return RTResult().success(Number(len(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Argument must be List or String",
                    context
                )
            )
    execute_len.names = ['variable']

    def execute_log(self, context):
        variable = context.symbol_table.get('variable')
        base = context.symbol_table.get('base')
        if isinstance(variable, Number):
            if isinstance(base, Number):
                return RTResult().success(Number(log(variable.value, base.value)))
            else:
                return RTResult().failure(
                    RunTimeError(
                        self.start, self.end,
                        "Base argume must be a Number",
                        context
                    )
                )
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_log.names = ['variable', 'base']

    def execute_round(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            value = variable.value
            floor = int(value)
            value = floor + 1 if value - floor > .5 else floor
            return RTResult().success(Number(value))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_round.names = ['variable']

    def execute_cos(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(cos(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_cos.names = ['variable']

    def execute_sin(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(sin(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_sin.names = ['variable']

    def execute_tan(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(tan(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_tan.names = ['variable']

    def execute_run(self, context):
        fn = context.symbol_table.get('fn')
        if not isinstance(fn, String):
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Argument must be string",
                    context
                )
            )
        fn = fn.value
        try:
            with open(fn, 'r') as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    f'Failed to load script \ {fn}\"\n"' + str(e),
                    context
                )
            )
        _, error = run(fn, script)
        if error:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    f'Failed to finish script \ {fn}\"\n"' + error.as_string(),
                    context
                )
            )
        return RTResult().success(Number.null)
    execute_run.names = ['fn']

    def execute_ceil(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(int(variable.value) + 1))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_ceil.names = ['variable']

    def execute_floor(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(int(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_floor.names = ['variable']

    def execute_radians(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(radians(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_radians.names = ['variable']

    def execute_degrees(self, context):
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(degrees(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_degrees.names = ['variable']

    def execute_factorial(self, context):
        from math import factorial
        variable = context.symbol_table.get('variable')
        if isinstance(variable, Number):
            return RTResult().success(Number(factorial(variable.value)))
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_factorial.names = ['variable']

    def execute_trunc(self, context):
        variable = context.symbol_table.get('variable')
        digits = context.symbol_table.get('digits')
        if isinstance(variable, Number):
            if isinstance(digits, Number):
                return RTResult().success(Number(round(variable.value, ndigits = int(digits.value))))
            else:
                return RTResult().failure(
                    RunTimeError(
                        self.start, self.end,
                        "Number of digits must be a Number",
                        context
                    )
                )
        else:
            return RTResult().failure(
                RunTimeError(
                    self.start, self.end,
                    "Variable must be a Number",
                    context
                )
            )
    execute_trunc.names = ['variable', 'digits']

##########NODES###################

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.start = self.cases[0][0].start
        self.end = (self.else_case or self.cases[-1])[0].end

class ForNode:
    def __init__(self, name, start, end, step, body, return_null):
        self.name = name
        self.start_value = start
        self.end_value = end
        self.step = step
        self.body = body
        self.start = self.name.start
        self.end = body.end
        self.return_null = return_null

class WhileNode:
    def __init__(self, condition, body, return_null):
        self.condition = condition
        self.body = body
        self.start = condition.start
        self.end = body.end
        self.return_null = return_null

class VarAccessNode:
    def __init__(self, name):
        self.name = name
        self.start = name.start
        self.end = name.end
    
    def __repr__(self):
        return f'{self.name.value}'

class VarAssignNode:
    def __init__(self, name, node):
        self.name = name
        self.node = node
        self.start = name.start
        self.end = node.end

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.start = tok.start
        self.end = tok.end
    
    def __repr__(self):
        return f'{self.tok}'

class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.start = tok.start
        self.end = tok.end
    
    def __repr__(self):
        return f'{self.tok}'

class ListNode:
    def __init__(self, elements, start, end):
        self.elements = elements
        self.start = start
        self.end = end
    
    def __repr__(self):
        return str(self.elements)

class UniOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
        self.start = op.start
        self.end = node.end
    
    def __repr__(self):
        return f'({self.op}, {self.node})'

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.start = left.start
        self.end = right.end
    
    def __repr__(self):
        opers = {
            'PLUS': '+',
            'MINUS': '-',
            'MUL': '*',
            'DIV': '/',
            'EXP': '^',
            'ROOT': '#',
            'MOD': 'MOD'
        }
        # print(type(self.left), type(self.op), type(self.right))
        return f'({self.left} {opers[self.op.type]} {self.right})'

class FuncDefNode:
    def __init__(self, name, args, body, auto_return):
        self.name = name
        self.args = args
        self.body = body
        self.auto_return = auto_return
        if self.name:
            self.start = self.name.start
        elif len(self.args) > 0:
            self.start = self.args[0].start
        else:
            self.start = self.body.start
        self.end = self.body.end

class CallNode:
    def __init__(self, node, args):
        self.node = node
        self.args = args
        self.start = self.node.start
        if len(self.args) > 0:
            self.end = self.args[-1].end
        else:
            self.end = self.node.end

class ReturnNode:
    def __init__(self, return_node, start, end):
        self.return_node = return_node
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f'SHOULD RETURN: {self.return_node}'

class ContinueNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class BreakNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.fn = fn
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_identifier(self):
        id_str = ''
        start = self.pos.copy()
        while self.current_char != None and self.current_char in LETTERS + '_':
            id_str += self.current_char
            self.advance()
        if id_str == MOD:
            return Token(MOD, start = start, end = self.pos)
        type_ = KEYWORD if id_str in KEYWORDS else IDENTIFIER
        return Token(type_, id_str, start, self.pos)

    def make_digits(self):
        num_str = ''
        start = self.pos.copy()
        dot = 0
        while self.current_char != None and self.current_char in DIGITS + '.':
            if dot == 2: break
            if self.current_char == '.':
                dot += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot == 1:
            return Token(FLOAT, float(num_str), start, self.pos)
        else:
            return Token(INT, int(num_str), start, self.pos)

    def make_symbol(self):
        sym_str = ''
        start = self.pos.copy()
        breaks = [
            None, ' '
        ]
        while not self.current_char in breaks:
            if not self.current_char in OPERS: 
                break
            sym_str += self.current_char
            self.advance()
        if sym_str in SYMBOLS:
            tok = SYMBOLS[sym_str]
            if tok in KEYWORDS:
                return [Token(KEYWORD, tok, start = start, end = self.pos)], None
            else:
                return [Token(tok, start = start, end = self.pos)], None
        else:
            toks = []
            while True:
                for symbol in SYMBOLS:
                    if sym_str == '': return toks, None
                    elif sym_str[:len(symbol)] == symbol:
                        toks.append(Token(SYMBOLS[symbol], start = start, end = self.pos))
                        sym_str = sym_str[len(symbol):]

    def make_string(self):
        str_str = ''
        quote = self.current_char
        start = self.pos.copy()
        self.advance()
        while self.current_char != None and self.current_char != quote:
            str_str += self.current_char
            self.advance()
        self.advance()
        return Token(STRING, str_str, start, self.pos)

    def comment(self):
        breaks = [
            '@', None, '\n'
        ]
        self.advance()
        while not self.current_char in breaks:
            self.advance()
        self.advance()

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '@':
                self.comment()
            elif self.current_char in LETTERS + '_':
                tokens.append(self.make_identifier())
            elif self.current_char in DIGITS + '.':
                tokens.append(self.make_digits())
            elif self.current_char in ('"', "'"):
                tokens.append(self.make_string())
            else:
                tok, error = self.make_symbol()
                if error: return [], error
                tokens.extend(tok)
        tokens.append(Token(EOF, start = self.pos))
        return tokens, None
    
global_symbol_table = SymbolTable()
VARIABLES = {
    'NULL': Number(0),
    'TRUE': Number(1),
    'FALSE': Number(0),
    'e': Number(2.71828),
    'pi': Number(3.14159),
}

FUNCTIONS = [
    'PRINT', 'INPUT', 'INT',
    'FLOAT', 'STR', 'COMPLEX',
    'CLS', 'RUN', 'LEN',
    'HELP', 'FACTORIAL'
    'LOG', 'ROUND', 'COS',
    'SIN', 'TAN', 'FLOOR',
    'CEIL', 'RADIANS', 'DEGREES',
    'TRUNC', 'DIR', 'HELP'
]
for name, function in zip(VARIABLES.keys(), VARIABLES.values()):
    global_symbol_table.set(name, function) 
for function in FUNCTIONS:
    global_symbol_table.set(function, BuiltInFunction(function.lower())) 

def run(fn, text, console = True):
    global cmd
    cmd = console
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<Program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error