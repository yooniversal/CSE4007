import random


# 범위 벗어났는지 체크 (out of bound)
def OOB(x, y):
    return x < 0 or x >= 5 or y < 0 or y >= 5


# state 계산
def state(x, y):
    return x * 5 + y


# 방향 (북, 동, 남, 서)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 초기화
q = [[0.0 for i in range(4)] for j in range(25)]
reward = [[0 for i in range(5)] for j in range(5)]
bomb = [[False for i in range(5)] for j in range(5)]

# 좌표
x, y = 0, 0
start_x, start_y = 0, 0

# input.txt에 담긴 정보를 참고해 reward, bomb 반영
input = open('input.txt', 'r')

while True:

    # 처리할 내용이 있을 때까지 한 줄씩 처리하며 진행
    line = input.readline()
    if not line:
        break

    for y in range(0, 5):
        if line[y] == 'S':
            start_x, start_y = x, y
        elif line[y] == 'G':
            reward[x][y] = 100
        elif line[y] == 'T':
            reward[x][y] = 1
        elif line[y] == 'B':
            reward[x][y] = -100
            bomb[x][y] = True

    x = x + 1

input.close()

# Q-Learning
x, y = start_x, start_y

cnt = 0
while cnt < 500000:
    cnt = cnt + 1

    # 현재 위치가 폭탄 -> 시작 위치로 이동
    if bomb[x][y]:
        x, y = start_x, start_y

    # 랜덤 방향 설정
    a = random.randint(0, 3)

    # 다음 위치
    nx, ny = x + dx[a], y + dy[a]

    # 다음 위치가 정해진 범위를 벗어나지 않도록 처리
    while OOB(nx, ny):
        a = random.randint(0, 3)
        nx, ny = x + dx[a], y + dy[a]

    # 다음 state s'의 Q(s', a') 최댓값 구하기
    max_next_q = -987654321.0
    for d in range(0, 4):
        if max_next_q < q[state(nx, ny)][d]:
            max_next_q = q[state(nx, ny)][d]

    # Q(s, a) update 여부에 따른 케이스 분류
    q[state(x, y)][a] = reward[x][y] + 0.9 * max_next_q

    # 다음 state로 이동
    x, y = nx, ny

# output.txt 작성
f = open('output.txt', 'w')

start_q = -987654321.0
for a in range(0, 4):
    if start_q < q[state(start_x, start_y)][a]:
        start_q = q[state(start_x, start_y)][a]

x, y = start_x, start_y
while True:

    # 위치 작성
    f.write(str(state(x, y)) + ' ')

    # Goal state 도달 -> Q
    if reward[x][y] == 100:
        f.write('\n' + str(start_q))
        break
    
    # 가장 큰 Q(s, a) 탐색 및 state s'로 이동
    max_next_q = -987654321.0
    next_a = -1
    for a in range(0, 4):
        nx, ny = x + dx[a], y + dy[a]
        if OOB(nx, ny):
            continue
        if max_next_q < q[state(x, y)][a]:
            max_next_q = q[state(x, y)][a]
            next_a = a

    x, y = x + dx[next_a], y + dy[next_a]

f.close()