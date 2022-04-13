if __name__ == "__main__":
    n = int(input())

    
    for i in range(n):
        answer = 0
        sum = 0
        quiz = list(input())
        
        for j in quiz:
            if j == "O":
                answer += 1
                sum += answer
            else:
                answer = 0
            
        print(sum)
    