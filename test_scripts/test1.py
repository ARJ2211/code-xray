import random

def generate_random_list(length, min_val, max_val):
    """Generates a list of random integers."""
    return [random.randint(min_val, max_val) for _ in range(length)]

def calculate_average(numbers):
  """Calculates the average of a list of numbers."""
  if not numbers:
    return 0
  return sum(numbers) / len(numbers)

def find_max_and_min(numbers):
  """Finds the maximum and minimum values in a list."""
  if not numbers:
    return None, None
  return max(numbers), min(numbers)

def main():
  """Main function to execute the script."""
  list_length = random.randint(10, 20)
  min_value = 1
  max_value = 100
  random_list = generate_random_list(list_length, min_value, max_value)
  print("Generated List:", random_list)

  average = calculate_average(random_list)
  print("Average:", average)

  max_val, min_val = find_max_and_min(random_list)
  print("Maximum Value:", max_val)
  print("Minimum Value:", min_val)

  #Demonstrates list comprehension
  even_numbers = [num for num in random_list if num % 2 == 0]
  print("Even Numbers:", even_numbers)
  
  #Illustrates use of enumerate
  print("Index and Value pairs:")
  for index, value in enumerate(random_list):
      print(f"Index: {index}, Value: {value}")

if __name__ == "__main__":
    main()