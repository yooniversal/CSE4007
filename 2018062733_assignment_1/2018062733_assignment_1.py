import random
from collections import deque


# c번 열에 퀸이 r행에 위치한다고 가정했을 때 (현재 퀸)
# c번 이전 열에 속힌 퀸들이 현재 퀸을 공격하는지 체크
def check(col, c, r):
    # c보다 작은 열들에 대해 조건을 만족하는지 탐색
    for i in range(c):

        # c보다 작은 열에 속해있는 퀸이 현재 퀸을 공격한다면 False 반환
        # 열의 차이값(c-i)을 가지고 판단할 수 있음
        if col[i] == r + (c - i) or col[i] == r - (c - i) or col[i] == r:
            return False

    return True  # 모든 퀸이 서로 대각선으로 공격하지 않는 경우


# c번 열 퀸이 공격받는 횟수 반환
# mode == True  : c보다 큰 열에 있는 퀸에서 탐색
# mode == False : c보다 작은 열에 있는 퀸에서 탐색
def getH(col, n, c, mode):
    ret = 0

    if mode:
        for i in range(c+1, n):

            # 가로 또는 대각선으로 겹친다면 카운트
            if col[i] == col[c] + (i - c) or col[i] == col[c] - (i - c) or col[i] == col[c]:
                ret += 1
    else:
        for i in range(c):

            # 가로 또는 대각선으로 겹친다면 카운트
            if col[i] == col[c] + (c - i) or col[i] == col[c] - (c - i) or col[i] == col[c]:
                ret += 1

    return ret


def outOfBound(r, c, n):
    return r<0 or r>=n or c<0 or c>=n


def updateRemainCnt(selected, remainCnt, reducedCnt, r, c, n):
    dr = [-1, -1, 1, 1]
    dc = [-1, 1, -1, 1]

    for nextCol in range(n):
        # 열이 같은 경우 예외 처리
        if nextCol == c:
            remainCnt[c] -= 1
            reducedCnt[c] += 1
            continue

        dist = abs(c - nextCol)
        for dir in range(4):
            nr = r + dr[dir] * dist # 다음 행
            nc = c * dc[dir] * dist # 다음 열

            if outOfBound(nr, nc, n): continue  # 범위 밖으로 나가는 경우 제외
            if selected[nc]: continue  # 이미 퀸이 위치한 열은 제외
            remainCnt[nc] -= 1
            reducedCnt[nc] += 1


def bfs(n):
    q = deque()
    q.append([0, [-1 for i in range(n)]]) # 첫 번째 열 삽입

    # 큐에 값이 다 떨어질 때까지 진행
    while q:
        cur = q.popleft()
        columnNumber = cur[0]   # 현재 colmun 번호
        states = cur[1]         # 현재 각 퀸의 row 정보

        # 마지막 열까지 처리를 완료했다면 답을 찾은 상태이므로 종료
        if columnNumber >= n:
            return states

        # cur번 열에서 퀸을 놓을 수 있는 행 테스트
        # 열은 이미 search space에서 제외됐으므로 행과 대각선만 체크
        for r in range(n):

            # 놓을 수 있는 행을 찾았다면 위치 설정 및 큐 삽입
            if check(states, columnNumber, r):
                nextStates = []
                for element in states:
                    nextStates.append(element)

                nextStates[columnNumber] = r
                q.append([columnNumber + 1, nextStates])

    return [-1 for i in range(n)]


def hc(col, h, n, curH):

    # 답을 찾았을 때 종료
    if curH == 0:
        return True

    # 현재 h값(curH)보다 더 작은 h값이 있는지 탐색
    # 존재한다면, 해당 좌표와 최솟값 얻기
    r = -1
    c = -1
    minn = 987654321
    for i in range(n):
        for j in range(n):
            if h[i][j] < curH and h[i][j] < minn:
                r = i
                c = j
                minn = h[i][j]

    # curH보다 더 작은 h값이 존재한다면 그 중 최솟값으로 이동
    if minn != 987654321:
        col[c] = r  # 퀸 위치 변경

        # 다음 탐색에서 쓰일 h 재설정
        for i in range(n):
            origin = col[i]
            before = getH(col, n, i, True)
            for j in range(n):
                col[i] = j
                after = getH(col, n, i, False) + getH(col, n, i, True)
                h[j][i] = h[j][i] - before + after
            col[i] = origin

        # 값 반영 후 탐색(greedy search)
        return hc(col, h, n, minn)

    # stuck에 걸린 상태
    return False


