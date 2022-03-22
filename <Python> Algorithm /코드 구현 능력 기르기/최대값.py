if __name__ == "__main__":
    nums = []
    for i in range(9):
        nums.append(int(input()))
    
    print(max(nums))
    print(nums.index(max(nums))+1)