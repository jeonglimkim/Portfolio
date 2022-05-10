
if __name__ == "__main__":
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    n = int(input())
    nums = [list(map(int, input(). split())) for _ in range(n)]
    
    nums.insert(0, [0]*n)
    nums.append([0] * n)
    
    for l in nums:
        l.insert(0, 0)
        l.append(0)
    
    cnt = 0
    
    for i in range(1, n+1):
        for j in range(1, n+1):
            if all (nums[i][j] > nums[i + dx[k]][j + dy[k]] for k in range(4)):
                cnt += 1
                
    print(cnt)
        
    
    
    