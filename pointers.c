#include <stdio.h>

// Function to demonstrate basic pointer usage
void pointer_basics() {
    int num = 10;  // Declare an integer variable
    int *ptr = &num;  // Declare a pointer to an integer and store the address of 'num'
    
    printf("\n=== Step 1: Understanding Pointers ===\n");
    printf("An integer variable 'num' is declared and initialized to 10.\n");
    printf("A pointer 'ptr' is declared and assigned the address of 'num'.\n");
    printf("num = %d\n", num);
    printf("&num (Address of num) = %p\n", (void*)&num);
    printf("ptr (Pointer to num) = %p\n", (void*)ptr);
    printf("*ptr (Value at ptr) = %d\n\n", *ptr);
}

// Function to modify a variable using a pointer
void pointer_modification() {
    int num = 20;
    int *ptr = &num; // Pointer stores address of 'num'
    
    printf("\n=== Step 2: Modifying Value Through Pointer ===\n");
    printf("Initially, 'num' is set to 20. A pointer 'ptr' is assigned its address.\n");
    printf("Before modification: num = %d\n", num);
    *ptr = 30; // Modifies 'num' via pointer
    printf("Using '*ptr = 30', we modify 'num' through the pointer.\n");
    printf("After modification: num = %d\n\n", num);
}

// Function to demonstrate pointer arithmetic
void pointer_arithmetic() {
    int arr[3] = {5, 10, 15};
    int *ptr = arr; // Pointer points to first element of 'arr'
    
    printf("\n=== Step 3: Pointer Arithmetic ===\n");
    printf("An array 'arr' is declared with values {5, 10, 15}.\n");
    printf("A pointer 'ptr' is assigned to the first element of 'arr'.\n");
    printf("Array elements using pointer arithmetic: \n");
    for (int i = 0; i < 3; i++) {
        printf("Element %d: %d (Address: %p)\n", i, *(ptr + i), (void*)(ptr + i));
    }
    printf("\n");
}

int main() {
    pointer_basics();
    pointer_modification();
    pointer_arithmetic();
    
    printf("\n=== Summary of Important Pointer Symbols ===\n");
    printf("* 'int *ptr'      -> Declares a pointer to an integer\n");
    printf("* '&var'          -> Gets the memory address of 'var'\n");
    printf("* '*ptr'          -> Dereferencing: Accesses value at the pointer’s address\n");
    printf("* 'ptr + i'       -> Pointer arithmetic: Moves pointer 'i' elements forward\n");
    printf("* '*(ptr + i)'    -> Accesses value at 'ptr + i' (used for arrays)\n\n");
    
    return 0;
}