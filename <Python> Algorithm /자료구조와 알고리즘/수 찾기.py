
if __name__ == "__main__":
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    m = int(input())
    b = list(map(int, input().split()))
    
    for i in range(m):
        left = 0
        right = n-1
        answer = False
        while left <= right:
            mid = (left + right) // 2
            if a[mid] < b[i]:
                left = mid + 1
            elif a[mid] > b[i]:
                right = mid - 1
            else:
                answer = True
                break
        if answer == True:
            print(1)
        else:
            print(0)
                