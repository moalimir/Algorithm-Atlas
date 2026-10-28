> To analyze an algorithm effectively, we must shift our mindset from measuring time in seconds to measuring how the workload scales with input size.
> 

### 1. The "Why" and "What": Growth Rate vs. Clock Time

If you run the exact same code on a 2010 smartphone and a modern supercomputer, the execution times will differ vastly. Relying on a stopwatch to evaluate an algorithm is flawed because it depends on:

- The hardware architecture (CPU, RAM).
- The compiler or interpreter being used.
- Other background processes running on the machine.

Instead of measuring absolute time, **Big O notation measures the growth rate of an algorithm's execution time relative to the size of the input, denoted as $N$.** We ask: *If the input size doubles, triples, or grows to one million, how does the number of operations scale?*

### 2. The Three Asymptotic Notations

In academic computer science, there are three primary ways to describe an algorithm's bounds:

- **Big O ($O$): Upper Bound (Worst-Case)**
    
    It guarantees that the algorithm will never perform worse than a certain rate. This is the industry standard for analysis because software engineers must plan for worst-case scenarios.
    
- **Big Omega ($\Omega$): Lower Bound (Best-Case)**
    
    It defines the absolute minimum number of operations required. For example, sorting an already sorted array might take $\Omega(N)$ time.
    
- **Big Theta ($\Theta$): Tight Bound**
    
    This describes an algorithm whose best-case and worst-case growth rates are identical.
    

> **Practical Reality Check:** In interviews and real-world engineering, people often say "Big O" when they technically mean "Big Theta." If someone asks for the Big O of a loop that always runs $N$ times, say $O(N)$, even though it is a tight bound ($\Theta(N)$).
> 

### 3. The Golden Rules of Big O Simplification

When evaluating an algorithm, you will often count a precise number of operations, like
$f(N) = 3N^2 + 5N + 12$. To convert this into Big O notation, you must apply two non-negotiable rules:

### Rule 1: Drop the Constants

We care about the trend line, not the scale. As $N$ approaches infinity, constants become irrelevant.

- $O(2N) \rightarrow O(N)$
- $O(500) \rightarrow O(1)$
- $O(\frac{N}{2}) \rightarrow O(N)$

### Rule 2: Drop Non-Dominant Terms

We look only for the fastest-growing term. If an algorithm has an $N^2$ component and a linear $N$ component, the $N^2$ term completely dominates the total runtime as $N$ grows large.

- $O(N^2 + N) \rightarrow O(N^2)$
- $O(N \log N + N^3 + 45) \rightarrow O(N^3)$

### 4. The Efficiency Spectrum

To quickly evaluate code, you need to memorize the hierarchy of standard complexities.

| **Notation** | **Name** | **Practical Example** |
| --- | --- | --- |
| $O(1)$ | Constant | Accessing an array element by index or looking up a key in a hash map. |
| $O(\log N)$ | Logarithmic | Binary search. The problem space is cut in half with each step. |
| $O(N)$ | Linear | Iterating through an array of size $N$ once. |
| $O(N \log N)$ | Linearithmic | Efficient sorting algorithms like Merge Sort and Quick Sort. |
| $O(N^2)$ | Quadratic | Two nested loops iterating over the same input. |
| $O(2^N)$ | Exponential | Finding all subsets of a set (brute-force recursion). |
| $O(N!)$ | Factorial | Finding all permutations of a string (Traveling Salesperson problem). |

---

## Time Complexity: Analyzing Iterative Code

Analyzing iterative code requires mapping control flow structures (loops, branches, and sequential steps) to mathematical growth rates. When reading code, your goal is to count how many times the most deeply nested operations execute relative to the input size $N$.

Here are the four essential patterns you will encounter in iterative code.

### 1. Sequential Statements (The Addition Rule)

When blocks of code execute one after the other, you compute the complexity of each block individually and add them together.

```python
def sequential_steps(n):
    # Step 1: Constant time operation
    print("Starting analysis")  # O(1)

    # Step 2: Linear loop
    for i in range(n):
        print(i)               # O(N)

    # Step 3: Another linear loop
    for j in range(n):
        print(j)               # O(N)
```

**Mathematical Breakdown:**

$\text{Total Time} = O(1) + O(N) + O(N) = O(1 + 2N)$

Applying the golden rules of simplification (dropping constants), the total time complexity is **$O(N)$**.

### 2. Nested Loops (The Multiplication Rule)

