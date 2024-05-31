# n 격자의 크기, m 리브로수를 키우는 총 년 수
# 영양제는 좌측 하단에 주어진다.
# 1. 영양제 투입하면 높이 +1 증가
# 2. 영양제 이동
# 3. 영양제 투입한 리브로는 제외하고 2이상인 리브로수는 높이 2를 베어서 그자리에 영양제 자리가 된다.
# 4. n년 동안 반복한다.
import sys
input = sys.stdin.readline
n, m = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(n)]
# d: 이동방향, p: 이동 칸 수

medicine = [[0]*n for _ in range(n)]
# 초기 영양제 투입
medicine[n-1][0] = 1
medicine[n-1][1] = 1
medicine[n-2][0] = 1
medicine[n-2][1] = 1

dx = [0, 1,  1, 0,  -1, -1, -1, 0 , 1]
dy = [0, 0, -1, -1, -1, 0,  1 , 1, 1]

# func 영양제 이동
def move(y,x,p,d) :
    # 먼저 x,y의 값을 그래프 크기로 나눠 나머지를 구한다.
    # 음수일때 그 값을 n을 더하고
    # 양수면서 n 이상이면 %n을 한다.
    dir_x = dx[d]
    dir_y = dy[d]
    medicine[y][x] = 0 
    for _ in range(p):
        y = (dir_y + y) % n
        x = (dir_x + x) % n
        if y < 0:
            y += n
        if x < 0:
            x += n
        if y >= n:
            y = y % n
        if x >= n:
            x = x % n
    return y,x
# func 영양제 대각선에 리브로수 탐색
def search(y,x):
    cnt = 0
    for i in range(2,len(dx),2):
        ny = y + dy[i]
        nx = x + dx[i]
        
        if 0<= ny < n and 0<= nx < n:
            if graph[ny][nx] > 0:
                cnt += 1
    return cnt

# func 영양제 자리 빼고 자란것 가지치기
def check_grow(graph, medicine):
    for i in range(n):
        for j in range(n):
            if medicine[i][j] != 1 and graph[i][j] >= 2:
                graph[i][j] -= 2
                medicine[i][j] = 1
            elif medicine[i][j] == 1:
                medicine[i][j] = 0 

# m년 동안 반복
for year in range(m):
    d, p = map(int, input().split())
    next_medicine = [[0]*n for _ in range(n)]
    # 이동방향 결정

    # 1. 영양제 이동
    for i in range(n):
        for j in range(n):
            if medicine[i][j] == 1:
                y,x = move(i,j,p,d)
                next_medicine[y][x] = 1
    medicine = next_medicine
    # 2. 영양제 위치 높이 1 증가
    for i in range(n):
        for j in range(n):
            if medicine[i][j] == 1:
                graph[i][j] += 1
    for i in range(n):
        for j in range(n):
            if medicine[i][j] == 1:    
                graph[i][j] += search(i,j)
    # 3. 먼저 영양제 기존에 것 없애고, 자라난것 영양제 처리 
    check_grow(graph,medicine)
answer = 0
for row in graph:
    answer += sum(row)
print(answer)