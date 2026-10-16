#!/usr/bin/env python3
"""
Simple Student Management System (Python)
Data is stored in students.json in the same directory.
Commands: add, list, find, update, delete, exit
"""
import json
import os
from typing import List, Dict

DATA_FILE = "students.json"

def load_students() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_students(students: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)

def next_id(students: List[Dict]) -> int:
    if not students:
        return 1
    return max(s["id"] for s in students) + 1

def add_student(students: List[Dict]) -> None:
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    grade = input("Grade: ").strip()
    sid = next_id(students)
    students.append({"id": sid, "name": name, "age": age, "grade": grade})
    save_students(students)
    print(f"Added student with id {sid}")

def list_students(students: List[Dict]) -> None:
    if not students:
        print("No students found.")
        return
    print("{:>4}  {:<20} {:<4} {:<6}".format("ID", "Name", "Age", "Grade"))
    print("-" * 38)
    for s in students:
        print("{:>4}  {:<20} {:<4} {:<6}".format(s["id"], s["name"], s["age"], s["grade"]))

def find_student(students: List[Dict]) -> None:
    q = input("Enter id or name to search: ").strip()
    found = [s for s in students if str(s["id"]) == q or q.lower() in s["name"].lower()]
    if not found:
        print("No matching students.")
        return
    for s in found:
        print(json.dumps(s, indent=2))

def update_student(students: List[Dict]) -> None:
    sid = input("Enter id to update: ").strip()
    for s in students:
        if str(s["id"]) == sid:
            name = input(f"Name [{s['name']}]: ").strip() or s["name"]
            age = input(f"Age [{s['age']}]: ").strip() or s["age"]
            grade = input(f"Grade [{s['grade']}]: ").strip() or s["grade"]
            s.update({"name": name, "age": age, "grade": grade})
            save_students(students)
            print("Updated.")
            return
    print("Student id not found.")

def delete_student(students: List[Dict]) -> None:
    sid = input("Enter id to delete: ").strip()
    for i, s in enumerate(students):
        if str(s["id"]) == sid:
            confirm = input(f"Delete {s['name']} (id {s['id']})? [y/N]: ").lower()
            if confirm == "y":
                students.pop(i)
                save_students(students)
                print("Deleted.")
            else:
                print("Cancelled.")
            return
    print("Student id not found.")

def menu() -> None:
    students = load_students()
    commands = {
        "add": add_student,
        "list": list_students,
        "find": find_student,
        "update": update_student,
        "delete": delete_student,
    }
    while True:
        cmd = input("\nCommand (add/list/find/update/delete/exit): ").strip().lower()
        if cmd == "exit":
            break
        func = commands.get(cmd)
        if func:
            func(students)
        else:
            print("Unknown command.")

if __name__ == "__main__":
    print("Student Management System (Python)")
    menu()
