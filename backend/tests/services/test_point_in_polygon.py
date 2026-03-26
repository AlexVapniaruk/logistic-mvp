from app.services.geo.point_in_polygon import is_point_in_polygon

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]
TRIANGLE = [[0, 0], [100, 0], [50, 100]]
CONCAVE = [[0, 0], [100, 0], [100, 40], [60, 40], [60, 60], [100, 60], [100, 100], [0, 100]]


def test_point_inside_square() -> None:
    assert is_point_in_polygon(50, 50, SQUARE) is True


def test_point_outside_square() -> None:
    assert is_point_in_polygon(150, 50, SQUARE) is False


def test_point_outside_square_negative() -> None:
    assert is_point_in_polygon(-10, 50, SQUARE) is False


def test_point_inside_triangle() -> None:
    assert is_point_in_polygon(50, 10, TRIANGLE) is True


def test_point_outside_triangle() -> None:
    assert is_point_in_polygon(5, 90, TRIANGLE) is False


def test_point_inside_concave_polygon() -> None:
    # Left half — inside
    assert is_point_in_polygon(30, 50, CONCAVE) is True


def test_point_in_notch_of_concave_polygon() -> None:
    # The notch cut-out region — outside
    assert is_point_in_polygon(80, 50, CONCAVE) is False


def test_point_at_origin_corner() -> None:
    # Corners are edge cases; just verify no crash
    result = is_point_in_polygon(0, 0, SQUARE)
    assert isinstance(result, bool)


def test_single_point_polygon_is_outside() -> None:
    assert is_point_in_polygon(5, 5, [[0, 0]]) is False


def test_empty_polygon_is_outside() -> None:
    assert is_point_in_polygon(5, 5, []) is False
