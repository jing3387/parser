# LL(1) parser

## Grammar
```
P   → L
L   → I L1
L1  → ; L | ε
I   → A | C | W
A   → id := E
C   → if E then L O endif
O   → else L | ε
W   → while E do L end
E   → E2 E1
E1  → Op1 E2 E1 | ε
E2  → T E3
E3  → Op2 E2 | ε
T   → c | id
Op1 → < | = | !=
Op2 → + | -
```

## Usage
To use the parser:
    ./parser file

To test the parser with the tests in t/:
    ./test
