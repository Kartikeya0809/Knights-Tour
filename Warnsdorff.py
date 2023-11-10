dx = [1, 2, 2, 1, -1, -2, -2, -1]
dy = [2, 1, -1, -2, -2, -1, 1, 2]
count = 1
paths = []
visited = []
n, m = 0, 0

def solve(x, y, path):
    global dx, dy, visited, count, paths, m, n
    if count >= m * n:
        paths = path.copy()
        return True
    degrees = []
    for i in range(0, 8):
        deg = 0
        r = x + dx[i]
        c = y + dy[i]
        if 0 <= r < n and 0 <= c < m and not visited[r][c]:
            for j in range(0, 8):
                k = r + dx[j]
                l = c + dy[j]
                if 0 <= k < n and 0 <= l < m and not visited[k][l]:
                    deg += 1
            degrees.append((i, deg))
    degrees = sorted(degrees, key=lambda x:x[1])
    # print(x, y, degrees)
    for i in degrees:
        r = x + dx[i[0]]
        c = y + dy[i[0]]
        visited[r][c] = 1
        count += 1
        path.append((r, c))
        if solve(r, c, path):
            return True
        count -= 1
        visited[r][c] = 0
        path.pop()
    if len(path) > len(paths):
        paths = path.copy()
    return False

def warnsdorff_path(x, y):
    global n, m, visited, paths
    n = x; m = y
    visited = [[0 for i in range(0, m)] for j in range(0, n)]
    visited[0][0] = 1
    if not solve(0, 0, [(0, 0)]):
        print("No Solution")
    return paths