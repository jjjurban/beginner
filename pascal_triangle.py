def generate_pascals_triangle(rows):
    triangle = []

    for row_num in range(rows):
        row = [None for _ in range(row_num + 1)]  # Create a row with 'None' placeholders
        row[0], row[-1] = 1, 1  # Set the first and last elements to 1

        # Fill in the interior values
        for j in range(1, len(row) - 1):
            row[j] = triangle[row_num - 1][j - 1] + triangle[row_num - 1][j]

        triangle.append(row)

    return triangle

# Ask the user for input
try:
    num_rows = int(input("How many rows of Pascal's Triangle would you like? "))
    if num_rows < 1:
        print("Please enter a positive number.")
    else:
        triangle = generate_pascals_triangle(num_rows)

        # Determine the maximum width of the numbers in the last row for symmetry
        max_width = len(str(triangle[-1][len(triangle[-1]) // 2]))  # Width of the largest number

        for row in triangle:
            # Print each row with a single space between numbers
            row_str = ' '.join(str(num) for num in row)
            # Calculate the padding for each row to maintain symmetry
            print(row_str.center(num_rows * (max_width + 1)))  # Adjust spacing based on the number of rows
except ValueError:
    print("Invalid input! Please enter an integer.")
