## build lexical analyzer
## import  the Lexical.py file to this file
from pygments import lex
import Lexical
from Livin import Lexer, My_AND, My_ASSIGN, My_DEC, My_DIV, My_EQ, My_GT, My_GTE, My_INT, My_LPAREN, My_LT, My_LTE, My_MINUS, My_MUL, My_NOT, My_OR, My_PLUS, My_RPAREN, My_SEMI

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'LPAREN',
    'RPAREN',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'PRINT',
    'ASSIGN',
    'ID',
    'SEMI',
            'COMMA',
    'COLON',
    'LBRACE',
    'RBRACE',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQ',
    'NEQ',
    'AND',
    'OR',
    'NOT',
    'INC',
    'DEC',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'REM',
    'REMASSIGN',
)

# Regular expression rules for simple tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MUL     = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_IF      = r'if'
t_ELSE    = r'else'
t_WHILE   = r'while'
t_FOR     = r'for'
t_PRINT   = r'print'
t_ASSIGN  = r'='
t_SEMI    = r';'
t_COMMA   = r','
t_COLON   = r':'
t_LBRACE  = r'{'
t_RBRACE  = r'}'
t_LT      = r'<'
t_GT      = r'>'
t_LTE     = r'<='
t_GTE     = r'>='
t_EQ      = r'=='
t_NEQ     = r'!='
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_INC     = r'\+\+'
t_DEC     = r'--'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_REM      = r'%'
t_REMASSIGN = r'%='


# A regular expression rule with some action code

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Define a rule so we can track line numbers

def t_newline(t): 
    r'\
'    
    t.lexer.lineno += len(t.value)
    
# A string containing ignored characters (spaces and tabs)

t_ignore  = ' \t'

# Error handling rule

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer

lexer = lex.lex()

# Test it out

data = ''' 
3 + 4 * 10 + 22 * 2
'''

# Give the lexer some input

lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
    

# Path: Parser.py
# Compare this snippet from Livin.py:

class Parser: 
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.advance()
        
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        return self.current_token
    
    def parse(self):
        result = self.expr()
        return result
    
    def factor(self):
        token = self.current_token
        if token.type == My_NUMBER: 
            self.advance()
            return NumberNode(token)
        elif token.type == My_LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type == My_RPAREN:
                self.advance()
                return result
            else:
                return None
        elif token.type == My_ID:
            self.advance()
            return VarAccessNode(token)
        else:
            return None
        
    def term(self):
        result = self.factor()
        while self.current_token.type in (My_MUL, My_DIV):
            token = self.current_token
            if token.type == My_MUL:
                self.advance()
                result = BinOpNode(result, token, self.factor())
            elif token.type == My_DIV:
                self.advance()
                result = BinOpNode(result, token, self.factor())
        return result
    

    
    def expr(self):
        result = self.term()
        while self.current_token.type in (My_PLUS, My_MINUS):
            token = self.current_token
            if token.type == My_PLUS:
                self.advance()
                result = BinOpNode(result, token, self.term())
            elif token.type == My_MINUS:
                self.advance()
                result = BinOpNode(result, token, self.term())
        return result
    
    def comparison(self):
        result = self.expr()
        while self.current_token.type in (My_LT, My_GT, My_LTE, My_GTE, My_EQ, My_EQ):
            token = self.current_token
            if token.type == My_LT:
                self.advance()
                result = BinOpNode(result, token, self.expr())
            elif token.type == My_GT:
                self.advance()
                result = BinOpNode(result, token, self.expr())
            elif token.type == My_LTE:
                self.advance()
                result = BinOpNode(result, token, self.expr())
            elif token.type == My_GTE:
                self.advance()
                
    
            return result
        

    
    
    def logic(self):
        result = self.comparison()
        while self.current_token.type in (My_AND, My_OR, My_NOT):
            token = self.current_token
            if token.type == My_AND:
                self.advance()
                result = BinOpNode(result, token, self.comparison())
            elif token.type == My_OR:
                self.advance()
                result = BinOpNode(result, token, self.comparison())
            elif token.type == My_NOT:
                self.advance()
                result = BinOpNode(result, token, self.comparison())
        return result
    
    
    def statement(self):
        result = self.logic()
        while self.current_token.type in (My_SEMI):
            token = self.current_token
            if token.type == My_SEMI:
                self.advance()
                result = BinOpNode(result, token, self.logic())
        return result 
    
    def assignment(self):
        result = self.statement()
        while self.current_token.type in My_ASSIGN:
            token = self.current_token
            if token.type == My_ASSIGN:
                self.advance()
                result = BinOpNode(result, token, self.statement())
        return result
    
    def increment(self):
        result = self.assignment()
        while self.current_token.type in (My_INC):
            token = self.current_token
            if token.type == My_INT:
                self.advance()
                result = BinOpNode(result, token, self.assignment())
        return result
    
    def decrement(self):
        result = self.increment()
        while self.current_token.type in (My_DEC):
            token = self.current_token
            if token.type == My_DEC:
                self.advance()
                result = BinOpNode(result, token, self.increment())
        return result
    
    def var_decl(self):
        result = self.decrement()
        while self.current_token.type in (My_VAR):
            token = self.current_token
            if token.type == My_VAR:
                self.advance()
                result = BinOpNode(result, token, self.decrement())
        return result
    
    def var_assign(self):
        result = self.var_decl()
        while self.current_token.type in (My_VAR):
            token = self.current_token
            if token.type == My_VAR:
                self.advance()
                result = BinOpNode(result, token, self.var_decl())
        return result
    
    def var_inc(self):
        result = self.var_assign()
        while self.current_token.type in (My_VAR):
            token = self.current_token
            if token.type == My_VAR:
                self.advance()
                result = BinOpNode(result, token, self.var_assign())
        return result


class BinOpNode: 
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        
    def __repr__(self):
        return '({left} {op} {right})'.format(
            left=self.left, op=self.op, right=self.right)
        
class NumberNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __repr__(self):
        return '({value})'.format(value=self.value)

class VarAccessNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __repr__(self):
        return '({value})'.format(value=self.value)
    
class VarDeclNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __repr__(self):
        return '({value})'.format(value=self.value)
    
class VarAssignNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __repr__(self):
        return '({value})'.format(value=self.value)
    
class VarIncNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
    def __repr__(self):
        return '({value})'.format(value=self.value)
    
class VarDecNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value 
        
    def __repr__(self):
        return '({value})'.format(value=self.value)
    
class tree ():
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        
    def __repr__(self):
        return '({left} {op} {right})'.format(
            left=self.left, op=self.op, right=self.right)
        
class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        
    def error(self):
        raise Exception('Invalid character')
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit():
                return Token(My_INT, self.integer())
            
            if self.current_char.isalpha():
                return Token(My_ID, self.identifier())
            
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
    
LexicalAnalyzer = Lexer('Regular_grammer.txt')
parser = Parser(LexicalAnalyzer)
tree = parser.parse()
print(tree)


#
    

##I am getting the following error:

