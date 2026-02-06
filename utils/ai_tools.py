def generate_study_plan(subjects, hours):
    weight = {
        "Math": 1.3,
        "Physics": 1.2,
        "CS": 1.1,
        "Chemistry": 1.4
    }

    total = sum(weight.get(s, 1) for s in subjects)
    plan = {}

    for sub in subjects:
        plan[sub] = round((weight.get(sub, 1) / total) * hours, 2)

    return plan
