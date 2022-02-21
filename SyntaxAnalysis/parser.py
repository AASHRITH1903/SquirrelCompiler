from sly import Parser as SlyParser
import sys
import os
sys.path.append(os.path.abspath('../LexicalAnalysis'))
import lexer
from AstNode import Operator, AstNode

'''
symbol_table : {
    'identifier_name' : {
        'type' : 'int',
        'size' : 4,
        'line_no' : 1,
        'scope' : 'global',

}

{ id -> 1
    
    int age = 0;

    { id -> 2

        int age = 1;

        { id -> 3

        }

        { id -> 4

        int a;

        }
      
    }
}

symbol_table : [
    {
        identifier_name : 'age',
        ....details,
        scope: 1
        parent_scope: 0
    },
    {
        identifier_name : 'age',
        ....details,
        scope: 2
        parent_scope: 1
    }
]


global = {

    variable : {
        "age" :{ info about age}
        "name" : { info about name}
    }

    sub_scopes : {
        "sub_scope_1" : {
            parent_scope : global
            variable : {
                "age" :{ info about age}
                "name" : { info about name}
            }
            sub_scopes : {
            
            }
        }

        "sub_scope_2" : {
            parent_scope : global
            variable : {
                "age" :{ info about age}
                "name" : { info about name}
            }
            sub_scopes : {
            
            }
        }
    }
}

'''


