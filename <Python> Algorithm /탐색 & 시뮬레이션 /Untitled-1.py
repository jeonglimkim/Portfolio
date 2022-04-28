if __name__ == "__main__":
    n = int(input())
    nums = [list(map(int, input().split())) for _ in range(n)]

    answer = 0
    
    for i in range(n):
        if answer < sum(nums[i]):
            answer = sum(nums[i])
    
    for i in range(n):
        temp = 0
        for j in range(n):
            temp += nums[j][i]
        if answer < temp:
            answer = temp
 
    temp1 = 0
    temp2 = 0
       
    for i in range(n):
        temp1 = nums[i][i]
        temp2 = nums[i][n-1-i]
        if answer < temp1:
            answer = temp1
        if answer < temp2:
            answer = temp2
    
    print(answer)