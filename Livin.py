#<start> ::= <statement> | <statement> <start>
#<statement> ::= <if> | <while> | <assign> | <print> | <block>
#<if> ::= if <condition> then <start> else <start> end
#<while> ::= while <condition> do <start> end
#<condition> ::= <expression> <comparator> <expression>
#<comparator> ::= < | > | <= | >= | == | !=
#<assign> ::= <variable> = <expression>
#<print> ::= print <expression>



DIGITS = '0123456789'

## INT 
My_INT = 'INT'
## PLUS
My_PLUS = 'PLUS'
## MINUS
My_MINUS = 'MINUS'

## MUL
My_MUL = 'MUL'
## DIV
My_DIV = 'DIV'
## LPAREN
My_LPAREN = 'LPAREN'
## RPAREN   
My_RPAREN = 'RPAREN'
## IF 
My_IF = 'UGH'
## ELSE
My_ELSE = 'THEN'
## WHILE
My_WHILE = 'SO'

My_ID = 'ID'

My_EOF = 'EOF'
My_LT = 'LT'
My_GT   = 'GT'
My_LTE  = 'LTE'
My_GTE  = 'GTE'
My_EQ   = 'EQ'
My_NE = 'NEQ'

My_AND='AND'
My_OR= 'OR'
My_NOT= 'NOT'
My_SEMI = 'SEMI'
My_ASSIGN = 'ASSIGN'
My_INC = 'INC'
My_DEC = 'DEC'
#######
##CREATE ERRORS
###
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__('Invalid Syntax', details)
        
class ExpectedCharError(Error):
    def __init__(self, details):
        super().__init__('Expected Character', details)
        
class InvalidVariableName(Error):
    def __init__(self, details):
        super().__init__('Invalid Variable Name', details)
        
class InvalidNumber(Error):
    def __init__(self, details):
        super().__init__('Invalid Number', details)

       



class Token: 
    def __init__(self, type, value = None,pos_start = None, pos_end = None):
        self.type = type
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end


    def __repr__(self):
        return f'{self.type}:{self.value}'
    

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] 
        self.advance()
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1: 
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
            
    def make_tokens(self): 
    
        tokens = []
        while self.current_char != None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char  in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token (My_PLUS, '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token (My_MINUS, '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token (My_MUL, '*'))
                self.advance()
                
            elif self.current_char == '/':
                tokens.append(Token (My_DIV, '/'))
                self.advance()
                
            elif self.current_char == '(':
                tokens.append(Token (My_LPAREN, '('))
                self.advance()
                
            elif self.current_char == ')':
                tokens.append(Token (My_RPAREN, ')'))
                self.advance()
                
            elif self.current_char == 'i':
                tokens.append(Token (My_IF, 'i'))
                self.advance()
                
            elif self.current_char == 'e':
                tokens.append(Token (My_ELSE, 'e'))
                self.advance()
                
            elif self.current_char == 'w':
                tokens.append(Token (My_WHILE, 'w'))
                self.advance()
                
            elif self.current_char == 'f':
                tokens.append(Token (My_IF, 'f'))
                self.advance()
            
### regrextion for if else while
            elif self.current_char == 'i' and self.text[self.pos + 1] == 'f':
                tokens.append(Token (My_IF, 'i'))
                self.advance()
                self.advance()
            
            elif self.current_char == 'e' and self.text[self.pos + 1] == 'l' and self.text[self.pos + 2] == 's' and self.text[self.pos + 3] == 'e':
                tokens.append(Token (My_ELSE, 'e'))
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                
            elif self.current_char == 'w' and self.text[self.pos + 1] == 'h' and self.text[self.pos + 2] == 'i' and self.text[self.pos + 3] == 'l' and self.text[self.pos + 4] == 'e':
                tokens.append(Token (My_WHILE, 'w'))
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
            
   
            else:
                raise Exception('Invalid character')
        return tokens , None
    
    ## def make number without float 
    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        if dot_count > 1:
            raise Exception('Invalid syntax')
        return Token(My_INT, int(num_str))

class Parser_result:
    def __init__(self):
        self.error = None
        self.node = None
        
    def register(self, res):
        if res.error:
            self.error = res.error
        return res.node
    
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
    
    



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self):
        res = self.expr()
        if self.current_token.type != My_EOF:
            return None, InvalidSyntaxError()
        return res, None
    
    def factor(self):
        res = Parser_result()
        token = self.current_token
        if token.type in (My_PLUS, My_MINUS):
            res.register(self.advance())
            node = UnaryOp(token, self.factor())
            return res.success(node) 
        
        elif token.type == My_INT:
            self.advance()
            return Num(token)
        elif token.type == My_LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type == My_RPAREN:
                self.advance()
                return node
            else:
                return None, InvalidSyntaxError()
        elif token.type == My_ID:
            self.advance()
            return VarAccess(token)
        return None, InvalidSyntaxError()
    
    def term(self):
        res = Parser_result()
        return self.bin_op(self.factor, (My_MUL, My_DIV))
    
    def expr(self):
        return self.bin_op(self.term, (My_PLUS, My_MINUS))
    
    def bin_op(self, func, ops):
        res = Parser_result()
        left = func()
        if left == None:
            return None, InvalidSyntaxError()
        while self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            if right == None:
                return None, InvalidSyntaxError()
            left = BinOp(left, op_token, right)
        return left
    
    def parse(self):
        res = self.expr()
        if self.current_token.type != My_EOF:
            return None, InvalidSyntaxError()
        return res, None
    
    def factor(self):
        token = self.current_token
        if token.type in (My_PLUS, My_MINUS):
            self.advance()
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == My_INT:
            self.advance()
            return Num(token)
        elif token.type == My_LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type == My_RPAREN:
                self.advance()
                return node 
    
    
    RDA = {
        My_INT: factor,
        My_PLUS: factor,
        My_MINUS: factor,
        My_LPAREN: factor,
        My_ID: factor,
        My_EOF: None,
    }
## keywords  
KEYWORDS = [
    My_IF,
    My_ELSE,
    My_WHILE,
]

## Show wherer every rule set confomrs to LL Grammar

## LL Grammar
## expr : term ((PLUS | MINUS) term)*
## term : factor ((MUL | DIV) factor)*
## factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN

## Parser
## expr
##  term
##   factor
##    INTEGER
##    LPAREN expr RPAREN
##    (PLUS | MINUS) factor
##   (MUL | DIV) factor
##  ((PLUS | MINUS) term)*

## read in a file and run it



    
def run (text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(tokens)
    
    ast = parser.parse()
    return ast.tree, ast.error

## Create a LR Parser table for the grammar

## LR Grammar
# S -> E -> E + T -> E + T + F -> E + T + F + I
# S -> E -> E + T -> E + T + F -> E + T + F - I
## start with S
## Statement -> Expression -> Expression + Term -> Expression + Term + Factor -> Expression + Term + Factor + Integer
## expr : term ((PLUS | MINUS) term)*
## term : factor ((MUL | DIV) factor)*
## factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN


##with open('Regular_grammer.txt', 'r') as f:
  ##    text = f.read()
    ##  print(run(text))
##with open ('Testin2.py', 'r') as f:
  ##  text = f.read()
    ##print(run(text))
##with open ('Testin3.py', 'r') as f:
  ##  text = f.read()
    ##print(run(text))
##with open ('Testin4.py', 'r') as f:
  ##  text = f.read()
    ##print(run(text))
    
    
##def run(text):
  ##  lexer = Lexer(text)
    ##tokens,error = lexer.make_tokens()
    ##return tokens, error
