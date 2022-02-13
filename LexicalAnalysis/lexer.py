from sly import Lexer


class Lexer(Lexer):
    tokens = {PLUS, MINUS, MULT, DIVIDE, MOD, ASSIGN, LPAREN, RPAREN, LSQB, RSQB, COMMA, INTVAL, FLOATVAL, CHARVAL, STRINGVAL, BOOLVAL,
              LBRACE, RBRACE, SEMICOL, VARNAME, IF, ELSE, WHILE, FOR, ELIF, RETURN, BREAK, FUNCNAME, DATATYPE, RELOP, LOGOP}

    ignore = ' \t'
    ignore_comment = r'``(.|\n)[^``]*``'
    ignore_newline = r'\n+'

    # Tokens
    MULT = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'{'
    RBRACE = r'}'
    LSQB = r'\['
    RSQB = r'\]'
    RELOP = r'<=|>=|<|>|==|!='
    ASSIGN = r'='
    LOGOP = r'&&|\|\|'
    COMMA = r','
    SEMICOL = r';'
    FLOATVAL = r'(\d+\.\d+)|(\d+\.)|(-|\+)(\d+\.\d+)|(-|\+)(\d+\.)'
    INTVAL = r'\d+|(-|\+)\d+'
    PLUS = r'\+'
    MINUS = r'-'
    CHARVAL = r'\'\w\''
    STRINGVAL = r'\"[^\"]*\"'
    VARNAME = r'[a-zA-Z][a-zA-Z0-9_]*'
    FUNCNAME = r'@[a-zA-Z][a-zA-Z0-9_]*'
    VARNAME['if'] = IF
    VARNAME['else'] = ELSE
    VARNAME['while'] = WHILE
    VARNAME['for'] = FOR
    VARNAME['elif'] = ELIF
    VARNAME['return'] = RETURN
    VARNAME['break'] = BREAK
    VARNAME['int'] = DATATYPE
    VARNAME['float'] = DATATYPE
    VARNAME['char'] = DATATYPE
    VARNAME['string'] = DATATYPE
    VARNAME['bool'] = DATATYPE
    VARNAME['void'] = DATATYPE
    VARNAME['true'] = BOOLVAL
    VARNAME['false'] = BOOLVAL

    def error(self, t):
        print("----Illegal character '%s'----" % t.value[0])
        self.index += 1


if __name__ == '__main__':
    test_case = open('../TestSuites/MatrixSum.sq', 'r')
    lexer = Lexer()
    for token in lexer.tokenize(test_case.read()):
        print('type=%r, value=%r' % (token.type, token.value))
    test_case.close()