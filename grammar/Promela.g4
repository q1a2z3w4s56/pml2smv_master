grammar Promela;

// Parser Rules

spec: unit* EOF;

unit
    : mtypeDecl
    | varDecl
    | proctype
    | init
    | inlineDecl
    | typedefDecl
    ;

mtypeDecl: 'mtype' '=' '{' ID (',' ID)* '}' ';'? ;

typedefDecl: 'typedef' ID '{' varDecl+ '}' ';'? ;

varDecl: typename ID ('[' expr ']')? ('=' expr)? (',' ID ('[' expr ']')? ('=' expr)?)* ';'? ;

typename
    : 'bit'
    | 'bool'
    | 'byte'
    | 'short'
    | 'int'
    | 'mtype'
    | 'chan'
    | 'pid'
    | ID  // for typedef types
    ;

proctype
    : 'active' ('[' expr ']')? 'proctype' ID '(' (varDecl (',' varDecl)*)? ')' '{' sequence '}'
    | 'proctype' ID '(' (varDecl (',' varDecl)*)? ')' '{' sequence '}'
    ;

init: 'init' '{' sequence '}' ;

inlineDecl: 'inline' ID '(' (ID (',' ID)*)? ')' '{' sequence '}' ;

sequence: step (';'? step)* ';'? ;

step
    : stmt
    | stmt 'unless' stmt
    ;

stmt
    : 'skip'                                          # SkipStmt
    | 'break'                                         # BreakStmt
    | ID ':' stmt                                     # LabeledStmt
    | 'goto' ID                                       # GotoStmt
    | expr                                            # ExprStmt
    | ID '=' expr                                     # AssignStmt
    | ID '[' expr ']' '=' expr                        # ArrayAssignStmt
    | ID '.' ID '=' expr                              # FieldAssignStmt
    | 'if' options 'fi'                               # IfStmt
    | 'do' options 'od'                               # DoStmt
    | 'atomic' '{' sequence '}'                       # AtomicStmt
    | 'd_step' '{' sequence '}'                       # DstepStmt
    | '{' sequence '}'                                # BlockStmt
    | 'printf' '(' STRING (',' expr)* ')'             # PrintfStmt
    | 'printm' '(' expr ')'                           # PrintmStmt
    | 'assert' '(' expr ')'                           # AssertStmt
    | ID '!' expr (',' expr)*                         # SendStmt
    | ID '?' ID (',' ID)*                             # ReceiveStmt
    | ID '?' '<' ID (',' ID)* '>'                     # ReceivePollStmt
    | 'run' ID '(' (expr (',' expr)*)? ')'           # RunStmt
    | ID '(' (expr (',' expr)*)? ')'                 # InlineCallStmt
    ;

options: '::' sequence ('::' sequence)* ;

expr
    : '(' expr ')'                                    # ParenExpr
    | expr ('*' | '/' | '%') expr                     # MulDivModExpr
    | expr ('+' | '-') expr                           # AddSubExpr
    | expr ('<<' | '>>') expr                         # ShiftExpr
    | expr ('<' | '<=' | '>' | '>=') expr            # RelationalExpr
    | expr ('==' | '!=') expr                        # EqualityExpr
    | expr '&' expr                                   # BitwiseAndExpr
    | expr '^' expr                                   # BitwiseXorExpr
    | expr '|' expr                                   # BitwiseOrExpr
    | expr '&&' expr                                  # LogicalAndExpr
    | expr '||' expr                                  # LogicalOrExpr
    | '!' expr                                        # LogicalNotExpr
    | '~' expr                                        # BitwiseNotExpr
    | '-' expr                                        # UnaryMinusExpr
    | '+' expr                                        # UnaryPlusExpr
    | expr '++' | '++' expr                           # IncrementExpr
    | expr '--' | '--' expr                           # DecrementExpr
    | ID '[' expr ']'                                 # ArrayAccessExpr
    | ID '.' ID                                       # FieldAccessExpr
    | 'len' '(' ID ')'                                # LenExpr
    | 'empty' '(' ID ')'                              # EmptyExpr
    | 'full' '(' ID ')'                               # FullExpr
    | 'enabled' '(' expr ')'                          # EnabledExpr
    | 'nempty' '(' ID ')'                             # NemptyExpr
    | 'nfull' '(' ID ')'                              # NfullExpr
    | 'timeout'                                       # TimeoutExpr
    | 'np_'                                           # NonProgressExpr
    | ID                                              # IdExpr
    | NUMBER                                          # NumberExpr
    | STRING                                          # StringExpr
    | 'true'                                          # TrueExpr
    | 'false'                                         # FalseExpr
    ;

// Lexer Rules

NUMBER: [0-9]+ ;
ID: [a-zA-Z_][a-zA-Z0-9_]* ;
STRING: '"' (~["\r\n] | '\\' .)* '"' ;

COMMENT: '/*' .*? '*/' -> skip ;
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
WS: [ \t\r\n]+ -> skip ;