def csp(col, selected, remainCnt, n, time):

    # 모든 열에 퀸을 놓았으므로 정답 탐색 성공
    if time >= n:
        return True

    next = []   # 선택될 퀸 후보 정보

    # 위치가 정해지지 않은 퀸의 [열, legal value 개수]값 담기
    for i in range(0, n):
        if selected[i]: continue    # 위치가 정해진 퀸은 무시
        next.append([i, remainCnt[i]])

    # legal value 개수가 적은 순으로 정렬
    next.sort(key = lambda x:x[1])

    # value(row)를 선택하는 과정
    # 다른 퀸들이 위치할 수 있는 구역에 영향을 최소한으로 하는 value 선택
    for nextInfo in next:
        for r1, r2 in zip(range(0, n), range(n-1, -1, -1)):
            if r1 > r2: break

            selectedCol = nextInfo[0]
            reducedCnt = [0 for i in range(n)]  # 탐색 실패 시 remainCnt 복구용

            # r1부터 탐색
            row = r1

            flag = True  # 탐색 가능한 케이스 있는지 확인
            # 모든 열에 위치한 퀸들과 충돌하는지 조건 확인
            for c in range(n):

                # 위치하지 않은 퀸들 예외처리
                if selected[c] == False: continue

                # 가로, 대각선으로 충돌하는 퀸이 있는지 체크
                if col[c] == row + (selectedCol - c) or col[c] == row - (selectedCol - c) \
                        or col[c] == row:
                    flag = False
                    break

            # 탐색 가능한 케이스 발견 -> 진행
            if flag:

                # 다른 열의 legal value 사용에 영향을 주므로 remainCnt 업데이트
                updateRemainCnt(selected, remainCnt, reducedCnt, row, selectedCol, n)

                col[selectedCol] = row
                selected[selectedCol] = True

                if csp(col, selected, remainCnt, n, time + 1): return True

                # 탐색 실패했으므로 복구
                selected[selectedCol] = False
                for i in range(n):
                    remainCnt[i] += reducedCnt[i]

            # r1에서 정답을 찾지 못했다면 r2에서 탐색 진행
            row = r2

            flag = True  # 탐색 가능한 케이스 있는지 확인
            # 모든 열에 위치한 퀸들과 충돌하는지 조건 확인
            for c in range(n):

                # 위치하지 않은 퀸들 예외처리
                if selected[c] == False: continue

                # 가로, 대각선으로 충돌하는 퀸이 있는지 체크
                if col[c] == row + (selectedCol - c) or col[c] == row - (selectedCol - c) \
                        or col[c] == row:
                    flag = False
                    break

            # 탐색 가능한 케이스 발견 -> 진행
            if flag:

                # 다른 열의 legal value 사용에 영향을 주므로 remainCnt 업데이트
                updateRemainCnt(selected, remainCnt, reducedCnt, row, selectedCol, n)

                col[selectedCol] = row
                selected[selectedCol] = True

                if csp(col, selected, remainCnt, n, time + 1): return True

                # 탐색 실패했으므로 복구
                selected[selectedCol] = False
                for i in range(n):
                    remainCnt[i] += reducedCnt[i]

    return False

nList = []  # 입력받을 N 목록
typeList = []  # 입력받을 Type 목록

# input 처리
input = open("input.txt", 'r')

while True:
    # 처리할 내용이 있을 때까지 한 줄씩 처리하며 진행
    line = input.readline()
    if not line:
        break

    # 한 줄에서 첫 번째 값은 N, 두 번째 값은 Type
    split = line.split()
    nList.append(split[0])
    typeList.append(split[1])

input.close()

# 각 N, Type에 따라 결과 반환
for n, type in zip(nList, typeList):
    print(n + " " + type)

    col = []  # col[i] = i열에 있는 퀸의 row값
    for i in range(int(n)):
        col.append(i)  # col 배열에 서로 다른 row에 위치하는 퀸 채우기

    outputName = n + "_" + type + "_output.txt"
    f = open(outputName, 'w')
    n = int(n)

    success = False  # 탐색 성공 여부

    # Type에 따라 케이스 분류
    if type == "bfs":
        col = bfs(n)
        if col[0] != -1:
            success = True
    elif type == "hc":

        # 최대 10000번 hill-climbing으로 탐색 진행
        h = [[0 for i in range(n)] for j in range(n)]
        for time in range(10001):

            for i in range(n):
                col[i] = i

            random.shuffle(col)

            currentH = 0
            for c in range(n):
                currentH += getH(col, int(n), c, True)

            # 탐색에서 쓰일 h 재설정
            for i in range(n):
                origin = col[i]
                before = getH(col, n, i, True)
                for j in range(n):
                    col[i] = j
                    after = getH(col, n, i, False) + getH(col, n, i, True)
                    h[j][i] = currentH - before + after
                col[i] = origin

            if hc(col, h, n, currentH):
                success = True
                break

    elif type == "csp":
        selected = [False for i in range(n)]
        remainCnt = [n for i in range(n)]  # 열 별로 남은 legal value 개수
        success = csp(col, selected, remainCnt, n, 0)

    # 탐색 성공 -> 결과값 출력
    if success:
        for ans in col:
            f.write(str(ans) + " ")
        f.write("\n")
    # 탐색 실패
    else:
        f.write("no solution\n")

    f.close()
