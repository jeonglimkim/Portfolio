
def DFS(v):
    if v == 0:
        return
    else:
        DFS(v // 2)
        print (v % 2, end = "")
        
        
if __name__ == "__main__":
    n = int(input())
    DFS(n)