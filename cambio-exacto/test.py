denominations_input = '1 3 4 5'
limits_input = '5 2 2 1'
target_input = '7'

denominations = list(map(int, denominations_input.split()))
limits = list(map(int, limits_input.split()))
target_amount = int(target_input)

print(f"Denominations: {denominations}")
print(f"Limits: {limits}")
print(f"Target Amount: {target_amount}")