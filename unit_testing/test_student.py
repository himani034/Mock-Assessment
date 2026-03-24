# test_student_functions.py

import pytest
from student import calculate_average, is_passed

# Fixture for sample scores
@pytest.fixture
def sample_scores():
    return [70, 80, 90]

# Test calculate_average function
def test_calculate_average(sample_scores):
    assert calculate_average(sample_scores) == 80

# Test is_passed function
def test_is_passed():
    assert is_passed(50) == True
    assert is_passed(30) == False