When loops are nested inside one another, the inner loop executes completely for every single iteration of the outer loop. This requires multiplication.

```python
def nested_loops(n):
    for i in range(n):         # Runs N times
        for j in range(n):     # Runs N times for every 'i'
            print(i, j)        # O(1) operation
```

**Mathematical Breakdown:**

$\text{Total Time} = O(N \times N) = O(N^2)$

### The Trait of Dependent Nested Loops

Be careful when the inner loop depends on the outer loop's variable.

```python
def dependent_loops(n):
    for i in range(n):
        for j in range(i, n):  # Starts at 'i', not 0
            print(i, j)
```

The first time, the inner loop runs $N$ times. The second time, $N-1$ times, then $N-2$, down to $1$ time.

The total number of operations is the sum of the first $N$ integers:

$\text{Total Operations} = \frac{N \times (N + 1)}{2} = \frac{N^2 + N}{2}$

Applying our simplification rules (dropping the denominator constant and the non-dominant $N$ term), the complexity is still $O(N^2)$.

### 3. Logarithmic Growth (Dividing the Problem Space)

Logarithmic time complexity, $O(\log N)$, occurs when the amount of work left to do is divided or multiplied by a constant factor at each step. You do not look at every element; you eliminate halves of the data structure.

```python
def logarithmic_loop(n):
    i = 1
    while i < n:
        print(i)
        i = i * 2              # Counter doubles every step
```

If $N = 8$, the loop variable $i$ takes the values: 1, 2, 4, 8. The loop runs 4 times.

Mathematically, we are asking: *To what power must we raise 2 to reach* $N$*?*

$2^x = N \implies x = \log_2 N$

Whenever you see a loop counter doubling, tripling, or halving (`i = i // 2`) on each iteration, the time complexity is **$O(\log N)$**.

### 4. Conditional Branches (Worst-Case Analysis)

When code contains `if/else` structures, different paths may have entirely different complexities. Because Big O looks at the absolute worst-case scenario, you must default to the most expensive branch.

```python
def conditional_branch(n, condition):
    if condition:
        # Branch A: Linear time
        for i in range(n):
            print(i)           # O(N)
    else:
        # Branch B: Quadratic time
        for i in range(n):
            for j in range(n):
                print(i, j)    # O(N^2)
```

Even if `condition` is true 99% of the time, the theoretical Big O complexity of this function is **$O(N^2)$** because we must account for the worst-case path.

---

## Space Complexity: Memory Footprint Analysis

> While time complexity measures the number of operations an algorithm performs, space complexity measures the amount of memory (RAM) an algorithm allocates relative to the input size `N`.
> 

To master space complexity, you must understand where memory is allocated and the critical difference between total space and auxiliary space.

### 1. Total Space vs. Auxiliary Space

When analyzing memory, you will look at two components:

- **Input Space:** The memory required to store the input data itself.
- **Auxiliary Space:** The extra or temporary memory allocated by the algorithm to solve the problem.

> **The Interview Standard:** In almost every software engineering interview, when someone asks for "space complexity," they are specifically asking for **Auxiliary Space**. If a function accepts an array of size `N` as an input and does not create any new data structures, its auxiliary space complexity is `O(1)` (constant), even though the input itself takes up `O(N)` space.
> 

### 2. Primitive Variables and Data Structures

Memory allocation scales differently depending on the types of data you initialize inside your function.

### Constant Space: `O(1)`

Primitive variables (integers, booleans, floats, pointers) require a fixed amount of memory regardless of the input size.

```python
def constant_space(n):
    result = 0             # O(1) space
    for i in range(n):     # i is O(1) space
        result += i
    return result
```

Even though the loop runs `N` times, the variables `result` and `i` are just updated in place. No new memory is created on each iteration. The auxiliary space is `O(1)`.

### Linear Space: `O(N)`

Allocating a collection whose size grows proportionally with the input size creates linear space complexity.

```python
def linear_space(n):
    visited_set = set()    # Space scales with N
    for i in range(n):
        visited_set.add(i) 
    return visited_set
```

Because `visited_set` will store exactly `N` elements by the end of the execution, the auxiliary space complexity is `O(N)`.

### Quadratic Space: `O(N²)`

This typically occurs when creating two-dimensional grids, matrices, or table-like structures used in dynamic programming.

```python
def quadratic_space(n):
    # Creates an N x N matrix initialized to zeros
    matrix = [[0] * n for _ in range(n)]
    return matrix
```

