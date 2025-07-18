from constraint import *
import tkinter as tk
from tkinter import ttk, messagebox

# --- SUBJECTS & TEACHERS ---
subject_periods = {
    "Math": 4, "Science": 3, "English": 3, "History": 2, "Computer": 1,
    "Mechanics": 2, "Python": 4, "Drawing": 1, "Material sci": 3, "Biology": 2, "Computer Lab": 2,
    "Sports": 2, "Communication": 2, "GK": 1, "Library": 2
}

teachers = {
    "Math": "Mr. A", "Science": "Ms. B", "English": "Mr. C", "History": "Mr. D",
    "Computer": "Mr. E", "Mechanics": "Mr. F", "Python": "Mr. G",
    "Drawing": "Mr. H", "Material sci": "Mr. I", "Biology": "Mr. J",
    "Computer Lab": "Mr.E", "Sports": "Mr. H", "Communication": "Mr. C", "GK": "Mr. K", "Library": "Mr.L"
}


# --- Period Times & Break ---
period_times = {
    1: "08:00-09:00",
    2: "09:00–10:00",
    3: "10:00–11:00",
    4: "11:00–12:00",
    5: "12:00–01:00",
    6: "01:00–02:00",
    7: "02:00–03:00", 
    8: "03:00-04:00"
}
break_after = 5
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
slots = [f"{day[:3]}-{period}" for day in days for period in period_times if period != break_after + 1]

# --- Generate Timetable ---
def generate_timetable():
    expanded_subjects = []
    subject_lookup = {}
    for subject, count in subject_periods.items():
        for i in range(1, count + 1):
            var_name = f"{subject}_{i}"
            expanded_subjects.append(var_name)
            subject_lookup[var_name] = subject

    problem = Problem()
    for var in expanded_subjects:
        problem.addVariable(var, slots)
    problem.addConstraint(AllDifferentConstraint(), expanded_subjects)

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

    def no_same_subject_clash(*args):
        return len(set(args)) == len(args)

    for subject in subject_periods:
        vars_for_subject = [v for v in expanded_subjects if subject_lookup[v] == subject]
        problem.addConstraint(no_same_subject_clash, vars_for_subject)

    solution = problem.getSolution()
    if not solution:
        messagebox.showerror("Error", "No valid timetable found.")
        return

    # --- Build Timetable Dictionary with Breaks ---
    timetable = {}
    for day in days:
        for period in period_times:
            key = f"{day[:3]}-{period}"
            if period == break_after + 1:
                timetable[key] = "Break"
            else:
                timetable[key] = "Free"

    # Assign real subjects
    for var, sl in solution.items():
        subject = subject_lookup[var]
        teacher = teachers[subject]
        timetable[sl] = f"{subject} ({teacher})"

    # --- GUI Output ---
    for widget in frame_output.winfo_children():
        widget.destroy()

    headers = ["Period", "Time"] + days
    for col, text in enumerate(headers):
        label = tk.Label(frame_output, text=text, borderwidth=1, relief="solid", bg="#dee2e6",
                         font=('Segoe UI', 10, 'bold'), padx=5, pady=5)
        label.grid(row=0, column=col, sticky="nsew")

    for row_idx, period in enumerate(period_times, start=1):
        tk.Label(frame_output, text=str(period), borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_idx, column=0, sticky="nsew")
        tk.Label(frame_output, text=period_times[period], borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_idx, column=1, sticky="nsew")

        for col_idx, day in enumerate(days, start=2):
            slot = f"{day[:3]}-{period}"
            text = timetable.get(slot, "Free")
            
            bg = '#fce5cd'

            tk.Label(frame_output, text=text, borderwidth=1, relief="solid", padx=5, pady=5, bg=bg, wraplength=120).grid(row=row_idx, column=col_idx, sticky="nsew")
            lbl_summary.config(text=f"Timetable Generated | Break After Period {break_after}")

# --- GUI SETUP ---
root = tk.Tk()
root.title("College Timetable Generator")
root.geometry("1050x600")

frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

btn_generate = ttk.Button(frame_top, text="Generate Timetable", command=generate_timetable)
btn_generate.pack(side="left", padx=10)

lbl_summary = ttk.Label(frame_top, text="Click 'Generate Timetable' to begin", font=('Segoe UI', 10))
lbl_summary.pack(side="left", padx=20)

frame_canvas = tk.Canvas(root)
frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=frame_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

frame_canvas.configure(yscrollcommand=scrollbar.set)
frame_canvas.bind("<Configure>", lambda e: frame_canvas.configure(scrollregion=frame_canvas.bbox("all")))

frame_output = ttk.Frame(frame_canvas)
frame_canvas.create_window((0, 0), window=frame_output, anchor="nw")

root.mainloop()

