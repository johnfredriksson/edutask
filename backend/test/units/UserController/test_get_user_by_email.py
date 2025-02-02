import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

# Fixture setup
@pytest.fixture
def sut(response):
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = response
    mockedsut = UserController(mockedDAO)
    return mockedsut

# Test with valid email
@pytest.mark.unit
@pytest.mark.parametrize(
    'email, response, expected',
    [
        ('local-part@domain.host', [], None),
        ('local-part@domain.host', ['local-part@domain.host'], 'local-part@domain.host'),
        ('local-part@domain.host', ['local-part@domain.host', 'local-part-second@domain.host'], 'local-part@domain.host')
    ]
)
def test_getUserByEmail_emailValid(sut, email, expected):
    result = sut.get_user_by_email(email)
    assert result == expected

# Test with invalid email
@pytest.mark.unit
@pytest.mark.parametrize(
    'email, response',
    [
        ('@domain.host', []),
        ('local-partdomain.host', []),
        ('local-part@.host', []),
        ('local-part@domainhost', []),
        ('local-part@.', [])
    ]
)
def test_getUserByEmail_emailInvalid(sut, email):
    with pytest.raises(ValueError):
        sut.get_user_by_email(email)

# Test with database failure
@pytest.mark.unit
@pytest.mark.parametrize(
    'email, response',
    [
        ('local-part@domain.host', Exception)
    ]
)
def test_getUserByEmail_databaseFailure(sut, email):
    with pytest.raises(Exception):
        sut.get_user_by_email(email)
