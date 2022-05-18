
if __name__ == "__main__":
    n, m = map(int, input().split())
    nums = list(map(int, input().split()))
    nums.sort()
    
    left = 0
    right = n - 1
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < m:
            left = mid + 1
        elif nums[mid] > m:
            right = mid - 1
        else:
            answer = mid
            break
    
    print(answer + 1)