from constraint import *

# STEP 1: Define subject period counts
subject_periods = {
    "Math": 4,
    "Science": 3,
    "English": 3,
    "History": 2,
    "Computer": 1,
    "Mechanics": 2,
    "Python": 4,
    "Drawing": 1,
    "Material sci": 3,
    "Biology": 2,
}

# STEP 2: Assign teachers to each subject
teachers = {
    "Math": "Mr. A",
    "Science": "Ms. B",
    "English": "Mr. C",
    "History": "Ms. D",
    "Computer": "Mr. E",
    "Mechanics": "Mr. F",
    "Python": "Mr. G",
    "Drawing": "Mr. H",
    "Material sci": "Mr. I",   # ✅ Fixed
    "Biology": "Mr. J",
}

# STEP 3: Time slots
period_times = {
    1: "09:00–10:00",
    2: "10:00–11:00",
    3: "11:00–12:00",
    4: "12:00–01:00",
    5: "01:00–02:00"
}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
slots = [f"{day[:3]}-{period}" for day in days for period in period_times.keys()]

# STEP 4: Expand subject instances (e.g., Python_1, Python_2)
expanded_subjects = []
subject_lookup = {}
for subject, count in subject_periods.items():
    for i in range(1, count + 1):
        var_name = f"{subject}_{i}"
        expanded_subjects.append(var_name)
        subject_lookup[var_name] = subject

# STEP 5: Create CSP
problem = Problem()

# Add all variables
for var in expanded_subjects:
    problem.addVariable(var, slots)

# No two subjects in the same slot
problem.addConstraint(AllDifferentConstraint(), expanded_subjects)

# No same teacher in two places
def no_teacher_conflict(*args):
    teacher_slots = {}
    for i, slot in enumerate(args):
        subject = subject_lookup[expanded_subjects[i]]
        teacher = teachers[subject]
        if teacher in teacher_slots and teacher_slots[teacher] == slot:
            return False
        teacher_slots[teacher] = slot
    return True

problem.addConstraint(no_teacher_conflict, expanded_subjects)

# No duplicate slots for the same subject (e.g., Python_1, Python_2 on same slot)
def no_same_subject_clash(*args):
    return len(set(args)) == len(args)

for subject in subject_periods:
    vars_for_subject = [v for v in expanded_subjects if subject_lookup[v] == subject]
    problem.addConstraint(no_same_subject_clash, vars_for_subject)

# STEP 6: Solve
solution = problem.getSolution()

# STEP 7: Display
if solution:
    print("\n" + "="*110)
    print(" " * 38 + "🏫 COLLEGE TIMETABLE")
    print("="*110)

    header = ["Period", "Time"] + days
    print("{:<8} {:<13} {:<18} {:<18} {:<18} {:<18} {:<18}".format(*header))
    print("-" * 110)

    for period in period_times:
        row = [f"{period}", period_times[period]]
        for day in days:
            slot = f"{day[:3]}-{period}"
            found = False
            for var, sl in solution.items():
                if sl == slot:
                    subject = subject_lookup[var]
                    teacher = teachers[subject]
                    row.append(f"{subject} ({teacher})")
                    found = True
                    break
            if not found:
                row.append("Free")
        print("{:<8} {:<13} {:<18} {:<18} {:<18} {:<18} {:<18}".format(*row))
    print("="*110)
else:
    print("❌ No valid timetable found. Please check constraints.")
