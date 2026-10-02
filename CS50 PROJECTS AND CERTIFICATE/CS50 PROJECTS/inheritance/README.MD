# Blood Type Inheritance

A C program that simulates the inheritance of blood type alleles across multiple generations.

## Overview

The program creates a family tree using a recursive data structure. Each person has two parents and two blood type alleles.

The program randomly generates the alleles of the oldest generation and then uses the parents' alleles to determine the alleles inherited by each subsequent generation.

It then prints the resulting family tree and blood type alleles.

## Concepts Demonstrated

- C structs
- Pointers
- Recursive functions
- Dynamic memory allocation
- Memory management with `malloc` and `free`
- Random number generation
- Tree data structures

## How It Works

The program creates a family tree with three generations.

Each `person` contains:

- Two pointers to their parents
- Two blood type alleles

The parents are generated recursively. Each person's alleles are then randomly selected from one allele of each parent.

After the family tree is printed, the program recursively frees the allocated memory.

## Example Output

```text
Child (Generation 0): blood type AB
    Parent (Generation 1): blood type AO
        Grandparent (Generation 2): blood type BO
        Grandparent (Generation 2): blood type OO
    Parent (Generation 1): blood type BB
        Grandparent (Generation 2): blood type AB
        Grandparent (Generation 2): blood type BB