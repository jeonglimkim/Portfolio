
if __name__ == "__main__":
    n = int(input())
    nums = [list(map(int, input().split())) for _ in range(n)]
    
    start = end = n//2
    answer = 0
    for i in range(n):
        for j in range(start, end+1):
            answer += nums[i][j]
        if i < n//2:
            start -= 1
            end += 1
        else:
            start += 1
            end -= 1
            
    print(answer)