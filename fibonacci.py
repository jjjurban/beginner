def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b
    print()

try:
    num = int(input("How many Fibonacci numbers would you like? "))
    if num < 1:
        print("Please enter a positive number.")
    else:
        fibonacci(num)
except ValueError:
    print("Invalid input! Please enter an integer.")
