from sys import stdin

def Budget(mid):
    budget = 0
    for x in nums:
        if x >= mid:
            budget += mid
        else:
            budget += x
    return(budget)


if __name__ == "__main__":
    
    n = int(stdin.readline()) #지방의 수 
    nums = list(map(int, stdin.readline().split())) #각 지방의 예산요청
    m = int(stdin.readline()) #총 예산
    left = 1
    right = max(nums)
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2 #mid = 상한액
        if Budget(mid) <= m :
            left = mid + 1
            answer = mid #최대를 늘리고 
        else:
            right = mid - 1 #최대를 줄이고
            
    print(answer)