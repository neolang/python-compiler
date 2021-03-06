#!/usr/bin/env python
import compiler.lexer as lexer
import ply.yacc as yacc
import anytree
# Get the token map
tokens = lexer.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
)


class Node(anytree.Node):
    def __init__(self, type, children=None):
        self.name = type
        tmp_children = []
        if children:
            for child in children:
                if isinstance(child, Node):
                    tmp_children.append(child)
                else:
                    tmp_children.append(Node(child))
        self.children = tmp_children

    def __str__(self):
        ret = ""
        for pre, _, node in anytree.RenderTree(self):
            ret += "%s%s" % (pre, node.name) + "\n"
        return ret


start = 'compilation_unit'


def p_compilation_unit_1(p):
    '''compilation_unit : external_declaration'''
    p[0] = Node("compilation_unit", p[1:])


def p_compilation_unit_2(p):
    '''compilation_unit : compilation_unit external_declaration'''
    p[0] = Node("compilation_unit", p[1:])


def p_external_declaration_1(p):
    '''external_declaration : function_definition
                            | declaration'''
    p[0] = Node("external_declaration", p[1:])


def p_primary_expresssion_1(p):
    '''primary_expression : NUMBER
                          | ID'''
    p[0] = Node("primary_expression", p[1:])


def p_postfix_expression_1(p):
    '''postfix_expression : primary_expression'''
    p[0] = Node("postfix_expression", p[1:])


def p_postfix_expression_2(p):
    '''postfix_expression : postfix_expression LPAREN RPAREN'''
    p[0] = Node("postfix_expression", p[1:])


def p_postfix_expression_3(p):
    '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
    p[0] = Node("postfix_expression", p[1:])


def p_argument_expression_list_1(p):
    '''argument_expression_list : postfix_expression'''
    p[0] = Node("argument_expression_list", p[1:])


def p_argument_expression_list_2(p):
    '''argument_expression_list : argument_expression_list COMMA postfix_expression'''
    p[0] = Node("argument_expression_list", p[1:])


def p_math_expression_1(p):
    '''math_expression : postfix_expression'''
    p[0] = Node("math_expression", p[1:])


def p_math_expression_2(p):
    ''' math_expression : math_expression PLUS math_expression
                        | math_expression MINUS math_expression
                        | math_expression MULT math_expression
                        | math_expression DIVIDE math_expression
                        | math_expression MOD math_expression'''
    p[0] = Node("math_expression", p[1:])


def p_math_expression_3(p):
    '''math_expression : LPAREN math_expression RPAREN'''
    p[0] = Node("math_expression", p[1:])


def p_assignment_expression_1(p):
    '''assignment_expression : math_expression'''
    p[0] = Node("assignment_expression", p[1:])


def p_assignment_expression_2(p):
    '''assignment_expression : postfix_expression ASSIGN assignment_expression'''
    p[0] = Node("assignment_expression", p[1:])


def p_type(p):
    '''type : BYTE
            | INT
            | VOID'''
    p[0] = Node("type", p[1:])


def p_declaration_1(p):
    '''declaration : declaration_specifier SEMICOLON'''
    p[0] = Node("declaration", p[1:])


def p_declaration_2(p):
    '''declaration : declaration_specifier init_declarator_list SEMICOLON'''
    p[0] = Node("declaration", p[1:])


def p_declaration_specifier_1(p):
    '''declaration_specifier : type'''
    p[0] = Node("declaration_specifier", p[1:])


def p_declaration_specifier_2(p):
    '''declaration_specifier : type declaration'''
    p[0] = Node("declaration_specifier", p[1:])


def p_init_declarator_list_1(p):
    '''init_declarator_list : init_declarator'''
    p[0] = Node("init_declarator_list", p[1:])


def p_init_declarator_list_2(p):
    '''init_declarator_list : init_declarator_list COMMA init_declarator'''
    p[0] = Node("init_declarator_list", p[1:])


def p_init_declarator_1(p):
    '''init_declarator : declarator'''
    p[0] = Node("init_declarator", p[1:])


def p_init_declarator_2(p):
    '''init_declarator : declarator ASSIGN assignment_expression'''
    p[0] = Node("init_declarator", p[1:])


def p_declarator_1(p):
    '''declarator : ID'''
    p[0] = Node("declarator", p[1:])


def p_declarator_2(p):
    '''declarator : LPAREN declarator RPAREN'''
    p[0] = Node("declarator", p[1:])


