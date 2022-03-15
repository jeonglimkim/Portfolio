
def digit_sum(x):
    n = 0
    while x > 0:
        t = x % 10
        x = x // 10
        n = n + t
    return n


if __name__ == "__main__":
    N = int(input())
    nums = list(map(int, input().split()))
    max_value = 0
    answer = -1
    
    for i in range(N):
        temp = digit_sum(nums[i])
        if temp > max_value:
            max_value = temp
            answer = i
            
    print(nums[answer])
    