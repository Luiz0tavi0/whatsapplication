import pytest

from app.services.status_transition import is_valid_transition


@pytest.mark.parametrize(
    ('current', 'new', 'expected'),
    [
        ('pending', 'sent', True),
        ('sent', 'received', True),
        ('received', 'read', True),
        ('read', 'received', False),
        ('received', 'failed', False),
        ('pending', 'failed', True),
        ('failed', 'sent', False),
        ('failed', 'received', False),
        ('read', 'failed', False),
    ],
)
def test_is_valid_transition(current, new, expected):
    assert is_valid_transition(current, new) == expected