def p_declarator_3(p):
    '''declarator : declarator LPAREN RPAREN'''
    p[0] = Node("declarator", p[1:])


def p_declarator_4(p):
    '''declarator : declarator LPAREN parameter_list RPAREN'''
    p[0] = Node("declarator", p[1:])


def p_declarator_5(p):
    '''declarator : declarator LPAREN identifier_list RPAREN'''
    p[0] = Node("declarator", p[1:])


def p_function_definition_1(p):
    '''function_definition : FUNC ID LPAREN RPAREN type compound_statement'''
    p[0] = Node("function_definition", p[1:])


def p_function_definition_2(p):
    '''function_definition : FUNC ID LPAREN parameter_list RPAREN type compound_statement'''
    p[0] = Node("function_definition", p[1:])


def p_identifier_list_1(p):
    '''identifier_list : ID'''
    p[0] = Node("identifier_list", p[1:])


def p_identifier_list_2(p):
    '''identifier_list : identifier_list COMMA ID'''
    p[0] = Node("identifier_list", p[1:])


def p_parameter_declaration_1(p):
    '''parameter_declaration : declaration_specifier'''
    p[0] = Node("parameter_declaration", p[1:])


def p_parameter_declaration_2(p):
    '''parameter_declaration : declaration_specifier declarator'''
    p[0] = Node("parameter_declaration", p[1:])


def p_parameter_list_1(p):
    '''parameter_list : parameter_declaration'''
    p[0] = Node("parameter_list", p[1:])


def p_parameter_list_2(p):
    '''parameter_list : parameter_list COMMA parameter_declaration'''
    p[0] = Node("parameter_list", p[1:])


def p_compound_statement_1(p):
    '''compound_statement : LBRACE RBRACE'''
    p[0] = Node("compound_statement", p[1:])


def p_compound_statement_2(p):
    '''compound_statement : LBRACE compound_list RBRACE'''
    p[0] = Node("compound_statement", p[1:])


def p_compound_statement_inner_1(p):
    '''compound_statement_inner : statement_list
                                | declaration_list'''
    p[0] = Node("compound_list", p[1:])


def p_compound_list_1(p):
    '''compound_list : compound_statement_inner'''
    p[0] = Node("compound_list", p[1:])


def p_compound_list_2(p):
    '''compound_list : compound_list compound_statement_inner'''
    p[0] = Node("compound_list", p[1:])


def p_statement_list_1(p):
    '''statement_list : statement'''
    p[0] = Node("statement_list", p[1:])


def p_statement_list_2(p):
    '''statement_list : statement_list statement'''
    p[0] = Node("statement_list", p[1:])


def p_statement_1(p):
    '''statement : expression_statement
                 | jump_statement'''
    p[0] = Node("statement", p[1:])


def p_expression_statement_1(p):
    '''expression_statement : SEMICOLON'''
    p[0] = Node("expression_statement", p[1:])


def p_expression_statement_2(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = Node("expression_statement", p[1:])


def p_jump_statement_1(p):
    '''jump_statement : RETURN SEMICOLON'''
    p[0] = Node("jump_statement", p[1:])


def p_jump_statement_2(p):
    '''jump_statement : RETURN expression SEMICOLON'''
    p[0] = Node("jump_statement", p[1:])


def p_expression_1(p):
    '''expression : assignment_expression'''
    p[0] = Node("expression", p[1:])


def p_expression_2(p):
    '''expression : expression COMMA assignment_expression'''
    p[0] = Node("expression", p[1:])


def p_declaration_list_1(p):
    '''declaration_list : declaration'''
    p[0] = Node("declaration_list", p[1:])


def p_declaration_list_2(p):
    '''declaration_list : declaration_list declaration'''

    p[0] = Node("declaration_list", p[1:])


def p_empty(p):
    'empty : '
    p[0] = Node("empty")


def p_error(p):
    print("Whoa. We're hosed")
    if not p:
        print("End of File!")
        return


plyparser = yacc.yacc()


class Parser:
    def __init__(self, inFile=None, inString=None, debug=0):
        plyparser.error = 0
        self.nodes = []

        if inFile == None and inString != None:
            self.nodes = plyparser.parse(inString, debug=debug)

        elif inString == None and inFile != None:
            self.nodes = plyparser.parse(inFile.read(), debug=debug)
        else:
            raise ValueError("Requires either a file or string")

    def getNodes(self):
        if plyparser.error:
            return None
        return self.nodes
