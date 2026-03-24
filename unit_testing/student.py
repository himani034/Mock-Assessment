# student_functions.py

def calculate_average(scores):
    """Calculate average of a list of scores"""
    return sum(scores) / len(scores)

def is_passed(score, pass_mark=40):
    """Return True if score >= pass_mark"""
    return score >= pass_mark