Since the total number of cells stored in memory is `n * n`, the auxiliary space complexity scales quadratically as `O(N²)`.

### 3. The Call Stack (The Hidden Memory Consumer)

Memory is not just allocated via variables and data structures. Every time a function is called, the runtime environment allocates a block of memory called a **stack frame**. This frame stores the function's local variables and execution state.

For iterative code, the call stack remains at a constant depth of `O(1)` because functions return before the next line runs. However, for **recursive algorithms**, stack frames pile up on top of each other until the base case is reached.

Consider this recursive implementation of a counter:

```python
def recursive_countdown(n):
    if n <= 0:
        return
    recursive_countdown(n - 1)
```

If you call `recursive_countdown(5)`, the computer cannot clear the frame for `recursive_countdown(5)` until `recursive_countdown(4)` finishes. This chain continues down to 0, meaning `N` distinct frames exist simultaneously in memory.

- **Iterative countdown:** Time `O(N)`, Space `O(1)`
- **Recursive countdown:** Time `O(N)`, Space `O(N)` (due to the call stack)

---

## Advanced Patterns: Recursion and Divide-and-Conquer

Analyzing recursive and divide-and-conquer algorithms requires a shift from counting loop iterations to tracking how a problem breaks down into smaller subproblems.

> Two powerful tools allow us to crack these complexities: **The Recursion Tree Method** and **The Master Theorem**. We will also explore **Amortized Analysis** for handling algorithms with variable costs.
> 

### 1. The Recursion Tree Method

When a function calls itself multiple times, it creates a branching tree of execution. The recursion tree method helps us visualize two critical components:

1. **The depth of the tree:** How many times the problem can be divided before hitting the base case.
2. **The work per level:** How much non-recursive work is performed at each layer of the tree.

### Example: Merge Sort

Merge Sort divides an array of size $N$ into two halves, recursively sorts them, and then merges the sorted halves. The mathematical recurrence relation is:

$T(N) = 2T\left(\frac{N}{2}\right) + O(N)$

To find the total time complexity using the tree:

- **Tree Height:** The problem size is divided by 2 at each step. An input of size $N$ can be split in half $\log_2 N$ times before reaching a size of 1. Thus, the tree height is $O(\log N)$.
- **Work Per Level:** At the top level, merging takes $O(N)$ time. At the second level, we have 2 subproblems of size $\frac{N}{2}$, which requires $2 \times O(\frac{N}{2}) = O(N)$ work. This linear pattern continues down every single level of the tree.

$\text{Total Time} = (\text{Work per Level}) \times (\text{Tree Height}) = O(N) \times O(\log N) = O(N \log N)$

### Space Complexity of Recursion Trees

Unlike time complexity, which sums up the work across the entire tree, **space complexity only tracks the deepest active path on the call stack at any single moment.**

For Merge Sort, even though there are many recursive branches, the computer executes them sequentially. The call stack never grows deeper than the height of the tree, which is $O(\log N)$.

> **Important Caveat:** Merge Sort requires an extra temporary array to merge elements, which takes $O(N)$ auxiliary space. Because $O(N)$ is larger than the stack space $O(\log N)$, the total auxiliary space complexity of Merge Sort is $O(N)$.
> 

### 2. The Master Theorem

The Master Theorem provides a mechanical cookbook recipe for solving divide-and-conquer recurrence relations instantly. It applies to recurrences that fit this exact template:

$T(N) = aT\left(\frac{N}{b}\right) + f(N)$

Where:

- $a$ is the number of recursive subproblems created.
- $b$ is the factor by which the input size is divided.
- $f(N)$ is the cost of the work done outside the recursive calls (like splitting or merging).

By comparing the work done at the leaves, which is $N^{\log_b a}$, against the work done at the root, $f(N)$, you can immediately determine the Big O shorthand:

| **Condition** | **Dominant Factor** | **Resulting Time Complexity** | **Real-World Example** |
| --- | --- | --- | --- |
| Leaves do more work | Leaf work dominates | $O(N^{\log_b a})$ | Naive Matrix Multiplication |
| Root and Leaves do equal work | Balanced work | $O(f(N) \log N)$ | Merge Sort: $T(N) = 2T(\frac{N}{2}) + O(N) \rightarrow O(N \log N)$ |
| Root does more work | Root work dominates | $O(f(N))$ | Quicksort (Best/Average case Partitioning) |

### 3. Amortized Analysis

