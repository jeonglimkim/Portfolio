from sys import stdin

if __name__ == "__main__":
    n = int(stdin.readline())
    a = list(map(int, stdin.readline().split()))
    cnt = 0
    answer = ""
    value = 0
    temp = []
    
    left = 0
    right = n - 1
    
    while left <= right:
        if a[left] > value:
            temp.append((a[left], 'L'))
        if a[right] > value:
            temp.append((a[right], 'R'))
        if len(temp) == 0:
            break
        temp.sort()
        answer += temp[0][1]
        cnt += 1
        
        if temp[0][1] == 'L':
            value = a[left]
            left += 1
        else:
            value = a[right]
            right -= 1
        temp.clear()
    
    print(cnt)
    print(answer)