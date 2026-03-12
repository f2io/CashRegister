from cashregister.util.division import Division


def test_valid_division_using_float():
    result = Division.is_divided_by(3.33, 3)
    assert result is True

    result = Division.is_divided_by(9.99, 3)
    assert result is True

    result = Division.is_divided_by(0.33, 3)
    assert result is True


def test_valid_division_using_int():
    result = Division.is_divided_by(3, 3)
    assert result is True

    result = Division.is_divided_by(9, 3)
    assert result is True


def test_invalid_division():
    result = Division.is_divided_by(2.12, 3)
    assert result is False

    result = Division.is_divided_by(3.34, 3)
    assert result is False

    result = Division.is_divided_by(1.97, 3)
    assert result is False

    result = Division.is_divided_by(0.11, 3)
    assert result is False

    result = Division.is_divided_by(10, 3)
    assert result is False
