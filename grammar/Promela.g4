grammar Promela;

// Top-level specification
spec: unit* EOF;

// Top-level units
unit: chanDecl
    | mtypeDecl
    | typedefDecl
    | varDecl
    | proctype
    | init
    | inlineDecl
    ;

// Channel declaration
chanDecl: 'chan' ID '=' '[' expr ']' 'of' '{' typename (',' typename)* '}' ';'?;

// Mtype declaration
mtypeDecl: 'mtype' '=' '{' ID (',' ID)* '}' ';'?;

// Typedef declaration
typedefDecl: 'typedef' ID '{' varDecl+ '}' ';'?;

// Variable declaration
varDecl: typename ID ('[' expr ']')? ('=' expr)? (',' ID ('[' expr ']')? ('=' expr)?)* ';'?;

// Type names
typename: 'bit' | 'bool' | 'byte' | 'short' | 'int' | 'mtype' | 'chan' | 'pid' | ID;


proctype:  ('active' ('[' expr ']')?)? 'proctype' ID '(' (paramGroup (';' paramGroup)*)? ')' '{' sequence '}';


// 参数组：同一类型的多个参数
paramGroup: typename ID (',' ID)*;

// Init process
init: 'init' '{' sequence '}' ;

// Inline declaration
inlineDecl: 'inline' ID '(' (ID (',' ID)*)? ')' '{' sequence '}' ;

// Sequence of steps
sequence: (varDecl | step)* ;

// Step (statement or unless)
step: stmt ('unless' stmt)? ;

// 语句
stmt
    : 'skip' ';'?                                                          # skipStmt
    | 'break' ';'?                                                         # breakStmt
    | ID ':' stmt?                                                         # labeledStmt
    | 'goto' ID ';'?                                                       # gotoStmt
    // 注意：这里的 exprStmt 很宽，会吃掉很多东西，顺序要放在赋值/调用之后会更安全
    | ID '=' expr ';'?                                                     # assignStmt
    | ID '[' expr ']' '=' expr ';'?                                        # arrayAssignStmt
    | ID '.' ID '=' expr ';'?                                              # fieldAssignStmt
    | 'if' optionLists 'fi' ('unless' expr)? ';'?                          # ifStmt
    | 'do' optionLists 'od' ('unless' expr)? ';'?                          # doStmt
    | 'atomic' '{' sequence '}' ';'?                                       # atomicStmt
    | 'd_step' '{' sequence '}' ';'?                                       # dstepStmt
    | '{' sequence '}' ';'?                                                # blockStmt
    | 'assert' '(' expr ')' ';'?                                           # assertStmt
    | 'printf' '(' STRING (',' expr)* ')' ';'?                             # printfStmt
    | 'printm' '(' expr ')' ';'?                                           # printmStmt
    | ID '!' expr (',' expr)* ';'?                                         # sendStmt
    | ID '?' ID (',' ID)* ';'?                                             # receiveStmt
    | ID '?' '<' ID (',' ID)* '>' ';'?                                     # receivePollStmt
    | ID '?' ID (',' ID)* '->' stmt                                        # receiveArrowStmt
    | 'run' ID '(' (expr (',' expr)*)? ')' ';'?                            # runStmt
    | ID '(' (expr (',' expr)*)? ')' ';'?                                  # inlineCallStmt
    | expr ';'?                                                            # exprStmt
    ;

// Option lists for if/do
optionLists: option+ ;

// Single option
option: '::' (expr '->')? sequence ;

// Expressions (with precedence)
expr
    : NUMBER                                                               # numberExpr
    | 'true'                                                               # trueExpr
    | 'false'                                                              # falseExpr
    | STRING                                                               # stringExpr
    | ID                                                                   # idExpr
    | '_pid'                                                               # pidExpr
    | '_nr_pr'                                                             # nrPrExpr
    | 'timeout'                                                            # timeoutExpr
    | 'np_'                                                                # nonProgressExpr
    | '(' expr ')'                                                         # parenExpr
    | expr ('*'|'/'|'%') expr                                              # mulDivModExpr
    | expr ('+'|'-') expr                                                  # addSubExpr
    | expr ('<<'|'>>') expr                                                # shiftExpr
    | expr ('<'|'>'|'<='|'>=') expr                                        # relationalExpr
    | expr ('=='|'!=') expr                                                # equalityExpr
    | expr '&' expr                                                        # bitwiseAndExpr
    | expr '^' expr                                                        # bitwiseXorExpr
    | expr '|' expr                                                        # bitwiseOrExpr
    | expr '&&' expr                                                       # logicalAndExpr
    | expr '||' expr                                                       # logicalOrExpr
    | '!' expr                                                             # logicalNotExpr
    | '~' expr                                                             # bitwiseNotExpr
    | '-' expr                                                             # unaryMinusExpr
    | '+' expr                                                             # unaryPlusExpr
    | expr '++'                                                            # postIncrExpr
    | expr '--'                                                            # postDecrExpr
    | ID '[' expr ']'                                                      # arrayAccessExpr
    | ID '.' ID                                                            # fieldAccessExpr
    | 'len' '(' ID ')'                                                     # lenExpr
    | 'empty' '(' ID ')'                                                   # emptyExpr
    | 'full' '(' ID ')'                                                    # fullExpr
    | 'nempty' '(' ID ')'                                                  # nemptyExpr
    | 'nfull' '(' ID ')'                                                   # nfullExpr
    | 'enabled' '(' expr ')'                                               # enabledExpr
    ;

// Lexer rules
NUMBER      : [0-9]+ ;
ID          : [a-zA-Z_][a-zA-Z0-9_]* ;
STRING      : '"' (~["\\\r\n] | '\\' .)* '"' ;

COMMENT     : '/*' .*? '*/' -> skip ;
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
WS          : [ \t\r\n]+ -> skip ;
