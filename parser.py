from fileinput import input

# Terminals
T = [';', 'id', ':=', 'if', 'then', 'endif', 'else', 'while', 'do',
    'end', 'c', '<', '=', '!=', '+', '-', '$']

# Parse table
table = {'P': {'id': ['L'], 'if': ['L'], 'while': ['L']},
    'L': {'id': ['I', 'L1'], 'if': ['I', 'L1'], 'while': ['I', 'L1']},
    'L1': {';': [';', 'L'], 'endif': [], 'else': [], 'end': [], '$': []},
    'I': {'id': ['A'], 'if': ['C'], 'while': ['W']},
    'A': {'id': ['id', ':=', 'E']},
    'C': {'if': ['if', 'E', 'then', 'L', 'O', 'endif']},
    'O': {'endif': [], 'else': ['else', 'L']},
    'W': {'while': ['while', 'E', 'do', 'L', 'end']},
    'E': {'id': ['E2', 'E1'], 'c': ['E2', 'E1']},
    'E1': {';': [], 'then': [], 'endif': [], 'else': [], 'do': [], 'end': [],
        '<': ['Op1', 'E2', 'E1'], '=': ['Op1', 'E2', 'E1'],
        '!=': ['Op1', 'E2', 'E1'], '$': []},
    'E2': {'id': ['T', 'E3'], 'c': ['T', 'E3']},
    'E3': {';': [], 'then': [], 'endif': [], 'else': [], 'do': [], 'end': [],
        '<': [], '=': [], '!=': [], '+': ['Op2', 'E2'], '-': ['Op2', 'E2'],
        '$': []},
    'T': {'id': ['id'], 'c': ['c']},
    'Op1': {'<': ['<'], '=': ['='], '!=': ['!=']},
    'Op2': {'+': ['+'], '-': ['-']}}

# Error recovery
error = False
panic = False
sync = [';', 'endif', 'end', '$']
first = {
    'P': ['id', 'if', 'while'],
    'L': ['id', 'if', 'while'],
    'L1': [';', ''],
    'I': ['id', 'if', 'while'],
    'A': ['id'],
    'C': ['if'],
    'O': ['else', 'endif'],
    'W': ['while'],
    'E': ['c', 'id'],
    'E1': ['<', '=', '!=', ''],
    'E2': ['c', 'id'],
    'E3': ['+', '-', ''],
    'T': ['c', 'id'],
    'Op1': ['<', '=', '!='],
    'Op2': ['+', '-'],
    '$': ['EOF']
    }

stack = ['$', 'P']

def lex(s):
    "Convert a string into a list of tokens."
    return s.replace(';', ' ; ').split()

def panicking(s, tok, toks):
    global panic, error
    error = True
    msg = ''
    exp = first[s]
    if '' in exp:
        for e in reversed(stack):
            if e in T:
                exp += [e] if e != '$' else ['EOF']
                break
            else:
                exp += first[e]
                if '' in first[e]:
                    continue
                else:
                    break
    exp = [e for e in exp if e != '']
    msg = "'" + "', '".join(exp[:-1]) + "' or '" + exp[-1] + "'"
    if not panic:
        tokmsg = tok if tok != '$' else 'EOF'
        print "warning: expected {0} instead of '{1}'".format(msg, tokmsg)
    panic = True
    while tok not in sync:
        tok = toks.pop(0)
    toks = [tok] + toks

def parse(toks):
    while len(stack) > 0:
        print ' '.join(reversed(stack))
        s = stack.pop()
        tok = toks[0]
        if s in T:
            if s == tok:
                toks.pop(0)
                if tok == '$' and not error:
                    print('accepted')
                elif tok == '$' and error:
                    print('rejected')
            else:
                tokmsg = tok if tok != '$' else 'EOF'
                print("error: expected '{0}' instead of '{1}'".format(s, tokmsg))
                print('rejected')
                break
        else:
            try:
                rule = table[s][tok]
            except KeyError:
                panicking(s, tok, toks)
                continue
            panic = False
            for r in reversed(rule):
                stack.append(r)
        panic = False

def main():
    toks = []
    for line in input():
        toks += lex(line)
    toks += ['$']
    parse(toks)

if __name__ == '__main__':
    main()