Sometimes, evaluating an algorithm by its absolute worst-case scenario yields an inaccurate picture of its real-world performance. Amortized analysis is used when an operation is highly expensive occasionally, but cheap most of the time. We average the total cost of a sequence of operations over time.

### Example: Dynamic Array Resizing (e.g., Python's `list.append()`)

When you append an element to a dynamic array, it usually takes $O(1)$ constant time because there is empty space left in the pre-allocated memory slot.

However, when the array completely fills up, the underlying system must:

1. Allocate a new array that is double the size.
2. Copy all $N$ existing elements into the new array ($O(N)$ work).
3. Insert the new element.

If you look strictly at the worst case, appending is an $O(N)$ operation. But the $O(N)$ resize operation happens incredibly rarely—specifically, only after $N$ sequential $O(1)$ appends have occurred.

$\text{Total Cost for N appends} = (N - 1) \times O(1) + 1 \times O(N) \approx 2N \text{ operations}$

$\text{Amortized Cost per operation} = \frac{2N \text{ operations}}{N \text{ appends}} = O(1)$

Thus, we state that the **amortized time complexity** of appending to a dynamic array is $O(1)$.

We have covered the core theoretical frameworks. Would you like to transition to Topic 5: Multi-Variable and Real-World Complexities to wrap up the roadmap theory, or would you prefer to test your knowledge with a couple of practice code examples?

---

## Multi-Variable and Real-World Complexities

Up to this point, we have treated the input as a single variable, $N$. In production software and technical interviews, however, algorithms frequently process multiple independent datasets, or rely on built-in language methods that hide operational costs under the hood.

To master Big O completely, you must learn to spot these multi-variable inputs and account for the hidden costs of native language APIs.

### 1. Multiple Data Inputs (The $A$ and $B$ Trap)

A classic interview trap is forcing an algorithm to simplify to a single variable when it is mathematically impossible to do so. If an algorithm processes two distinct inputs, you must maintain separate variables in your Big O notation because you cannot predict which input will be larger.

### The Addition Rule with Two Inputs

```python
def print_two_lists(list_a, list_b):
    for item in list_a:
        print(item)            # Scales with len(list_a) -> A

    for item in list_b:
        print(item)            # Scales with len(list_b) -> B
```

Because these loops run sequentially, we add their complexities. The time complexity is **$O(A + B)$**. You cannot simplify this to $O(A)$ or $O(B)$ because $list\_b$ could contain millions of elements while $list\_a$ contains only two, or vice versa.

### The Multiplication Rule with Two Inputs

```python
def match_elements(list_a, list_b):
    for item_a in list_a:      # Runs A times
        for item_b in list_b:  # Runs B times for every item_a
            print(item_a, item_b)
```

Since the loops are nested, we multiply the growth rates. The time complexity is **$O(A \times B)$** (often written as $O(A \cdot B)$).

> **Graph Theory Context:** You will see this constantly in graph algorithms (like Breadth-First Search or Depth-First Search), where the complexity is expressed in terms of both Vertices ($V$) and Edges ($E$), resulting in a time complexity of $O(V + E)$.
> 

### 2. Hidden Complexities in Native Functions

Modern programming languages provide highly optimized built-in methods that look like single statements but actually loop over data under the hood. Treating native methods as $O(1)$ operations is one of the most common mistakes engineers make during complexity analysis.

Here is a breakdown of common hidden costs across popular languages:

| **Operation** | **Native Example (Python / JS)** | **True Complexity** | **Why?** |
| --- | --- | --- | --- |
| **String Concatenation** | `str1 + str2` | $O(M + N)$ | Strings are immutable. The system must allocate new memory and copy both strings element-by-element. |
| **Array Shift/Unshift** | `list.insert(0, val)` / `shift()` | $O(N)$ | Inserting or removing at the *beginning* of an array forces every subsequent element to shift over one index in memory. |
| **Array Slicing** | `array[1:4]` / `slice()` | $O(K)$ | Copying a portion of an array takes time proportional to the length of the slice ($K$). |
| **Value Search** | `if item in dynamic_array` | $O(N)$ | The engine must scan the array from left to right until it finds the element (Linear Search). |
| **Native Sorting** | `sizes.sort()` / `sort()` | $O(N \log N)$ | Under the hood, modern languages use highly optimized algorithms like Timsort or Quicksort. |

### Code Example: The Hidden $O(N^2)$

```python
def build_word(char_list):
    result = ""
    for char in char_list:
        result += char         # Hidden O(K) allocation and copy step!
    return result
```

