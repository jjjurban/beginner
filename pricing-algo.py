#pricing algo for rendex
#author: @j.j.j.urban
#different intervals for every meter square to adjust the price
#intervals
        #0-50m2         6x
        #51-100m2       5x+50
        #101-200m2      4x+150
        #201-500m2      3x+350
        #501-1000m2     2x+850
        #1001-2000m2    x+1850
        #2001-5000m2    x/2+3850
        #5001-10000m2   x/4+7850
        #10001+ m2      x/8+15850

#for the intervals the price changes according to the square meters 
#JEDNA SA O PODLAHOVU PLOCHU

import math

def calculate_price(square_meters, type_of_render):
    if square_meters <= 50:
        price = (6 * square_meters) * 1.12
    elif square_meters <= 100:
        price = (5 * square_meters + 50) * 1.12
    elif square_meters <= 200:
        price = (4 * square_meters + 150) * 1.12
    elif square_meters <= 500:
        price = (3 * square_meters + 350) * 1.12
    elif square_meters <= 1000:
        price = (2 * square_meters + 850) * 1.12
    elif square_meters <= 2000:
        price = (square_meters + 1850) * 1.12
    elif square_meters <= 5000:
        price = ((square_meters / 2) + 3850) * 1.12
    elif square_meters <= 10000:
        price = ((square_meters / 4) + 7850) * 1.12
    else:
        price = ((square_meters / 8) + 15850) * 1.12
    
    if type_of_render in ["interior", "exterior"]:
        price *= 0.75
    
    return math.ceil(price)

# Loop for continuous testing
while True:
    try:
        square_meters = float(input("Enter square meters (or type 'exit' to quit): "))
        type_of_render = input("Enter type (interior/exterior/both): ").strip().lower()
        if type_of_render not in ["interior", "exterior", "both"]:
            print("Invalid input. Please enter 'interior', 'exterior', or 'both'.")
            continue
        price = calculate_price(square_meters, type_of_render)
        print(f"The price for {square_meters} m² ({type_of_render}) is {price} euros.")
    except ValueError:
        print("Exiting...")
        break
