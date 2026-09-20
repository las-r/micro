# micro
A small, generic interpreted scripting language.

## Overview
micro is a minimal, dynamically-typed scripting language with somewhat Ruby-like syntax, first-class functions, and arrays. It's designed to be small enough to read the whole implementation in one sitting, while still being expressive enough for real programs.

The entirety of the source code, without any minification, is under 500 lines.

## Getting Started
```
python -m micro yourfile.mic
```

## Data Types
| Type | Description |
|---|---|
| `int` | Whole numbers |
| `float` | Decimal numbers |
| `str` | Strings, written `"like this"` |
| `arr` | Arrays, written `[1, 2, 3]` |
| `func` | Functions (first-class, see [below](https://github.com/las-r/micro#functions)) |

There is no dedicated boolean type. Comparisons and logic operators produce `int`s (`0` for false, any nonzero value, conventionally `1`, for true), and `if`/`while` treat any nonzero value as true.

## Variables
Variables don't need to be declared, assigning to a name creates it:
```
x = 10
name = "micro"
nums = [1, 2, 3]
```

## Operators
**Arithmetic:** `+`, `-`, `*`, `/`, `%`\
**Bitwise:** `~` (not / negate), `&` (and), `|` (or), `^` (xor)\
**Comparison:** `==`, `<`, `<=`, `>`, `>=`\
**Logic:** `!` (not), `&&` (and), `||` (or)

## Control Flow
**Conditionals:**
```
if x > 0
    print("positive")
else
    print("non-positive")
end
```
The `else` branch is optional.

**Loops:**
```
i = 0
while i < 5
    print(i)
    i = i + 1
end
```

Use `break` to exit a loop early:
```
while 1
    if done == 1
        break
    end
end
```

## Functions
Define a function with `func`, and return a value with `return` (a bare `return` with no expression returns nothing):
```
func add(a, b)
    return a + b
end

print(add(2, 3))
```

Functions are values (`type(add)` returns `"func"`) and can be passed as arguments.

## Arrays and Indexing
Arrays are created with `[...]` and indexed with `:`:
```
nums = [10, 20, 30]
print(nums:0)      // 10
nums:1 = 99        // nums is now [10, 99, 30]
```

### Array semantics
Arrays are copied whenever they're assigned to a variable or passed as a function argument. This means:
```
a = [1, 2, 3]
b = a
b:0 = 99
print(a:0)  // 1; b is an independent copy, not the same array as a

func mutate(x)
    x:0 = 999
end
a = [1, 2, 3]
mutate(a)
print(a:0)  // 1; the function got its own copy of a
```

This copying is shallow. Indexing into an array (`arr:i = val`) always mutates that array's own storage in place, which is how you make changes stick within a single variable.

## Imports
Import another `.mic` file with `import`:
```text
import "math.mic"

print(square(5))
```

The imported file is executed in the current environment, so any variables or functions it defines become available to the importing file.

Import paths are resolved relative to the file containing the import.

## Comments
```
// this is a comment, running to the end of the line
```

## Built-in Functions
| Function | Return Type | Description |
|---|---|---|
| `print(x)`      | | Prints `x` |
| `input(x)`      | | Prompts with `x` and reads a line |
| `type(x)`       | `str` | Returns the type of `x` (`"int"`, `"arr"`, etc.) |
| `conv(x, t)`    | `<t>` | Converts `x` to type `t` (`"int"`, `"float"`, `"str"`, `"arr"`) |
| `len(x)`        | `int` | Length of an array or string |
| `add(a, i, x)`  | `arr` | Returns a copy of `a` with `x` inserted at index `i` |
| `del(a, i)`     | `arr` | Returns a copy of `a` with the item at index `i` removed |

`add` and `del` never modify the original array, instead they return a new one.

## Grammar Reference
```
V = X                       assignment
if X ... else ... end       conditional
while X ... end             loop
func X(Y, Z, ...) ... end   function definition
break                       exit innermost loop
return X                    return from function
// COMMENT                  comment

A:I                         index into array A
A:I = X                     assign into array A at index I
```

## Example: Factorial
```
func fact(n)
    if n <= 1
        return 1
    end
    return n * fact(n - 1)
end

print(fact(5))  // 120
```