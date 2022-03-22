import numpy as np

if __name__ == "__main__":
    N = int(input())
    students = list(map(int, input().split()))
    avg = round(np.average(students))
    number = 0
    min = 2147000000
    
    for index, score in enumerate(students):
        temp = abs(score-avg)
        if temp < min:
            min = temp
            present = score
            number = index + 1 
        elif temp == min:
            if present < score:
                present = score
                number = index + 1
    
    print(avg, number)
    