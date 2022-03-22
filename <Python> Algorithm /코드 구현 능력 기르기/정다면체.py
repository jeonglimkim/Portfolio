
if __name__ == "__main__":
    N, M = map(int, input().split())
    case = [0] * (N + M + 1)
    
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            case[i+j] = case[i+j] + 1
    
    max_value = max(case)
    
    for i in range(len(case)): 
        if max_value == case[i]:
            print(i, end = " ")
            
