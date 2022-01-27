## CSE4007 : Artificial Intelligence
> 과제 1 : N-Queens Problem을 BFS, Hill Climbing, Cosstraint Satisfaction Problems 알고리즘으로 해결하기

* N*N 크기의 체스판에 N개의 퀸들이 서로 공격하지 않는 배치의 경우의 수를 구하는 문제
* 임의의 N에 대해 알고리즘별 solution 출력
* `input.txt`를 참조해 얻은 정보를 기반으로 각 알고리즘 수행
  - 파일 내용은 행마다 `N *\n`로 구성 (*에는 알고리즘 이름 bfs, hc, csp)
* 각 열에 대해 퀸의 행 위치를 출력
  - 출력 파일 예시 : `N_*_output.txt` (*에는 알고리즘 이름 bfs, hc, csp)
  - 정답이 존재하지 않을 시 `no solution` 출력
<br>

> 과제 2 : Q-Learning 기법을 통해 목표 지점까지 이동하기

* 5*5 맵에 대한 정보가 담긴 `input.txt`를 참조해 알고리즘 수행
  - 시작지점(S), 목표지점(G), 보너스(T), 폭탄(B), 기타(P)로 구성
  - 출발지점에서 목표지점까지 도달해야 하며 폭탄을 밟으면 출발지점에서 다시 시작
  - 폭탄 reward : `-100`, 목표지점 reward : `100`, 보너스 reward : `1`, 𝛾 : `0.9`
* 출력 내용은 `output.txt`에 저장
  - 1행은 시작지점부터 목표지점까지의 최적 경로 (시작지점은 0, 목표지점은 24 고정)
  - 2행은 시작지점의 `Q(s,a)` 최댓값

각 괴제 코드에 대한 설명은 `.docx`에 있습니다.
