from sys import stdin

def DVD(mid):
    cnt = 1 #there should be at least one DVD
    sum = 0
    for x in nums:
        if sum + x > mid:
            cnt += 1
            sum = x
        else:
            sum += x
    return(cnt)        
    

if __name__ == "__main__":
    
    n, m = map(int, input().split())
    nums = list(map(int, stdin.readline().split()))
    left = 1
    right = sum(nums)
    answer = 0
    minn = max(nums) #a DVD has to hold at least the max of nums
    
    while left <= right:
        mid = (left + right) // 2 #mid = time
        if DVD(mid) <= m and minn <= mid:
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
            
    print(answer)
            