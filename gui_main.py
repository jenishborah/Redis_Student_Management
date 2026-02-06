import tkinter as tk
from tkinter import ttk, messagebox
import redis
import re

# ---------- Redis Connection ----------
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

update_mode = False


# ---------- Grade Calculation ----------
def calculate_grade(total):
    if total >= 95:
        return "O"
    elif total >= 85:
        return "A+"
    elif total >= 75:
        return "A"
    elif total >= 65:
        return "B+"
    elif total >= 55:
        return "B"
    elif total >= 45:
        return "P"
    else:
        return "F"


# ---------- Validation ----------
def validate_inputs(enrol, name, st1, mid, st2, end):
    if not enrol or not name:
        messagebox.showerror("Error", "Enrollment and Name required")
        return False

    if not re.match(r"^[A-Za-z0-9]+$", enrol):
        messagebox.showerror("Error", "Invalid enrollment format")
        return False

    try:
        st1, mid, st2, end = int(st1), int(mid), int(st2), int(end)
    except:
        messagebox.showerror("Error", "Marks must be integers")
        return False

    if not (0 <= st1 <= 10):
        messagebox.showerror("Error", "ST1 must be 0-10")
        return False
    if not (0 <= mid <= 30):
        messagebox.showerror("Error", "Mid must be 0-30")
        return False
    if not (0 <= st2 <= 10):
        messagebox.showerror("Error", "ST2 must be 0-10")
        return False
    if not (0 <= end <= 40):
        messagebox.showerror("Error", "End must be 0-40")
        return False

    return True


# ---------- Add Student ----------
def add_student():
    enrol = enrol_entry.get().strip()
    name = name_entry.get().strip()

    st1, mid, st2, end = st1_entry.get(), mid_entry.get(), st2_entry.get(), end_entry.get()

    if not validate_inputs(enrol, name, st1, mid, st2, end):
        return

    if r.exists(f"student:{enrol}"):
        messagebox.showerror("Error", "Student already exists")
        return

    st1, mid, st2, end = int(st1), int(mid), int(st2), int(end)
    total = st1 + mid + st2 + end
    grade = calculate_grade(total)

    r.hset(f"student:{enrol}", mapping={
        "name": name,
        "st1": st1,
        "mid": mid,
        "st2": st2,
        "end": end,
        "total": total,
        "grade": grade
    })

    messagebox.showinfo("Success", "Student Added")
    clear_fields()
    list_students()


# ---------- View Student ----------
def view_student():
    enrol = enrol_entry.get().strip()
    data = r.hgetall(f"student:{enrol}")

    if not data:
        messagebox.showerror("Error", "Student not found")
        return

    name_entry.delete(0, tk.END)
    name_entry.insert(0, data["name"])

    st1_entry.delete(0, tk.END)
    st1_entry.insert(0, data["st1"])

    mid_entry.delete(0, tk.END)
    mid_entry.insert(0, data["mid"])

    st2_entry.delete(0, tk.END)
    st2_entry.insert(0, data["st2"])

    end_entry.delete(0, tk.END)
    end_entry.insert(0, data["end"])


# ---------- Improved Update ----------
def update_student():
    global update_mode

    enrol = enrol_entry.get().strip()
    key = f"student:{enrol}"

    if not r.exists(key):
        messagebox.showerror("Error", "Student not found")
        return

    # First click → Load data
    if not update_mode:
        data = r.hgetall(key)

        name_entry.delete(0, tk.END)
        name_entry.insert(0, data["name"])

        st1_entry.delete(0, tk.END)
        st1_entry.insert(0, data["st1"])

        mid_entry.delete(0, tk.END)
        mid_entry.insert(0, data["mid"])

        st2_entry.delete(0, tk.END)
        st2_entry.insert(0, data["st2"])

        end_entry.delete(0, tk.END)
        end_entry.insert(0, data["end"])

        update_mode = True
        messagebox.showinfo("Update Mode", "Modify marks and click Update again")
        return

    # Second click → Save updated data
    name = name_entry.get().strip()
    st1, mid, st2, end = st1_entry.get(), mid_entry.get(), st2_entry.get(), end_entry.get()

    if not validate_inputs(enrol, name, st1, mid, st2, end):
        return

    st1, mid, st2, end = int(st1), int(mid), int(st2), int(end)
    total = st1 + mid + st2 + end
    grade = calculate_grade(total)

    r.hset(key, mapping={
        "name": name,
        "st1": st1,
        "mid": mid,
        "st2": st2,
        "end": end,
        "total": total,
        "grade": grade
    })

    update_mode = False
    messagebox.showinfo("Success", "Student Updated")
    list_students()


# ---------- Delete ----------
def delete_student():
    enrol = enrol_entry.get().strip()

    if not r.exists(f"student:{enrol}"):
        messagebox.showerror("Error", "Student not found")
        return

    r.delete(f"student:{enrol}")
    messagebox.showinfo("Deleted", "Student Deleted")
    clear_fields()
    list_students()


# ---------- List Students ----------
def list_students():
    for row in tree.get_children():
        tree.delete(row)

    for key in r.keys("student:*"):
        enrol = key.split(":")[1]
        data = r.hgetall(key)

        tree.insert("", "end", values=(
            enrol,
            data["name"],
            data["st1"],
            data["mid"],
            data["st2"],
            data["end"],
            data["total"],
            data["grade"]
        ))


# ---------- Clear Fields ----------
def clear_fields():
    global update_mode
    update_mode = False

    for entry in entries:
        entry.delete(0, tk.END)


# ---------- GUI ----------
root = tk.Tk()
root.title("Redis Student Management System")
root.geometry("1000x600")
root.configure(bg="#eef2f3")

title = tk.Label(
    root,
    text="Student Management System",
    font=("Helvetica", 20, "bold"),
    bg="#eef2f3"
)
title.pack(pady=10)

frame = tk.Frame(root, bg="#eef2f3")
frame.pack()

labels = ["Enrollment", "Name", "ST1", "Mid", "ST2", "End"]

enrol_entry = tk.Entry(frame, width=30)
name_entry = tk.Entry(frame, width=30)
st1_entry = tk.Entry(frame, width=30)
mid_entry = tk.Entry(frame, width=30)
st2_entry = tk.Entry(frame, width=30)
end_entry = tk.Entry(frame, width=30)

entries = [enrol_entry, name_entry, st1_entry, mid_entry, st2_entry, end_entry]

for i, label in enumerate(labels):
    tk.Label(frame, text=label, bg="#eef2f3").grid(row=i, column=0, pady=5)
    entries[i].grid(row=i, column=1, pady=5)

btn_frame = tk.Frame(root, bg="#eef2f3")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", bg="#28a745", fg="white", command=add_student).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="View", bg="#007bff", fg="white", command=view_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", bg="#ffc107", command=update_student).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", bg="#dc3545", fg="white", command=delete_student).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Clear", bg="#6c757d", fg="white", command=clear_fields).grid(row=0, column=4, padx=5)

columns = ("Enroll", "Name", "ST1", "Mid", "ST2", "End", "Total", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

tree.pack(pady=20)

list_students()
root.mainloop()
