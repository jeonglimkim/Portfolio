from sys import stdin

if __name__ == "__main__":
    def Count():
        cnt = 0
        for x in a:
            cnt += x
        return cnt
    
    k, n = map(int, input().split())
    a = list(map(int, stdin.readlines()))
    left = 0
    right = max(a)
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if Count(mid) >= n:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    print(answer)