
def reverse(x):
    n = 0
    while x > 0:
        t = x % 10
        x = x // 10
        n = n * 10 + t
    return n
    
def isPrime(x):
    if x == 1:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True


if __name__ == "__main__":
    N = int(input())
    nums = list(map(int, input().split()))
    
    for i in range(N):
        temp = reverse(nums[i])
        if isPrime(temp):
            print(temp, end=" ")
            
            