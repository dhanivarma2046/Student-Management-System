import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import csv

DB_NAME = "students.db"

root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x700")
root.configure(bg="#EAF6F6")

title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 24, "bold"),
    bg="#EAF6F6",
    fg="#1B262C"
)

title.pack(pady=20)
dashboard_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#EAF6F6",
    fg="#0F4C75"
)

dashboard_label.pack(pady=5)

# ---------- INPUT FRAME ----------
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Age").grid(row=0, column=2, padx=5, pady=5)
tk.Label(input_frame, text="Course").grid(row=1, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Marks").grid(row=1, column=2, padx=5, pady=5)

name_entry = tk.Entry(
    input_frame,
    font=("Arial",12),
    width=20
)
age_entry = tk.Entry(
    input_frame,
    font=("Arial",12),
    width=20
)
course_entry = tk.Entry(
    input_frame,
    font=("Arial",12),
    width=20
)
marks_entry = tk.Entry(
    input_frame,
    font=("Arial",12),
    width=20
)

name_entry.grid(row=0, column=1, padx=5, pady=5)
age_entry.grid(row=0, column=3, padx=5, pady=5)
course_entry.grid(row=1, column=1, padx=5, pady=5)
marks_entry.grid(row=1, column=3, padx=5, pady=5)

# ---------- FUNCTIONS ----------
def update_dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    average_marks = cursor.fetchone()[0]

    conn.close()

    if average_marks is None:
        average_marks = 0

    dashboard_label.config(
        text=f"Total Students: {total_students}   |   Average Marks: {average_marks:.2f}"
    )

def view_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()

    for item in student_table.get_children():
        student_table.delete(item)

    for row in rows:
        student_table.insert("", tk.END, values=row)
    update_dashboard()

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if name == "" or age == "" or course == "" or marks == "":
        messagebox.showwarning("Input Error", "All fields are required")
        return
    
    if not age.isdigit() or not marks.isdigit():
        messagebox.showerror("Input Error", "Age and Marks must be numbers")
        return


    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, age, course, marks) VALUES (?, ?, ?, ?)",
        (name, age, course, marks)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student added successfully")
    view_students()

def search_student():
    name = name_entry.get()

    if name == "":
        messagebox.showwarning("Input Error", "Enter name to search")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT * FROM students
    WHERE name=? OR course=?
    """,
    (name, name)
    )

    rows = cursor.fetchall()
    conn.close()

    for item in student_table.get_children():
        student_table.delete(item)

    for row in rows:
        student_table.insert("", tk.END, values=row)

    if len(rows) == 0:
        messagebox.showinfo("Not Found", "No student found")

def sort_marks():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students ORDER BY marks DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    for item in student_table.get_children():
        student_table.delete(item)

    for row in rows:
        student_table.insert("", tk.END, values=row)

def select_record(event):
    selected = student_table.focus()
    values = student_table.item(selected, "values")

    if values:
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])
        course_entry.insert(0, values[3])
        marks_entry.insert(0, values[4])

def update_student():

    selected = student_table.focus()

    values = student_table.item(selected, "values")

    if not values:
        messagebox.showwarning(
            "Selection Error",
            "Select a student first"
        )
        return

    student_id = values[0]

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if name == "" or age == "" or course == "" or marks == "":
        messagebox.showwarning("Input Error", "All fields are required")
        return

    if not age.isdigit() or not marks.isdigit():
        messagebox.showerror("Input Error", "Age and Marks must be numbers")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=?, age=?, course=?, marks=?
        WHERE id=?
        """,
        (name, age, course, marks, student_id)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Student updated successfully"
    )

    view_students()

def delete_student():
    selected = student_table.focus()
    values = student_table.item(selected, "values")

    if not values:
        messagebox.showwarning(
            "Selection Error",
            "Select a student first"
        )
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if answer:
        student_id = values[0]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully"
        )

        view_students()
        clear_fields()

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()

    with open("students_export.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["ID", "Name", "Age", "Course", "Marks"])
        writer.writerows(rows)

    messagebox.showinfo("Success", "Data exported to students_export.csv")

# ---------- BUTTON ----------
# ---------- BUTTON FRAME ----------
button_frame = tk.Frame(root, bg="#EAF6F6")
button_frame.pack(pady=10)

add_button = tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    bg="#4CAF50",
    fg="white",
    font=("Arial",11,"bold"),
    command=add_student
)
add_button.grid(row=0, column=0, padx=5)

search_button = tk.Button(
    button_frame,
    text="Search Student",
    width=15,
    bg="#2196F3",
    fg="white",
    font=("Arial",11,"bold"),
    command=search_student
)
search_button.grid(row=0, column=1, padx=5)

sort_button = tk.Button(
    button_frame,
    text="Sort Marks",
    bg="#673AB7",
    fg="white",
    width=15,
    command=sort_marks
)
sort_button.grid(row=0,column=7,padx=5)

update_button = tk.Button(
    button_frame,
    text="Update Student",
    width=15,
    bg="#FFC107",
    command=update_student
)
update_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    bg="#F44336",
    command=delete_student
)
delete_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear Fields",
    width=15,
    bg="#9E9E9E",
    command=clear_fields
)
clear_button.grid(row=0, column=4, padx=5)

show_all_button = tk.Button(
    button_frame,
    text="Show All Students",
    width=15,
    bg="#3F51B5",
    command=view_students
)
show_all_button.grid(row=0, column=5, padx=5)

export_button = tk.Button(
    button_frame,
    text="Export CSV",
    width=15,
    bg="#009688",
    command=export_csv
)
export_button.grid(row=0, column=6, padx=5)

# ---------- TABLE ----------
columns = ("ID", "Name", "Age", "Course", "Marks")

student_table = ttk.Treeview(root, columns=columns, show="headings")
style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    font=("Arial",11),
    rowheight=30
)

style.configure(
    "Treeview.Heading",
    font=("Arial",12,"bold")
)

for col in columns:
    student_table.heading(col, text=col)
    student_table.column(
    col,
    width=180,
    anchor="center"
)

student_table.pack(fill="both", expand=True, padx=20, pady=20)
student_table.bind("<ButtonRelease-1>", select_record)

view_students()

root.mainloop()