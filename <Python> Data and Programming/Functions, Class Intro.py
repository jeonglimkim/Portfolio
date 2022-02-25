# Question 1: Write a function that takes any list of numbers as its input, then returns a dictionary
# with keys "length", "num_unique", "sum", "mean", and "median", with the values being the length of
# the list, the number of distinct values that appear in the list, the sum of all the values, the
# average of the values, and the median of the values, respectively. Print the result on this list as
# your answer:
from numpy import mean, median

q1_list = [33, 33, 12, 7, 4, 0, 0, 0, 0, 7]

def q1_func(x):
    length = len(x),
    num_unique = set(x),
    q1sum = sum(x),
    q1mean = mean(x),
    q1median = median(x)
    return {"length":length, "num_unique": num_unique, "sum": q1sum, "mean":q1mean, "median": q1median}

print(q1_func(q1_list))

 
# Question 2: Take the list below, and then write code to map a function onto each value in the list,
# generating a new list with the modified results.  You must use both a list comprehension and a function.
# What happens inside the function can be trivial as long as it does something to change the value.

q2_list = ['alex', 'molly', 'yihao', 'ellie', 'ashu']

def q2_func(x):
    return [y + ' is nice' for y in x]

print(q2_func(q2_list))


# Question 3: Create a class called StudentRecord.  Have it require three instance variables when created:
# one for the student's name, one for the student's major, and one for the student's GPA.
#
# Then create instances for three students: Jill - economics - 3.75, Jim - sociology - 3.1, Jose - economics - 3.9
#
# Write three methods for this class:
#     The first one named "summary", which prints out a one-sentence summary of the student's records
#       (e.g. "Jose is an economics major, and...")
#     The second one named "get_data", which returns a simple list of the students three values (name, major, gpa)
#     The third one named "same_major", which takes as an argument another student's StudentRecord
#       instance, and then prints whether or not the two students have the same major or not
#
# For your final answer, print Jill's summary, Jill's raw data values, and the answer to whether Jill shares a major
# with Jim and with Jose.

class StudentRecord():
    def __init__(self, name, major, GPA):
        self.name = name
        self.major = major
        self.GPA = GPA
        
    def summary(self):
        print ("{} is an {} major and has a GPA of {}.".format(
                    self.name,
                    self.major,
                    self.GPA))
        
    def get_data(self):
        print ([self.name, self.major, self.GPA])
    
    def same_major(self, other):
        other.major = other. major
        other.name = other.name
        if self.major == other.major:
            print("{} and {} have the same major.".format(
                self.name, 
                other.name))
        else:
            print("{} and {} do not have the same major.".format(
                self.name,
                other.name))
            
Jill = StudentRecord("Jill", "economics", 3.75)
Jim = StudentRecord("Jim", "sociology", 3.1)
Jose = StudentRecord("Jose", "economics", 3.9)

Jill.summary()
Jill.get_data()
Jill.same_major(Jim)
Jill.same_major(Jose)