At first glance, this loop appears to run in $O(N)$ time. However, because string concatenation requires copying the existing string, each step grows progressively more expensive. The actual time complexity of this iterative construction is **$O(N^2)$**.

*The fix:* Use native joining methods like `''.join(char_list)`, which allocate memory efficiently in a single $O(N)$ pass.

### 3. Asymptotic Analysis vs. Practical Reality

Big O notation assumes that the input size $N$ approaches infinity ($N \to \infty$). In the real world, constants and hardware optimization sometimes challenge theoretical bounds:

- **Small Inputs:** An $O(N^2)$ algorithm with a tiny constant factor may run faster than an $O(N \log N)$ algorithm with a huge initialization cost when $N$ is small (e.g., $N < 50$).
- **Cache Locality:** Iterating through a contiguous block of memory (like a primitive array) is significantly faster in practice than traversing a linked list, even if both operations are theoretically $O(N)$. Arrays take advantage of the CPU's memory cache lines.

---

<aside>

## Problems

Here is a curated set of practice problems designed to test the concepts we covered, from basic loops to hidden native complexities.

I recommend reading the code block, formulating your own answer for both Time and Space complexity, and then expanding the breakdown to see if your logic matches.

### Problem 1: The Sliding Window

**Core Concept Tested:** Dependent Nested Loops (Topic 2)

```python
def find_all_pairs(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            print(arr[i], arr[j])
```

**Answer:**

- **Time Complexity:** $O(N^2)$
- **Space Complexity:** $O(1)$

**Breakdown:**

The inner loop does not run $N$ times on every iteration. On the first pass, it runs $N-1$ times. On the second pass, $N-2$ times, continuing down to 1. This forms an arithmetic series ($N-1 + N-2 + \dots + 1$), which sums to roughly $\frac{N^2}{2}$. Dropping the constants leaves us with a time complexity of $O(N^2)$. The space complexity is $O(1)$ because we are only allocating primitive integer variables `n`, `i`, and `j`, regardless of how large the input array grows.

---

### Problem 2: The Two-Step Intersection

**Core Concept Tested:** Multi-Variable Inputs and Native Data Structures (Topic 5)

```python
def get_intersection(list_a, list_b):
    seen = set(list_a)
    intersection = []
    
    for item in list_b:
        if item in seen:
            intersection.append(item)
            
    return intersection
```

**Answer:**

- **Time Complexity:** $O(A + B)$
- **Space Complexity:** $O(A)$

**Breakdown:**

We have two independent inputs, so we must define them as $A$ (length of `list_a`) and $B$ (length of `list_b`).

1. Converting `list_a` to a set takes $O(A)$ time.
2. We then loop over `list_b`, which takes $O(B)$ time.
3. Inside the loop, checking `if item in seen` is an $O(1)$ operation because `seen` is a hash set.
    
    Adding the sequential steps yields a total time of $O(A + B)$.
    

For space, the `seen` set requires $O(A)$ memory. The `intersection` array at worst will hold $\min(A, B)$ elements. Since $O(A + \min(A, B))$ simplifies to $O(A)$ in the worst case (where every element in $A$ is matched), the auxiliary space is $O(A)$.

---

### Problem 3: The Deceptive Halving

**Core Concept Tested:** Geometric Series (Topic 2 & 4)

```python
def count_operations(n):
    count = 0
    while n > 0:
        for i in range(n):
            count += 1
        n = n // 2
    return count
```

**Answer:**

- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

**Breakdown:**

This is a classic interview "gotcha." At first glance, a `while` loop that halves $N$ combined with a `for` loop looks like $O(N \log N)$. However, you must count the actual operations.

If $N = 8$:

- Pass 1: `for` loop runs 8 times.
- Pass 2: `for` loop runs 4 times.
- Pass 3: `for` loop runs 2 times.
- Pass 4: `for` loop runs 1 time.
    
    Total operations: $8 + 4 + 2 + 1 = 15$.
    
    This forms a geometric series. The sum of $N + \frac{N}{2} + \frac{N}{4} + \dots + 1$ is mathematically bounded by $2N$. Dropping the constant gives a true time complexity of $O(N)$.
    

### Problem 4: The Hidden Slicer

**Core Concept Tested:** Call Stack Memory and Native Methods (Topic 3 & 5)

```python
def reverse_string(text):
    if len(text) <= 1:
        return text
    # text[1:] slices the string from index 1 to the end
    return reverse_string(text[1:]) + text[0]
```

