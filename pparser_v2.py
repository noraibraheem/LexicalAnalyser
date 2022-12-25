"""
The lex.py module is used to break input text into
a collection of tokens specified by a collection of
regular expression rules. yacc.py is used to recognize
language syntax that has been specified in the form of
a context free grammar.  
    
"""
import ply.lex as lex
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME','INT_NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    'FLOAT_NUMBER','QOUTE','PRINT','IF','SYM_COLON',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    )

# Tokens

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'

# Comparisons
t_EQ         = r'=='        # Equal Equal 
t_NE         = r'!='        # Not equal
t_LT         = r'<'         # Less than
t_LE         = r'<='        # Less equal
t_GT         = r'>'         # Greater than
t_GE         = r'>='        # Greater equal
t_EQUALS     = r'='         # Equals

t_QOUTE      = r'"'  # Qoute
# t_LPP = r'(\{)'
# t_RPP = r'\}'
t_SYM_COLON  = r'\:'        # Syn_co,on
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_NAME       = r'[a-zA-Z_][a-zA-Z0-9_]*'


################################################### 
def t_IF(t):
    r'if\s.*?'
    t.value = str(t.value)
    return t

def t_PRINT(t):
    r'printf'
    # t.value = str(t.value)
    return t
def t_FLOAT_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
################################################### 


def t_INT_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer

lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'EQ', 'NE'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),   
    )

# dictionary of variables (for storing variables)
variables = { }

def p_statement_expr(p):
    'statement : expression'
    print(p[1])
    
def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    variables[p[1]] = p[3]

#########################################
def p_expression_m_if(p):
    '''expression : IF LPAREN NAME EQ expression RPAREN expression
                  | IF LPAREN NAME NE expression RPAREN expression
                  | IF LPAREN NAME LT expression RPAREN expression
                  | IF LPAREN NAME LE expression RPAREN expression
                  | IF LPAREN NAME GT expression RPAREN expression
                  | IF LPAREN NAME GE expression RPAREN expression'''

    if p[4] == '=='  :
        if variables.get(p[3]) == p[5]:
            p[0] = p[7]
        
    elif p[4] == '!=': 
        if variables.get(p[2]) != p[4]:
            p[0] = p[7]
    elif p[4] == '<':
        if variables.get(p[2]) <  p[4] :
          p[0] = p[7]        
    elif p[4] == '<=':
        if variables.get(p[2]) <=  p[4] :
          p[0] = p[7]        
    elif p[4] == '>':
        if variables.get(p[2]) >  p[4] :
          p[0] = p[7]        
    elif p[4] == '>=':
        if variables.get(p[2]) >=  p[4] :
          p[0] = p[7]        
    else:
        pass
#########################################

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
    
###################################################  
def p_expression_print(p):
    'expression : PRINT LPAREN QOUTE NAME QOUTE RPAREN'
    p[0] = p[4]
    
def p_expression_printsum(p):
    'expression : PRINT LPAREN expression RPAREN'
    p[0] = p[3]
     
def p_expression_float_number(p):
    'expression : FLOAT_NUMBER'
    p[0] = p[1]
###################################################

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : INT_NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()
# read from user
while True:
    try:
        s = input('input > ')   # use input() on Python 3
    except EOFError:
        break
    yacc.parse(s)    # Test it





# read a file
# if __name__ == '__main__':
#     f = open("demo.txt",'r')
#     content = f.readlines()
    
#     for line in content:
#         yacc.parse(line)
