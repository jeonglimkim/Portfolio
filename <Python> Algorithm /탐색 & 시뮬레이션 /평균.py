
if __name__ == "__main__":
    n = int(input())
    score = list(map(int, input().split()))
    m = max(score)
    temp = 0
    
    for i in range(n):
        score[i] = score[i] / m * 100
        temp += score[i]
        
    print(temp/n)