**Answer:**

- **Time Complexity:** $O(N^2)$
- **Space Complexity:** $O(N)$

**Breakdown:**

The function calls itself $N$ times to reach the base case, creating a call stack of depth $N$. This makes the auxiliary space $O(N)$.

For time complexity, you must look at the hidden costs of native string operations. In Python and many other languages, strings are immutable. The slicing operation `text[1:]` takes $O(K)$ time, where $K$ is the length of the slice, because it must copy characters into a new string.

On the first call, it copies $N-1$ characters. On the second, $N-2$ characters, down to 1. Just like the sliding window in Problem 1, this arithmetic progression sums to a time complexity of $O(N^2)$.

Here is another batch of problems, stepping up the difficulty. These will test your ability to recognize recursive branching, logarithmic bounds, and some common interview trick questions regarding space complexity.

---

### Problem 5: The Branching Tree

**Core Concept Tested:** Multiple Recursive Calls (Topic 4)

```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    
    # Notice there are TWO recursive calls per function
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
```

**Answer:**

- **Time Complexity:** $O(2^N)$
- **Space Complexity:** $O(N)$

**Breakdown:**

For time complexity, every time the function runs, it branches into two more calls. Those two calls branch into four, then eight, creating a binary tree of execution. The height of this tree is roughly $N$. Because the number of nodes doubles at each level, the time complexity is exponential: $O(2^N)$.

For space complexity, remember that the call stack only holds the deepest *active* path at any given moment. The computer calculates the entire left side of the tree before touching the right side. The maximum depth of this tree is $N$, so the auxiliary space is $O(N)$.

---

### Problem 6: The Boundary Shrinker

**Core Concept Tested:** Logarithmic Time and Pointers (Topic 2)

```python
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

**Answer:**

- **Time Complexity:** $O(\log N)$
- **Space Complexity:** $O(1)$

**Breakdown:**

This is the classic binary search algorithm. In each iteration of the `while` loop, the problem space (`right - left`) is cut perfectly in half. If you start with 100 elements, it goes to 50, then 25, then 12, etc. As discussed in the logarithmic growth section, repeatedly dividing the input by 2 yields a time complexity of $O(\log N)$.

The space complexity is $O(1)$ because we are only allocating three integer pointers (`left`, `right`, and `mid`), and modifying them in place without adding new frames to the call stack.

---

### Problem 7: The Asymmetric Grid

**Core Concept Tested:** Multi-Variable Matrix Traversal (Topic 5)

```python
def search_matrix(matrix, target):
    # matrix is a list of lists (a 2D grid)
    for row in matrix:
        for val in row:
            if val == target:
                return True
    return False
```

**Answer:**

- **Time Complexity:** $O(R \times C)$
- **Space Complexity:** $O(1)$

**Breakdown:**

A common mistake is to automatically call nested loops $O(N^2)$. However, $N$ usually implies a square (where rows and columns are equal). In reality, a matrix might have 2 rows and 1,000,000 columns. Therefore, you must use two variables: $R$ for the number of rows and $C$ for the number of columns. The inner loop runs $C$ times, and the outer loop runs $R$ times, making the time complexity $O(R \times C)$.

The space complexity is $O(1)$ because we are just iterating over existing data and not storing anything new.

---

### Problem 8: The "Trick" Character Counter

**Core Concept Tested:** Bounded Input and Space Complexity Limits (Topic 3)

```python
def first_unique_character(string):
    char_counts = {}
    
    # First pass: count frequencies
    for char in string:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1
            
    # Second pass: find the first unique
    for i in range(len(string)):
        if char_counts[string[i]] == 1:
            return i
            
    return -1
```

**Answer:**

- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$ (with a caveat)

**Breakdown:**

For time, we iterate through the string of length $N$ twice sequentially. $O(N) + O(N) = O(2N)$, which simplifies to $O(N)$.

The space complexity is the trick. You might think it is $O(N)$ because we are storing characters in a dictionary. However, if the input is guaranteed to be standard English ASCII letters, there are only 26 lowercase letters (or 256 total ASCII characters). The dictionary can *never* grow larger than 256 keys, regardless of whether the string is 10 characters or 10 billion characters long. Because the maximum memory ceiling is a constant, the space complexity is strictly $O(1)$.

*(Note: If the character set is undefined or an infinitely growing arbitrary set of symbols, then space becomes $O(N)$ or $O(U)$ where $U$ is the number of unique characters).*

</aside>