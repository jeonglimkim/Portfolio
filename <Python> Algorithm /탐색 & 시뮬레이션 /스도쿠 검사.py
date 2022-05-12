import sys 

if __name__ == "__main__":
    puzzle = [list(map(int, input().split())) for _ in range(9)]
    
    for i in range(9): 
        row = [0] * 10     
        col = [0] * 10
        for j in range(9):
            row[puzzle[i][j]] = 1 
            col[puzzle[j][i]] = 1
        if sum(row) != 9 or sum(col) != 9:
            print("NO")
            sys.exit(0)
    
    for i in range(3): # 9*9 시작점
        for j in range(3):
            nums = [0] * 10
            for k in range(3): # 3*3의 element
                for l in range(3):
                    nums[puzzle[i*3+k][j*3+l]] = 1
            
            if sum(nums) != 9:
                print("NO")
                sys.exit(0)
                        
    print("YES")