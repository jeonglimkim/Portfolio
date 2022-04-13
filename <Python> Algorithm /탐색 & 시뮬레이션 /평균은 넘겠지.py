
if __name__ == "__main__":
    c = int(input())
    
    for i in range(c):
        case = list(map(int, input().split()))
        average = sum(case[1:])/case[0]
        
        cnt = 0
        for j in case[1:]:
            if j > average:
                cnt += 1
        
        result = (cnt/case[0]) * 100
        print('%.3f' %result + '%')