# Course notes  

This is where I will keep all my notes, questions asked in lectures and so on.  

### Serial code optimization  

#### general utilities:  

turning division into multiplications  
```
for loop: exp/a
vs
a_inv = 1/a
for loop: exp*a_inv
```


polynomials, Horners rule:  
((((ax + b)x + c)x + d)x + e)


#### Writing out powers  

`x*x*x` faster than `pow(x, 3)`

#### Loop factorizing
is the idea to keep loops as flat as possible
and pre compute reused values if possible

```C
for (i=0; i<ARRAY_SIZE; i++) {
    a[i] = 0.;
    for (j=0; j<ARRAY_SIZE; j++)
        a[i] = a[i] + b[j]*d[j];
    a[i] = a[i]*c[i];
}

```

```C
t = 0.;
for (j=0; j<ARRAY_SIZE; j++)
    t = t + b[j]*d[j];
for (i=0; i<ARRAY_SIZE; i++)
    a[i] = t*c[i];
```

#### Keep expensive functions out of the loop  

sin() is an expensive function: precomute if you can.  

```C
for (i=0; i<N; i++)
    A[i] = A[i] + s + r*sin(x);
⇓
tmp = s + r*sin(x);
for (i=0; i<N; i++)
    A[i] = A[i] + tmp;
```



#### Lookup tables  

if we know what the possible agruments of an expensive function is


## Personal goals for this course  

* Become a nimble C programmer  
  - Be able to write C programs quickly without having to look up basic stuff  
* Learn general HPC techniques to write more efficient code  
* Gain a foundation of knowledge for creating high-performance interfaces to high-level languages

## Questions and answers  

What are some established code standards we can follow to write idiomatic C code?
Do we have multiple to choose between?

What are the pros and cons of representing an n-dimensional array/tensor as
a 1d array versus nested arrays/array pointers? I have seen examples of both in HPC

1d array always better for performance reasons/physical alignment

Q:  
When will we learn more about the numerical projects?  
* Do we have to work in groups or solo?
* What creative freedom do we have?
    - Can we propose a topic or do we pick one
    - Can we use related, out-of-curriculum technology? E.g. GPU programming such as CUDA?

A:  
We will probably all get the same numerical project.  

Q: What is the benefit of macros?

A: functions have its own scope meaning the point to a different place in memory. Macros are like copy pasting an expression making them closer in memory (i.e. no context/scope switching)


Q:
Performance on pure 1darray vs nd-array pointing to underlying 1d array

Q:
Floating point operations: do they have a constant number of instructions?
The same goes for "complex operations" as pipeline bubbles

Q:
can you pipeline tasks with repetition of instructions? I'd imagine it will delay somewhat

## Remember this:

You cannot write to an unitialized pointer:
```C
int *C;
foo(C);
```
instead do
```C
int C
foo(&C)
```
