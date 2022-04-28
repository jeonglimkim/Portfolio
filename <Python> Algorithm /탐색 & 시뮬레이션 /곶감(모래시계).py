
if __name__ == "__main__":
    n = int(input())
    nums = [list(map(int, input().split())) for _ in range(n)]
    m = int(input())
    answer = 0
    start = 0
    end = n - 1
    
    for _ in range(m):
        row, dir, move = map(int, input().split())
    
        if dir == 0:
            for _ in range(move):
                nums[row - 1].append(nums[row - 1].pop(0)) 
        else:
            for _ in range(move):
                nums[row - 1].insert(0, nums[row - 1].pop()) 
        
    for i in range(n):
        for j in range(start, end+1):
            answer += nums[i][j]
        if i < n//2: 
            start += 1
            end -= 1
        else:
            start -= 1
            end += 1

    print(answer)