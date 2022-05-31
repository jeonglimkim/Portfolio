from sys import stdin

def Cut(mid): 
    cnt = 0
    for x in nums:
        if x > mid :
            cnt += x - mid
    return(cnt) 

if __name__ == "__main__":
    
    n, m = map(int, stdin.readline().split())
    nums = list(map(int, stdin.readline().split()))
    left = 0
    right = max(nums)
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if Cut(mid) >= m:
            left = mid + 1 
            answer = mid
        else:
            right = mid - 1 
    
    print(answer) 
    