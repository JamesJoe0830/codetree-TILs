# 총 K 턴을 진행한다.
# [1. 유물 회전 = 탐사 진행]
# 3x3 격자를 선택해서 회전이 가능하다. 90도 180도 270도 회전이 가능하다.
# 1) 유물의 획득 가치를 극대화하고, 만일 그 방법이 여러가지일 경우 회전 각도가 작은 것을 선택
# [2. 유물 획득 = 3개 이상인 경우 유물이 되고 사라진다.]
# 1) 유물이 사라지고 조각이 빈 상태일때
# 2) 유적 벽면에 써있는 숫자는 1. 열 번호 작은 순 2. 열번호가 같다면 행 번호가 큰 순으로 조각이 생긴다.

# def 함수------------------------------------------------------
# 1. 중심좌표를 기준으로 회전하는 함수 
#   a. 그 함수에 따른 현재 획득가치가 가장 작은 것의 (회전각도, 중심좌표의 열과 행이 가장 작은 것을 저장)
# 2. 그 중심좌표를 기준으로 회전한 새로운 그래프를 기반으로 dfs 탐색해서 총 유물의 합을 구한다.
# 3.
from collections import deque
import sys
import copy

input = sys.stdin.readline
K, M = map(int,input().split())
# K: 총 턴 , M: 추가될 유물의 배열수
graph = [list(map(int,input().split())) for _ in range(5)]
update_origin_graph = copy.deepcopy(graph)
nx_update_origin_graph = copy.deepcopy(update_origin_graph)
add_blockQ = deque(map(int,input().split()))
rotate_deg = [0,90,180,270]
center_point = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
# add_block : 빈 공간을 채워줄 블럭 리스트
dx = [0,0,-1,1]
dy = [-1,1,0,0]

def bfs(y,x,cnt,edit_graph,visited):
    # cnt : block 개수 세는 것
    block_value=edit_graph[y][x]
    visited.add((y,x))
    Q = deque()
    Q.append((y,x))
    while Q : 
        cy,cx = Q.popleft()
        for i in range(4):
            nx= cx + dx[i]
            ny= cy + dy[i]
            if 0<=nx<5 and 0<=ny<5 and edit_graph[ny][nx] == block_value and (ny,nx) not in visited:
                visited.add((ny,nx))
                Q.append((ny,nx))
                cnt+=1
    if cnt >= 3:
        for y,x in visited:
            edit_graph[y][x] = 0
        return cnt
    else : 
        return 0
            
def rotate (deg,y,x, edit_graph, graph):
    if deg == 90:
        edit_graph[y-1][x+1] = graph[y-1][x-1]
        edit_graph[y][x+1] = graph[y-1][x]
        edit_graph[y+1][x+1] = graph[y-1][x+1]
        
        edit_graph[y+1][x+1] = graph[y-1][x+1]
        edit_graph[y+1][x] = graph[y][x+1]
        edit_graph[y+1][x-1] = graph[y+1][x+1]
        
        edit_graph[y+1][x-1] = graph[y+1][x+1]
        edit_graph[y][x-1] = graph[y+1][x]
        edit_graph[y-1][x-1] = graph[y+1][x-1]

        edit_graph[y-1][x-1] = graph[y+1][x-1]
        edit_graph[y-1][x] = graph[y][x-1]
        edit_graph[y-1][x+1] = graph[y-1][x-1]
    elif deg == 180:
        edit_graph[y+1][x+1] = graph[y-1][x-1]
        edit_graph[y+1][x] = graph[y-1][x]
        edit_graph[y+1][x-1] = graph[y-1][x+1]
        
        edit_graph[y+1][x-1] = graph[y-1][x+1]
        edit_graph[y][x-1] = graph[y][x+1]
        edit_graph[y-1][x-1] = graph[y+1][x+1]
        
        edit_graph[y-1][x-1] = graph[y+1][x+1]
        edit_graph[y-1][x] = graph[y+1][x]
        edit_graph[y-1][x+1] = graph[y+1][x-1]

        edit_graph[y-1][x+1] = graph[y+1][x-1]
        edit_graph[y][x+1] = graph[y][x-1]
        edit_graph[y+1][x+1] = graph[y-1][x-1]
    elif deg == 270:
        edit_graph[y+1][x-1] = graph[y-1][x-1]
        edit_graph[y][x-1] = graph[y-1][x]
        edit_graph[y-1][x-1] = graph[y-1][x+1]
        
        edit_graph[y-1][x-1] = graph[y-1][x+1]
        edit_graph[y-1][x] = graph[y][x+1]
        edit_graph[y-1][x+1] = graph[y+1][x+1]
        
        edit_graph[y-1][x+1] = graph[y+1][x+1]
        edit_graph[y][x+1] = graph[y+1][x]
        edit_graph[y+1][x+1] = graph[y+1][x-1]

        edit_graph[y+1][x+1] = graph[y+1][x-1]
        edit_graph[y+1][x] = graph[y][x-1]
        edit_graph[y+1][x-1] = graph[y-1][x-1]
    return edit_graph
answer = []
for _ in range(K):
    step_answer = 0
    update_origin_graph = copy.deepcopy(nx_update_origin_graph)
    for deg in rotate_deg:
        for center_y, center_x in center_point:
            new_graph = copy.deepcopy(update_origin_graph)
            edit_graph = copy.deepcopy(update_origin_graph)
            if deg != 0:
                edit_graph = rotate(deg, center_y, center_x, edit_graph, update_origin_graph)
                new_graph = copy.deepcopy(edit_graph)
            cr_answer = 0
            
            for i in range(5):
                for j in range(5):
                    visited = set()
                    if edit_graph[i][j] != 0 :
                        cnt = 1
                        cr_answer += bfs(i,j, cnt,edit_graph,visited)
            
            if step_answer < cr_answer:
                nx_update_origin_graph = copy.deepcopy(edit_graph)
                step_answer = cr_answer
            # 여기서는 이제 빈 공간을 채워주는 형식으로 진행한다. 
            
            # 빈 배열의 여부를 판단하고 넣어준다.
            # add_blockQ에서 지속적으로 뽑아서 넣어준다.

    # 이구간을 계속 반복할건데 반복할 수 있는 조건은 하나도 
    Flag = True
    while Flag :
        Flag = False
        for x in range(5):
            for y in range(4, -1, -1):
                if nx_update_origin_graph[y][x] == 0:
                    if add_blockQ :
                        pop_element = add_blockQ.popleft()
                        nx_update_origin_graph[y][x] = pop_element
        # 잘 나옴 
        for i in range(5):
            for j in range(5):
                visited = set()
                if nx_update_origin_graph[i][j] != 0:
                    cnt = 1
                    cnt = bfs(i,j,cnt,nx_update_origin_graph,visited)
                    if cnt != 0 :
                        Flag = True
                        step_answer += cnt
        


    if step_answer != 0 :
        answer.append(str(step_answer))
print(' '.join(answer))