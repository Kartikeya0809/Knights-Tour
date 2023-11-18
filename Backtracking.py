dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
visited = []
count = 1
paths = []

def solve(x, y, path):
    global count, visited, n, m, paths
    if count >= n * m:
        paths = path
        return True
    for i in range(0, 8):
        r = x + dx[i]
        c = y + dy[i]
        if 0 <= r < n and 0 <= c < m and not visited[r][c]:
            visited[r][c] = 1
            path.append((r, c))
            count += 1
            solve(r, c, path)
            if count >= n * m:
                return True
            path.pop()
            visited[r][c] = 0
            count -= 1
    if len(path) > len(paths):
        paths = path.copy()
    return False

def get_path(x, y):
    global paths, visited, n, m
    n = x
    m = y
    visited = [[0 for i in range(0, y)] for j in range(0, x)]
    visited[0][0] = 1
    print("Solving")
    if not solve(0, 0, [(0, 0)]):
        print("No Solution")
    print("Returning")
    return paths

# board = Tk()
# board.geometry("700x550")
# board.title("Knight's Tour")