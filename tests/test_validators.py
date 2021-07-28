from app.core.util import get_type

field_type = 1
field_name = 0


def test_validate_empty_field():
    param = ("field_1", "")
    result = get_type(param)
    assert result[field_type] is None
    assert result[field_name] == param[0]


def test_validate_email():
    param = ("field_1", "ivanov@gmail.com")
    result = get_type(param)
    assert result[field_type] == "email"
    assert result[field_name] == param[0]


def test_validate_bad_email():
    param = ("field_1", "@ivanov@gmail.com")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_phone():
    param = ("field_1", "+7 123 456 77 88")
    result = get_type(param)
    assert result[field_type] == "phone"
    assert result[field_name] == param[0]


def test_validate_bad_phone1():
    param = ("field_1", "7 123 456 77 88")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_bad_phone2():
    param = ("field_1", "+8 123 456 77 88")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_bad_phone3():
    param = ("field_1", "+7 q23 456 77 88")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_date1():
    param = ("field_1", "2021-01-01")
    result = get_type(param)
    assert result[field_type] == "date"
    assert result[field_name] == param[0]


def test_validate_date2():
    param = ("field_1", "01.01.2021")
    result = get_type(param)
    assert result[field_type] == "date"
    assert result[field_name] == param[0]


def test_validate_bad_date1():
    param = ("field_1", "01.13.2021")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_bad_date3():
    param = ("field_1", "01.13.21")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_date4():
    param = ("field_1", "21-01-01")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]


def test_validate_bad_date5():
    param = ("field_1", "2021-01-32")
    result = get_type(param)
    assert result[field_type] == "text"
    assert result[field_name] == param[0]
