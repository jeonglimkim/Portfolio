

if __name__ == "__main__":
    nums = [0] * 42
    
    for _ in range (10):
        n = int(input())
        nums [n % 42] += 1
    
    print(42 - nums.count(0))