class Parser(SlyParser):

    def __init__(self):
        self.symbol_table = []
        self.id = 2
        self.scope_id_stack = [0, 1]

        self.num_labels = 0

    def get_new_label(self):
        self.num_labels += 1
        return "L" + str(self.num_labels - 1)
    
    start = "program"
    tokens = lexer.Lexer.tokens

    debugfile = 'parser.out'

    precedence = (
        ('left', 'COMMA'),
        ('right', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'RELOP2'),
        ('left', 'RELOP1'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE', 'MOD'),
        ('right', 'TYPECASTING'),         # fictitious token
        ('right', 'UMINUS', 'NOT'),       # fictitious token
        ('right', 'PAREN')                # fictitious token
    )

    # program -> methods
    @_('methods')
    def program(self, p):
        val = AstNode(Operator.A_ROOT,left=p.methods)
        val.left = p.methods
        AstNode.generateCode(val, self.get_new_label)

    # methods -> methods method
    @_('methods method')
    def methods(self, p):
        return AstNode(Operator.A_NODE,left=p.methods, right=p.method)

    @_('method')
    def methods(self, p):
        return AstNode(Operator.A_NODE,left=p.method)

    # method -> DATATYPE FUNCNAME ( params ) { statements }
    @_('DATATYPE FUNCNAME LPAREN params RPAREN LBRACE statements RBRACE')
    def method(self,p):
        # return AstNode(Operator.A_FUNC,left=p.params,right=p.statements)
        return AstNode(Operator.A_FUNC,left=p.params,right=p.statements, next_label=self.get_new_label())

    # params -> DATATYPE VARNAME, params | e
    @_('DATATYPE VARNAME COMMA params')
    def params(self,p):
        return None

    @_('empty')
    def params(self,p):
        return None

    # statements -> statements statement 
    @_("statements statement")
    def statements(self, p):
        return AstNode(Operator.A_NODE, left=p.statements, right=p.statement)

    @_('empty')
    def statements(self, p):
        val = AstNode()
        val.code = ""
        return val

    # statement -> declaration_statement | assignment_statement | io_statement | selection_statement | iteration_statement | jump_statement
    @_('declaration_statement SEMICOL')
    def statement(self, p):
        return p.declaration_statement

    @_('assignment_statement SEMICOL')
    def statement(self, p):
        pass

    @_('io_statement SEMICOL')
    def statement(self, p):
        return p[0]

    @_('selection_statement')
    def statement(self, p):
        return p.selection_statement
    
    @_("if_statement")
    def selection_statement(self, p):
        return p.if_statement
    
    # declaration_statement -> simple_init | array_init
    @_("simple_init")
    def declaration_statement(self, p):
        return p.simple_init

    # simple_init -> DATATYPE VARNAME | DATATYPE VARNAME = expr
    @_("DATATYPE VARNAME")
    def simple_init(self, p):
        val = AstNode(Operator.A_DECL, left=p.VARNAME)
        val.code = p.DATATYPE + " " + p.VARNAME
        return val

    # if_statement -> IF ( expr ) { statements }
    @_("IF LPAREN expr RPAREN LBRACE statements RBRACE")
    def if_statement(self, p):
        return AstNode(Operator.A_IF, left=p.expr, right=p.statements)

    # io_statement -> input_statement | output_statement
    @_('input_statement')
    def io_statement(self, p):
        return p[0]

    @_('output_statement')
    def io_statement(self, p):
        return p[0]

    # input_statement -> INPUT ( left_value )
    @_('INPUT LPAREN left_value RPAREN')
    def input_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # output_statement -> OUTPUT ( left_value )  | OUTPUT ( constant )
    @_('OUTPUT LPAREN left_value RPAREN')
    def output_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    @_('OUTPUT LPAREN constant RPAREN')
    def output_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # jump_statement -> BREAK | return_statement
    @_('BREAK')
    def jump_statement(self, p):
        return p.BREAK

    @_('return_statement')
    def jump_statement(self, p):
        return p.return_statement

    # return_statement -> RETURN expr | RETURN
    @_('RETURN expr')
    def return_statement(self, p):
        return str('return ' + p.expr)

    @_('RETURN')
    def return_statement(self, p):
        return str('return')

    @_('expr PLUS expr')
    def expr(self, p):
        '''
            expr0.code
            expr1.code
            t = expr0.addr + expr1.addr
        '''
        pass

    @_('expr MINUS expr')
    def expr(self, p):
        pass

    @_('expr MULT expr')
    def expr(self, p):
        pass

    @_('expr DIVIDE expr')
    def expr(self, p):
        pass

    @_('expr MOD expr')
    def expr(self, p):
        pass

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('LPAREN expr RPAREN %prec PAREN')
    def expr(self, p):
        return p.expr
    
    @_('expr RELOP1 expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')

    @_('expr RELOP2 expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')
    
    @_("COMMA")
    def b1_open(self, p):
        pass

    @_('')
    def b2_open(self, p):
        print("b2_open")
        
    @_('expr AND expr')
    def expr(self, p):
        return AstNode(Operator.A_AND, left=p.expr0, right=p.expr1)        

    @_('expr OR expr')
    def expr(self, p):
        return AstNode(Operator.A_OR, left=p.expr0, right=p.expr1)

    @_('NOT expr %prec NOT')
    def expr(self, p):
        print('NOT expr %prec NOT')
        return str('(!'+p.expr+')')

    @_('VARNAME')
    def expr(self, p):
        print("varname : " + p.VARNAME)
        return {
            "addr" : p.VARNAME,
            "code" : ""
        }

    # expr -> constant
    @_('constant')
    def expr(self, p):
        return AstNode(Operator.A_CONST,value=p.constant)

    # expr -> (DATATYPE) expr
    @_('LPAREN DATATYPE RPAREN expr %prec TYPECASTING')
    def expr(self, p):
        return str('('+p[0]+p[1]+p[2]+p[3]+')')

# -----------------------------------------------------------------------------------------

    # arr_variable -> VARNAME [INTVAL] | VARNAME [INTVAL][INTVAL] | VARNAME [VARNAME] | VARNAME [VARNAME][VARNAME] | VARNAME [INTVAL][VARNAME] | VARNAME [VARNAME][INTVAL]
    @_('VARNAME LSQB INTVAL RSQB')
    def array_variable(self, p):

        '''return {
            "code"
            "addr"
            "rows"
            "columns"
        }'''
        return str('('+p[0]+'['+p[2]+']'+')')

    @_('VARNAME LSQB INTVAL RSQB LSQB INTVAL RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB LSQB INTVAL RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB INTVAL RSQB LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    # assignment_statement -> left_value = expr
    @_('left_value ASSIGN expr')
    def assignment_statement(self, p):
        return {
            "code" : p.expr["code"] + str(p.left_value + '=' + p.expr["addr"]) + "\n"
        }
        

    # left_value -> VARNAME | array_variable
    @_('VARNAME')
    def left_value(self, p):
        return str(p[0])

    @_('array_variable')
    def left_value(self, p):
        return str(p[0])


    # constant -> INTVAL | FLOATVAL | CHARVAL | STRINGVAL | BOOLVAL
    @_('INTVAL')
    def constant(self, p):
        return str(p[0])

    @_('FLOATVAL')
    def constant(self, p):
        return str(p[0])

    @_('CHARVAL')
    def constant(self, p):
        return str(p[0])

    @_('STRINGVAL')
    def constant(self, p):
        return str(p[0])

    @_('BOOLVAL')
    def constant(self, p):
        return p.BOOLVAL

    # expr -> function_call
    @_('function_call')
    def expr(self, p):
        return str(p.function_call)

    # function_call -> VARNAME ( argument_list )
    @_('VARNAME LPAREN argument_list RPAREN')
    def function_call(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # argument_list -> argument, argument_list
    @_('argument COMMA argument_list')
    def argument_list(self, p):
        return str(p[0]+p[1]+p[2])

    # argument_list -> argument
    @_('argument')
    def argument_list(self, p):
        return str(p.argument)

    # argument -> VARNAME | constant | array_variable
    @_('VARNAME',
        'constant',
        'array_variable')
    def argument(self, p):
        return str(p[0])

    @_('')
    def empty(self, p):
        pass

    #def error(self, p):
        #if p:
            #print("Syntax error at line", p.lineno, "| TOKEN:", p.value)
            #
        #else:
            #print("Syntax error at EOF")
        #raise Exception('Syntax error')


if __name__ == '__main__':


    lex = lexer.Lexer()
    parser = Parser()

    with open("../TestSuites/TACtest.sq", 'r') as f:
        text = f.read()

    parser.parse(lex.tokenize(text))