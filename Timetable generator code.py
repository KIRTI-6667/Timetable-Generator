from constraint import *
import tkinter as tk
from tkinter import ttk, messagebox

# --- GLOBAL VARIABLES ---
subject_teacher_map = {}
subject_periods = {}
days = []
period_times = {}
break_after = 5

# --- FUNCTION: Add Subject ---
def add_subject():
    subject = entry_subject.get().strip()
    teacher = entry_teacher.get().strip()
    periods = entry_periods.get().strip()

    if subject and teacher and periods.isdigit():
        subject_teacher_map[subject] = teacher
        subject_periods[subject] = int(periods)
        listbox_subjects.insert(tk.END, f"{subject} ({teacher}) - {periods} periods/week")
        entry_subject.set("")
        entry_teacher.set("")
        entry_periods.set("")
    else:
        messagebox.showwarning("Input Error", "Please enter valid subject, teacher, and period count.")

# --- FUNCTION: Add Timing to List ---
def add_timing():
    selected = timing_var.get()
    if selected and selected not in text_timings.get("1.0", tk.END):
        text_timings.insert(tk.END, selected + "\n")

# --- FUNCTION: Add Days and Period Timings ---
def add_days_periods():
    global days, period_times, break_after

    days_input = entry_days.get().strip()
    timing_input = text_timings.get("1.0", tk.END).strip().splitlines()

    if not days_input or not timing_input:
        messagebox.showwarning("Missing Data", "Please enter both days and period timings.")
        return

    days = [d.strip() for d in days_input.split(",") if d.strip()]
    period_times = {i + 1: t for i, t in enumerate(timing_input)}
    messagebox.showinfo("Success", "Days and timings added successfully!")

# --- FUNCTION: Generate Timetable ---
def generate_timetable():
    if not subject_teacher_map or not days or not period_times:
        messagebox.showwarning("Missing Data", "Please add subjects, teachers, days, and timings before generating timetable.")
        return

    expanded_subjects = []
    subject_lookup = {}
    for subject, count in subject_periods.items():
        for i in range(1, count + 1):
            var_name = f"{subject}_{i}"
            expanded_subjects.append(var_name)
            subject_lookup[var_name] = subject

    # CSP Problem Setup
    problem = Problem()
    slots = [f"{day[:3]}-{p}" for day in days for p in period_times.keys() if p != break_after + 1]
    for var in expanded_subjects:
        problem.addVariable(var, slots)
    problem.addConstraint(AllDifferentConstraint(), expanded_subjects)

    # --- Teacher conflict constraint ---
    def no_teacher_conflict(*args):
        teacher_slots = {}
        for i, slot in enumerate(args):
            subject = subject_lookup[expanded_subjects[i]]
            teacher = subject_teacher_map[subject]
            if teacher in teacher_slots and teacher_slots[teacher] == slot:
                return False
            teacher_slots[teacher] = slot
        return True
    problem.addConstraint(no_teacher_conflict, expanded_subjects)

    # --- No duplicate subject constraint ---
    def no_same_subject_clash(*args):
        return len(set(args)) == len(args)

    for subject in subject_periods:
        vars_for_subject = [v for v in expanded_subjects if subject_lookup[v] == subject]
        problem.addConstraint(no_same_subject_clash, vars_for_subject)

    solution = problem.getSolution()
    if not solution:
        messagebox.showerror("Error", "No valid timetable found.")
        return

    # --- Build Timetable Dictionary ---
    timetable = {}
    for day in days:
        for p in period_times:
            key = f"{day[:3]}-{p}"
            timetable[key] = "Break" if p == break_after + 1 else "Free"

    for var, slot in solution.items():
        subject = subject_lookup[var]
        teacher = subject_teacher_map[subject]
        timetable[slot] = f"{subject} ({teacher})"

    display_timetable(timetable)

