
if __name__ == "__main__":
    n = int(input())
    nums = list(map(int, input().split()))
    answer = 0
    sum = 0
    
    for i in range(n):
        if nums[i] == 1:
            answer += 1
            sum += answer
        else:
            answer = 0
    
    print(sum)