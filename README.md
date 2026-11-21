# micro
A small, dynamically-typed scripting language with Ruby-like syntax, first-class functions, and arrays.

```
func fact(n)
    if n <= 1
        return 1
    end
    return n * fact(n - 1)
end

n = conv(input("Enter n for n!: "), "int")
print(fact(n))
```

### Editor Support
- [VSCode](https://github.com/las-r/micro-vscode)

### Forks
Subsets of micro, lacking features present in the standard implementation:
- [microbe](https://github.com/las-r/microbe): bytecode-esque fork written in Python
- [micro-jl](https://github.com/las-r/micro-jl): tree-walker fork written in Julia

Supersets of micro, adding features not present in the standard implementation:
- [macro](https://github.com/las-r/macro): extension adding for loops, maps, and closures, written in Python

## Getting Started
```sh
pip install git+https://github.com/las-r/micro
micro yourfile.mic
```

## Syntax & Basics
### Data Types & Variables
| Type | Description |
|---|---|
| `int` | Whole numbers |
| `float` | Decimal numbers |
| `str` | Strings, written `"like this"` |
| `arr` | Arrays, written `[1, 2, 3]` |
| `func` | Functions (first-class) |

There is no boolean type. Comparisons and logic operators produce `int`s (`0` for false, nonzero for true), and `if`/`while` treat any nonzero value as true.

Assigning to a name creates the variable, and comments start with `//`:
```
x = 10
name = "micro"
nums = [1, 2, 3]
// This is a comment!
```

### Operators
* **Arithmetic:** `+`, `-`, `*`, `/`, `%`
* **Bitwise:** `~` (not), `&`, `|`, `^`
* **Comparison:** `==`, `!=`, `<`, `<=`, `>`, `>=`
* **Logic:** `!`, `&&`, `||`

There is no operator precedence besides parentheses. Expressions evaluate strictly left to right, so `2 + 3 * 4` is `20`, but `2 + (3 * 4)` is `14`.

## Control Flow
### Conditionals
```
if x > 0
    print("positive")
else if x < 0
    print("negative")
else
    print("zero")
end
```
The `else if` chain and final `else` are optional and share a single `end`. `else if` must be written on one line. If `if` starts on the next line, it's a separate nested `if` that needs its own `end`:
```
if x > 0
    print("positive")
else
    if x < 0
        print("negative")
    end
end
```

### Loops
```
i = 0
while i < 5
    print(i)
    i = i + 1
end
```
Use `break` to exit the innermost loop early:
```
while 1
    if done == 1
        break
    end
end
```

## Functions
```
func add(a, b)
    return a + b
end

print(add(2, 3))
```
A bare `return` returns nothing. Functions are first-class values (`type(add)` is `"func"`), so they can be passed as arguments or returned from other functions.

There is no variable shadowing: a function's local environment can read from its parent environment but cannot modify it.

## Arrays & Indexing
Arrays are indexed with `:`, and `arr:idx = val` is the only way to mutate an array in place:
```
nums = [10, 20, 30]
print(nums:0)  // 10
nums:1 = 99    // nums is now [10, 99, 30]
```

Arrays are copied by value when assigned to a variable or passed to a function:
```
a = [1, 2, 3]
b = a
b:0 = 99
print(a:0)  // 1; b is an independent copy

func mutate(x)
    x:0 = 999
end
mutate(a)
print(a:0)  // 1; x was a copy of a
```

## Module Imports
```
import "math.mic"

print(pow(5, 2))
```
The imported file runs in the current environment, sharing variable and function scope. Paths resolve relative to the importing file.

## Built-in Functions
| Function | Returns | Description |
|---|---|---|
| `print(x)` | | Prints `x` |
| `input(x)` | | Prompts with `x` and reads a line |
| `type(x)` | `str` | Type of `x` (`"int"`, `"arr"`, etc.) |
| `conv(x, t)` | `<t>` | Converts `x` to `"int"`, `"float"`, `"str"`, or `"arr"` |
| `len(x)` | `int` | Length of an array or string |
| `add(a, i, x)` | `arr` | Copy of `a` with `x` inserted at index `i` |
| `del(a, i)` | `arr` | Copy of `a` with the item at index `i` removed |

`add` and `del` return a modified copy and never mutate the original.

## Grammar Reference
```
V = X                                 assignment
if X ... else if X ... else ... end   conditional
while X ... end                       loop
func X(Y, Z, ...) ... end             function definition
break                                 exit innermost loop
return X                              return from function
import X                              import file
// COMMENT                            comment

A:I       index into array A
A:I = X   assign into array A at index I
```
