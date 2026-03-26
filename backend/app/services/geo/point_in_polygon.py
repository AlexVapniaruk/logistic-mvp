def is_point_in_polygon(x: float, y: float, points: list[list[float]]) -> bool:
    """Ray casting algorithm. points is a list of [x, y] vertices."""
    n = len(points)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = points[i][0], points[i][1]
        xj, yj = points[j][0], points[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside
