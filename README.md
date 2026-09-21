# micro
A small, generic interpreted scripting language.

## Overview
micro is a minimal, dynamically-typed scripting language with somewhat Ruby-like syntax, first-class functions, and arrays. It's designed to be small enough to read the whole implementation in one sitting, while still being expressive enough for real programs.

The entirety of the source code, without any minification, is under 500 lines.

## Getting Started
### Installation
```sh
pip install git+https://github.com/las-r/aergia
```

### Usage
```sh
python -m micro yourfile.mic
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

There is no dedicated boolean type. Comparisons and logic operators produce `int`s (`0` for false, any nonzero value, conventionally `1`, for true), and `if`/`while` treat any nonzero value as true.

Variables don't need to be explicitly declared, assigning to a name creates it:
```
x = 10
name = "micro"
nums = [1, 2, 3]
```

### Comments
Comments are denoted with 2 slashes, similar to most C-like languages:
```
// This is a comment!
```

### Operators
* **Arithmetic:** `+`, `-`, `*`, `/`, `%`
* **Bitwise:** `~` (not / negate), `&` (and), `|` (or), `^` (xor)
* **Comparison:** `==`, `<`, `<=`, `>`, `>=`
* **Logic:** `!` (not), `&&` (and), `||` (or)

There is no operator precedence besides parentheses. Expressions evaluate strictly left-to-right. For example, `2 + 3 * 4` evaluates to `20`, but `2 + (3 * 4)` evaluates to `14`. 

There is also no `!=` operator, `!(x == y)` is the recommended equivalent.

## Control Flow
### Conditionals
```
if x > 0
    print("positive")
else
    print("not positive")
end
```

The `else` branch is optional.

### Loops
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

Functions are first-class values (`type(add)` returns `"func"`) and can be used as such, such being passed as arguments or returned by another function. 

Assigning to a variable inside a function only affects that function's local copy and never modifies variables from an enclosing scope, even for a nested function.

## Arrays & Indexing
Arrays are created with `[...]` and indexed with `:`:
```
nums = [10, 20, 30]
print(nums:0)  // 10
nums:1 = 99    // nums is now [10, 99, 30]
```

### Array Semantics
Arrays are copied strictly by value whenever they are assigned to a variable or passed as a function argument:
```
a = [1, 2, 3]
b = a
b:0 = 99
print(a:0)  // 1; b is an independent copy

func mutate(x)
    x:0 = 999
end
a = [1, 2, 3]
mutate(a)
print(a:0)  // 1; x was a copy of a
```

This copying is shallow. Direct element assignment (`arr:idx = val`) is the only way to mutate an array in place.

## Module Imports
Import another `.mic` file using `import`:
```
import "math.mic"

print(square(5))
```

The imported file is executed in the current environment, sharing variable and function scope. Import paths are resolved relative to the importing file.

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

`add` and `del` return a modified copy and do not mutate the original array.

## Grammar Reference
```
V = X                       assignment
if X ... else ... end       conditional
while X ... end             loop
func X(Y, Z, ...) ... end   function definition
break                       exit innermost loop
return X                    return from function
import X                    import file
// COMMENT                  comment

A:I                         index into array A
A:I = X                     assign into array A at index I
```
