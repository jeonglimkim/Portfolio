
if __name__ == "__main__":
    a = int(input())
    b = int(input())
    c = int(input())
    n = a * b * c
    nums = [0] * 10 
    
    while n != 0:
        r = n % 10
        nums[r] += 1
        n = n // 10
    
    for i in range(10):
        print(nums[i])