# --- FUNCTION: Display Timetable in GUI ---
def display_timetable(timetable):
    for widget in frame_output.winfo_children():
        widget.destroy()

    headers = ["Period", "Time"] + days
    for col, text in enumerate(headers):
        label = tk.Label(frame_output, text=text, borderwidth=1, relief="solid", bg="#d9ead3",
                         font=('Segoe UI', 10, 'bold'), padx=5, pady=5)
        label.grid(row=0, column=col, sticky="nsew")

    for row_idx, period in enumerate(period_times, start=1):
        tk.Label(frame_output, text=str(period), borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_idx, column=0, sticky="nsew")
        tk.Label(frame_output, text=period_times[period], borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_idx, column=1, sticky="nsew")

        for col_idx, day in enumerate(days, start=2):
            slot = f"{day[:3]}-{period}"
            text = timetable.get(slot, "Free")
            bg = "#fce5cd" if text != "Break" else "#b6d7a8"
            tk.Label(frame_output, text=text, borderwidth=1, relief="solid", padx=5, pady=5,
                     bg=bg, wraplength=120).grid(row=row_idx, column=col_idx, sticky="nsew")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Automated Timetable Generator (Dropdown Version)")
root.geometry("1200x700")

notebook = ttk.Notebook(root)
frame_input = ttk.Frame(notebook, padding=10)
frame_output_canvas = ttk.Frame(notebook)
notebook.add(frame_input, text="Input Panel")
notebook.add(frame_output_canvas, text="Generated Timetable")
notebook.pack(fill="both", expand=True)

# --- Dropdown Data ---
subjects_list = ["Math", "Science", "English", "Computer", "History"]
teachers_list = ["Mr. Sharma", "Ms. Kaur", "Dr. Singh", "Mrs. Verma"]
periods_list = [str(i) for i in range(1, 9)]
days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
timings_list = [
    "9:00 - 9:45", "9:45 - 10:30", "10:30 - 11:15",
    "11:15 - 12:00", "12:00 - 12:45", "1:15 - 2:00",
    "2:00 - 2:45", "2:45 - 3:30"
]

# --- Subject Dropdowns ---
ttk.Label(frame_input, text="Subject:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_subject = ttk.Combobox(frame_input, values=subjects_list, width=20)
entry_subject.grid(row=0, column=1, padx=5)

ttk.Label(frame_input, text="Teacher:").grid(row=0, column=2, sticky="w", padx=5)
entry_teacher = ttk.Combobox(frame_input, values=teachers_list, width=20)
entry_teacher.grid(row=0, column=3, padx=5)

ttk.Label(frame_input, text="Periods/Week:").grid(row=0, column=4, sticky="w", padx=5)
entry_periods = ttk.Combobox(frame_input, values=periods_list, width=10)
entry_periods.grid(row=0, column=5, padx=5)

ttk.Button(frame_input, text="Add Subject", command=add_subject).grid(row=0, column=6, padx=10)
listbox_subjects = tk.Listbox(frame_input, height=8, width=90)
listbox_subjects.grid(row=1, column=0, columnspan=7, padx=5, pady=10)

# --- Days Dropdown ---
ttk.Label(frame_input, text="Select Days:").grid(row=2, column=0, sticky="w", padx=5)
entry_days = ttk.Combobox(frame_input, values=[", ".join(days_list)], width=50)
entry_days.grid(row=2, column=1, columnspan=3, padx=5)

# --- Timing Dropdown ---
ttk.Label(frame_input, text="Select Timings:").grid(row=3, column=0, sticky="w", padx=5)
timing_var = tk.StringVar()
entry_timing = ttk.Combobox(frame_input, textvariable=timing_var, values=timings_list, width=25)
entry_timing.grid(row=3, column=1, padx=5)
ttk.Button(frame_input, text="Add Timing", command=add_timing).grid(row=3, column=2, padx=5)

text_timings = tk.Text(frame_input, height=5, width=50)
text_timings.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
ttk.Button(frame_input, text="Add Days & Timings", command=add_days_periods).grid(row=4, column=4, padx=10)

# --- Generate Button ---
ttk.Button(frame_input, text="Generate Timetable", command=generate_timetable).grid(row=5, column=0, columnspan=7, pady=20)

# --- Output Frame (scrollable) ---
canvas = tk.Canvas(frame_output_canvas)
scrollbar = ttk.Scrollbar(frame_output_canvas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.pack(side=tk.LEFT, fill="both", expand=True)
canvas.configure(yscrollcommand=scrollbar.set)
frame_output = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame_output, anchor="nw")
frame_output.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()

