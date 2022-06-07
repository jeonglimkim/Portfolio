from sys import stdin
import sys

x,y = map(int, stdin.readline().split())
left = 1
right = 2000000000
winrate = (y * 100 / x)

if winrate >= 99:
    print(-1)
    sys.exit()
answer = 0

while left <= right:
    mid = (left + right) // 2
    if int((y + mid) * 100 / (x + mid)) > winrate:
        answer = mid
        right = mid - 1
    else:
        left = mid + 1
        
print(answer)