from pathlib import Path
import json

def get_problems(p_problems, year, angle):
    p_data = Path(p_problems) / "moon_{}_{}.json".format(year, angle)
    with open(p_data, "r") as file:
        probs = json.load(file)
    return probs


def filter_problems(probs, repsge, grade_names, minlen=1, maxlen=15):
    probs_new = []
    grade_names = set(grade_names)
    probs_grade_names = set([])
    for p in probs:
        if p["repeats"] < repsge:
            continue
        if p["grade"] not in grade_names:
            continue
        if len(p["moves"]) < minlen:
            continue
        if len(p["moves"]) > maxlen:
            continue
        probs_grade_names.add(p["grade"])
        probs_new.append(p)
    assert grade_names == probs_grade_names, "Grades do not match! {}".format(grade_names - probs_grade_names)
    return probs_new



def filter_problems_ge(probs, grade_repge, grade_names, minlen=1, maxlen=15):
    probs_new = []
    grade_names = set(grade_names)
    probs_grade_names = set([])
    for p in probs:
        if p["grade"] not in grade_names:
            continue
        if p["repeats"] < grade_repge[p["grade"]]:
            continue
        if len(p["moves"]) < minlen:
            continue
        if len(p["moves"]) > maxlen:
            continue
        probs_grade_names.add(p["grade"])
        probs_new.append(p)
    assert grade_names == probs_grade_names, "Grades do not match! {}".format(grade_names - probs_grade_names)
    return probs_new