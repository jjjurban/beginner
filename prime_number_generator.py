def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    """Generate the first 'count' prime numbers."""
    primes = []
    num = 2  # Start checking from 2 (first prime number)
    
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes

# Ask the user for input
try:
    num_primes = int(input("How many prime numbers would you like? "))
    if num_primes < 1:
        print("Please enter a positive number.")
    else:
        print(generate_primes(num_primes))
except ValueError:
    print("Invalid input! Please enter an integer.")
