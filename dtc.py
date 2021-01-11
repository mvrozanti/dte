#!/usr/bin/env python
DEBUG = 1
import re
import code
from datetime import datetime, date, timedelta
import time
from ply.lex import TOKEN

replace = lambda replacee,replacer,string: re.sub(replacee, replacer, string)

tokens = (
    'PLUS','MINUS','EQUALS',
    'LPAREN','RPAREN',
    'TIME_INVALID',
    'TIME_MS',
    'TIME_HM',
    'TIME_HMS',
    'N', # now
    'T', # today
    'YD', # yesterday
    'DELTA', 
    'DATE', 
    'PERIOD', 
    # 'DATETIME', 
    'NAME',
    )

# Tokens

t_PERIOD    = r'\.'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_EQUALS    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

t_NAME      = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_YD(t):
    r'[yY][dD]'
    t.value = datetime.today() - timedelta(days=1)
    return t

def t_T(t):
    r'[tT]'
    t.value = datetime.today()
    return t

def t_N(t):
    r'[nN]'
    t.value = datetime.now()
    return t

def t_TIME_HMS(t):
    r'(2[0-4]|[01][0-9]):(60|[0-5][0-9]):(60|[0-5][0-9])'
    t.value = datetime.strptime(t.value, '%H:%M:%S')
    return t

def t_TIME_INVALID(t):
    r'\d+:\d+'
    raise SyntaxError("Ambiguous time definition")
    return t

def t_TIME_MS(t):
    r'(2[0-4]|[01][0-9])[mM]:(60|[0-5][0-9])[sS]'
    t.value = datetime.strptime(replace('m|s', '', t.value), '%M:%S')
    return t

def t_TIME_HM(t):
    r'(2[0-3]|[01][0-9])[hH]:([0-5][0-9])[mM]'
    t.value = datetime.strptime(replace('h|m', '', t.value), '%H:%M')
    return t

def t_DATE(t):
    r'\d+(\D)(1[0-2]|0[1-9])\2(3[01]|[12][0-9]|[1-9]) '
    t.value = datetime.strptime(replace(r'\D', '-', t), '%Y-%M-%D')
    return t

DELTA_TOKEN = r'((\d+(?:\.\d+)?)([smhdSMHD]))+'
@TOKEN(DELTA_TOKEN)
def t_DELTA(t):
    units_vals = { 
            u.lower():float(v) if v else 1 \
                    for v,u in re.findall(DELTA_TOKEN[1:-2], t.value)
            }
    t.value = timedelta()
    if 's' in units_vals:
        t.value += timedelta(seconds=units_vals['s'])
    if 'm' in units_vals:
        t.value += timedelta(minutes=units_vals['m'])
    if 'h' in units_vals:
        t.value += timedelta(hours=units_vals['h'])
    if 'd' in units_vals:
        t.value += timedelta(days=units_vals['d'])
    return t

def t_DATETIME(t):
    r'\d+(\D)(1[0-2]|0[1-9])\2(3[01]|[12][0-9]|[1-9]) ' 
    t.value = datetime.strptime(replace(r'\D', '-', t), '%Y-%M-%D')
    return t

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

import ply.lex as lex
lex.lex(debug=0)

precedence = (
    ('left',
        'PLUS',
        'MINUS', 

        ),
    ('right',
        'UMINUS',

        ),
    )


days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_abbrev = [d[:3] for d in days]

def wait(t):
    if isinstance(t, datetime):
        now = datetime.now()
        delta = t - now
    elif isinstance(t, timedelta):
        delta = t
    else:
        raise SyntaxError("wait accepts datetime or timedelta only")
    if delta > timedelta(0):
        time.sleep(delta.total_seconds())

names = {
            'dow'    : lambda t: days[t.weekday()],
            'day'    : lambda t: t.day,
            'month'  : lambda t: t.month,
            'year'   : lambda t: t.year,
            'hour'   : lambda t: t.hour,
            'minute' : lambda t: t.minute,
            'second' : lambda t: t.second,
            'wait'   : lambda t: wait(t),
        }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    if p[1]:
        if isinstance(p[1], datetime) and \
                p[1].year == 1900:
                    print(datetime.strftime(p[1], '%H:%M:%S'))
        else:
            print(p[1])
        names['_'] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression'''
    if isinstance(p[1], datetime) and \
            isinstance(p[3], int):
        raise SyntaxError('can\'t subtract number from datetime')
    if p[1] is None or p[3] is None:
        raise SyntaxError(f'in {p[2]} expr, p[1]={p[1]} and p[3]={p[3]}')
    if   p[2] == '+': 
        if isinstance(p[1], datetime) and \
                isinstance(p[3], datetime):
            raise SyntaxError('kek')
        p[0] = p[1] + p[3]
    elif p[2] == '-': 
        p[0] = p[1] - p[3]

def p_expression_datetime(p):
    '''expression : TIME_MS 
                  | TIME_HM
                  | TIME_HMS
                  | DATE
                  | YD
                  | N
                  | DELTA
                  | T
                  '''
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    # print('expression_name')
    # code.interact(banner='', local=globals().update(locals()) or globals(), exitmsg='')
    try:
        p[0] = names[p[1]]
    except LookupError:
        try:
            p[0] = names[p[3]](p[1])
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_get_attribute(p):
    'expression : expression PERIOD NAME'
    if p[3] is None:
        raise SyntaxError
    p[0] = names[p[3]](p[1])

def p_expression_funcall(p):
    'expression : NAME LPAREN expression RPAREN'
    p[0] = names[p[1].lower()](p[3])

def p_expression_invalid_time(p):
    'expression : TIME_INVALID'

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    import cmd
    class CmdParse(cmd.Cmd):
        prompt = ''
        commands = []
        def default(self, line):
            if line == 'EOF':
                exit(0)
            yacc.parse(line)
            self.commands.append(line)
        def do_exit(self, line):
            return True
    CmdParse().cmdloop()
