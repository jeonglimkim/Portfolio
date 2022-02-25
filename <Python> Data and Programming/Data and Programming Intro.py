# Question 1: The Pythagorean theorem says that the sides of a right triangle follow the formula:
# a squared + b squared = c squared
# where c is the hypotenuse. Write code that takes in the variables a and b, then prints out the
# length of the hyptenuse, the area of the triangle (one half base times height) and the perimeter
# (the sum of all three sides)

a = 3
b = 4
c = (a ** 2 + b ** 2) ** 0.5
area = 0.5 * a * b
perimeter = a + b + c 
print(area)
print(perimeter)


# Question 2: For any given rectangle, the area is simply its base times its height, and its perimeter
# is the sum of all four sides. Create a dictionary where the keys are a, b, area, and permieter. Fill
# in any values for a and b, and have the dictionary values for area and permiter calculated.

a = 5
b = 5
dict = {'length' : a, 'width': b, 'area': a * b, 'perimeter': 2 * a + 2 * b}
print(dict)

# Question 3: A palindrome is a word or phrase that is the same both forwards and backwards. Write code
# that takes a variable of any string, then tests to see whether it qualifies as a palindrome. Make sure
# it works on the word "radar" and the phrase "A man, a plan, a canal, Panama!", while rejecting the
# word "Apple" and the phrase "This isn't a palindrome". Print the result.

my_str = "A man, a plan, a canal, Panama!"
getVals = list([val for val in my_str if val.isalpha()])

just_str = "".join(getVals).lower()
just_str_reverse = just_str[::-1]
print(just_str)
print(just_str_reverse)

if just_str == just_str_reverse:
   print("This is a palindrome.")
else:
   print("This is not a palindrome.")    

# Question 4: Using a for loop, write code that takes in any list of objects, then prints out:
# "The value at position __ is __."
# for every element in the loop, where the first blank is the index location and the second blank is
# the object at that index location.

statement = "The value at position {} is {}."
barn = ["horse", "cat", "dog", "pig"]
for animal in barn:
    print(statement.format(barn.index(animal), animal))    

# Question 5: Create a list containing the values 10, 2, 3, 3, and 5, in that order. Then, using a list
# comprehension, reverse the list and add each element together with the value at the same position in the
# original list. For example, if a list contains 1 and 3, the reversed version contains 3 and 1. Then
# summing the first elements gives you 1+3=4, and the second elements gives you 3+1=4, for a final list of
# 4 and 4. Finally, remove duplicate values and print the result.

original = [10, 2, 3, 3, 5]
print([sum(reverse) for reverse in zip(original, reversed(original))])