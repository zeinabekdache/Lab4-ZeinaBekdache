"""
School Management System GUI Application

This module provides a comprehensive Tkinter-based graphical user interface
for managing school records, including students, instructors, and courses.

:module: gui
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
from db_manager import DatabaseManager
import shutil


class SchoolManagementSystemGui(tk.Tk):
    """
    Main application class for the School Management System GUI.

    This class inherits from tk.Tk and provides a GUI interface
    for managing school-related data, including students, instructors, and courses.

    Attributes:
        db (DatabaseManager): Database connection and management object
        notebook (ttk.Notebook): Tabbed interface for different management sections
    """
    def __init__(self):
        """
        Initialize the School Management System GUI.

        Sets up the main window, creates database connection, initializes tabs,
        and loads initial data. Provides a backup database functionality.
        """
        super().__init__()
        self.title("School Management System")
        self.geometry("800x600")

        # initialize db connection
        self.db = DatabaseManager()

        # creating tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_school_tab()

        # defining reusable template for buttons
        button_component = tk.Frame(self)
        button_component.pack(padx = 4, pady = 6)

        backup_button = tk.Button(button_component, text="Backup Database", command=self.backup_database)
        backup_button.pack(side= "right", padx=5)

        # load data on startup
        self.load_data()

    def create_student_tab(self):
        """
        Create the student management tab in the application.

        Sets up input fields and controls for adding new students,
        including name, age, email, ID, and course registration.
        """
        student_tab = ttk.Frame(self.notebook)
        self.notebook.add(student_tab, text="Add Student")
        ttk.Label(student_tab, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.student_name = ttk.Entry(student_tab)
        self.student_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(student_tab, text="Age:").grid(row=1, column=0, padx=10, pady=5)
        self.student_age = ttk.Entry(student_tab)
        self.student_age.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(student_tab, text="email:").grid(row=2, column=0, padx=10, pady=5)
        self.student_email = ttk.Entry(student_tab)
        self.student_email.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(student_tab, text="ID:").grid(row=3, column=0, padx=10, pady=5)
        self.student_id = ttk.Entry(student_tab)
        self.student_id.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(student_tab, text="Register Course:").grid(row=4, column=0, padx=10, pady=5)
        self.student_courses = tk.Listbox(student_tab, selectmode="multiple", height=4)
        for course in self.get_course_names():
            self.student_courses.insert(tk.END, course)
        self.student_courses.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(student_tab, text="Add Student", command=self.add_student).grid(row=5, columnspan=2, pady=10)

    def add_student(self):
        """
        Add a new student to the database.

        Validates input fields, adds student record, and registers
        selected courses. Displays success or error messages.

        Raises:
            ValueError: If required fields are missing or invalid
            Exception: For database-related errors
        """
        try:
            name = self.student_name.get().strip()
            age = int(self.student_age.get().strip())
            email = self.student_email.get().strip()
            student_id = self.student_id.get().strip()
            selected_indices = self.student_courses.curselection()

            if not all([name, age, email, student_id]):
                raise ValueError("All fields are required!")

            # Get selected course IDs
            courses = self.db.get_courses()
            selected_course_ids = [courses[i][0] for i in selected_indices]

            # Add student to database
            self.db.add_student(student_id, name, age, email)

            # Register courses
            self.db.update_student_registrations(student_id, selected_course_ids)

            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_form([self.student_name, self.student_age, self.student_email,
                            self.student_id, self.student_courses])
            self.load_data()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    def create_instructor_tab(self):
        """
        Create the instructor management tab in the application.

        Sets up input fields and controls for adding new instructors,
        including name, age, email, ID, and course assignment.
        """
        instructor_tab = ttk.Frame(self.notebook)
        self.notebook.add(instructor_tab, text="Add Instructor")
        ttk.Label(instructor_tab, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.instructor_name = ttk.Entry(instructor_tab)
        self.instructor_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(instructor_tab, text="Age:").grid(row=1, column=0, padx=10, pady=5)
        self.instructor_age = ttk.Entry(instructor_tab)
        self.instructor_age.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(instructor_tab, text="email:").grid(row=2, column=0, padx=10, pady=5)
        self.instructor_email = ttk.Entry(instructor_tab)
        self.instructor_email.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(instructor_tab, text="ID:").grid(row=3, column=0, padx=10, pady=5)
        self.instructor_id = ttk.Entry(instructor_tab)
        self.instructor_id.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(instructor_tab, text="Assign Course:").grid(row=4, column=0, padx=10, pady=5)
        self.instructor_courses = tk.Listbox(instructor_tab, selectmode="multiple", height=4 )
        for course in self.get_course_names():
            self.instructor_courses.insert(tk.END, course)
        self.instructor_courses.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(instructor_tab, text="Add Instructor", command=self.add_instructor).grid(row=5, columnspan=2, pady=10)

    def add_instructor(self):
        """
        Add a new instructor to the database.

        Validates input fields, adds instructor record, and assigns
        selected courses. Displays success or error messages.

        Raises:
            ValueError: If required fields are missing or invalid
            Exception: For database-related errors
        """
        try:
            name = self.instructor_name.get().strip()
            age = int(self.instructor_age.get().strip())
            email = self.instructor_email.get().strip()
            instructor_id = self.instructor_id.get().strip()
            selected_indices = self.instructor_courses.curselection()

            if not all([name, age, email, instructor_id]):
                raise ValueError("All fields are required!")

            # Add instructor to database
            self.db.add_instructor(instructor_id, name, age, email)

            # Assign selected courses
            courses = self.db.get_courses()
            for i, course in enumerate(courses):
                if i in selected_indices:
                    self.db.update_course(course[0], course[1], instructor_id)

            messagebox.showinfo("Success", "Instructor added successfully!")
            self.clear_form([self.instructor_name, self.instructor_age, self.instructor_email,
                            self.instructor_id, self.instructor_courses])
            self.load_data()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add instructor: {str(e)}")

    def create_course_tab(self):
        """
        Create the course management tab in the application.

        Sets up input fields and controls for adding new courses,
        including course name and course ID.
        """
        course_tab = ttk.Frame(self.notebook)
        self.notebook.add(course_tab, text="Add Course")
        ttk.Label(course_tab, text="Course Name:").grid(row=0, column=0, padx=10, pady=5)
        self.course_name = ttk.Entry(course_tab)
        self.course_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(course_tab, text="Course ID").grid(row=1, column=0, padx=10, pady=5)
        self.course_id = ttk.Entry(course_tab)
        self.course_id.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(course_tab, text="Add Course", command=self.add_course).grid(row=4, columnspan=2, pady=10)

    def add_course(self):
        """
        Add a new course to the database.

        Validates input fields and adds course record.
        Displays success or error messages.

        Raises:
            ValueError: If required fields are missing or invalid
            Exception: For database-related errors
        """
        try:
            course_id = self.course_id.get().strip()
            course_name = self.course_name.get().strip()

            if not all([course_id, course_name]):
                raise ValueError("All fields are required!")

            # Add course to database
            self.db.add_course(course_id, course_name, None)

            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_form([self.course_name, self.course_id])
            self.load_data()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")

    def get_course_names(self):
        """
        Retrieve a list of course names from the database.

        Returns:
            list: A list of course names
        """
        return [course[1] for course in self.db.get_courses()]

    def create_school_tab(self):
        """
        Create the school records tab in the application.

        Sets up a treeview for displaying school records and
        provides search, edit, and delete functionalities.
        """
        school_tab = ttk.Frame(self.notebook)
        self.notebook.add(school_tab, text="School Records")
        self.tree = ttk.Treeview(school_tab, columns=("type", "name", "id"), show="headings")
        self.tree.heading("type", text="Type")
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="ID")
        self.tree.pack(fill="both", expand=True)
        button_component = tk.Frame(school_tab)
        button_component.pack(padx=4, pady=4)
        search_label=tk.Label(button_component, text="Search")
        search_label.pack(side="left")
        self.search_entry = tk.Entry(button_component)
        self.search_entry.pack(side="left", padx=4)
        search_button = tk.Button(button_component, text="Search", command=self.search_data)
        search_button.pack(side= "left", padx=4)
        edit_button = tk.Button(button_component, text="Edit", command=self.edit_data)
        edit_button.pack(side= "left", padx=4)
        delete_button = tk.Button(button_component, text="Delete", command=self.delete_data)
        delete_button.pack(side= "left", padx=4)

    def search_data(self):
        """
        Search and display records based on user input.

        Performs a case-insensitive search across school records
        and displays matching results in a popup window.
        """
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Info", "Please input a search term.")
            return

        results = self.db.search_records(query)

        if not results:
            messagebox.showinfo("No Results", "No matching records found.")
            return

        # Create popup window for search results
        popup = tk.Toplevel(self)
        popup.title("Search Results")
        popup.geometry("600x400")

        tk.Label(popup, text="Search Results").pack(pady=10)
        results_tree = ttk.Treeview(popup, columns=("type", "name", "id", "details"), show="headings")
        results_tree.heading("type", text="Type")
        results_tree.heading("name", text="Name")
        results_tree.heading("id", text="ID")
        results_tree.heading("details", text="Details")
        results_tree.pack(fill="both", expand=True, padx=10, pady=10)

        for result in results:
            record_type = result[0]
            if record_type == "Student":
                details = f"Age: {result[3]}, Email: {result[4]}"
                values = (record_type, result[2], result[1], details)
            elif record_type == "Instructor":
                details = f"Age: {result[3]}, Email: {result[4]}"
                values = (record_type, result[2], result[1], details)
            else:  # Course
                instructor_name = result[4] if result[4] else "No instructor assigned"
                details = f"Instructor: {instructor_name}"
                values = (record_type, result[2], result[1], details)
            results_tree.insert("", "end", values=values)

        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def edit_data(self):
        """
        Edit a selected record from the school records.

        Provides edit dialogs for students, instructors, and courses
        with validation and update functionality.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return

        record_type, name, record_id = self.tree.item(selected_item, "values")

        if record_type == "Student":
            student = next((s for s in self.db.get_students() if s[0] == record_id), None)
            if student:
                # Create edit dialog
                edit_window = tk.Toplevel(self)
                edit_window.title("Edit Student")
                edit_window.geometry("400x500")

                tk.Label(edit_window, text="Name:").pack(pady=5)
                name_entry = tk.Entry(edit_window)
                name_entry.insert(0, student[1])
                name_entry.pack(pady=5)

                tk.Label(edit_window, text="Age:").pack(pady=5)
                age_entry = tk.Entry(edit_window)
                age_entry.insert(0, student[2])
                age_entry.pack(pady=5)

                tk.Label(edit_window, text="Email:").pack(pady=5)
                email_entry = tk.Entry(edit_window)
                email_entry.insert(0, student[3])
                email_entry.pack(pady=5)

                tk.Label(edit_window, text="Registered Courses:").pack(pady=5)
                courses_listbox = tk.Listbox(edit_window, selectmode="multiple", height=6)
                all_courses = self.db.get_courses()
                student_courses = self.db.get_student_courses(record_id)
                student_course_ids = [c[0] for c in student_courses]

                for i, course in enumerate(all_courses):
                    courses_listbox.insert(tk.END, f"{course[1]} ({course[0]})")
                    if course[0] in student_course_ids:
                        courses_listbox.selection_set(i)
                courses_listbox.pack(pady=5)

                def save_changes():
                    try:
                        new_name = name_entry.get().strip()
                        new_age = int(age_entry.get().strip())
                        new_email = email_entry.get().strip()

                        if not all([new_name, new_age, new_email]):
                            messagebox.showerror("Error", "All fields are required!")
                            return

                        # Update student info
                        self.db.update_student(record_id, new_name, new_age, new_email)

                        # Update course registrations
                        selected_indices = courses_listbox.curselection()
                        selected_course_ids = [all_courses[i][0] for i in selected_indices]
                        self.db.update_student_registrations(record_id, selected_course_ids)

                        self.load_data()
                        messagebox.showinfo("Success", "Student record updated successfully!")
                        edit_window.destroy()

                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

        elif record_type == "Instructor":
            instructor = next((i for i in self.db.get_instructors() if i[0] == record_id), None)
            if instructor:
                # Create edit dialog
                edit_window = tk.Toplevel(self)
                edit_window.title("Edit Instructor")
                edit_window.geometry("400x500")

                tk.Label(edit_window, text="Name:").pack(pady=5)
                name_entry = tk.Entry(edit_window)
                name_entry.insert(0, instructor[1])
                name_entry.pack(pady=5)

                tk.Label(edit_window, text="Age:").pack(pady=5)
                age_entry = tk.Entry(edit_window)
                age_entry.insert(0, instructor[2])
                age_entry.pack(pady=5)

                tk.Label(edit_window, text="Email:").pack(pady=5)
                email_entry = tk.Entry(edit_window)
                email_entry.insert(0, instructor[3])
                email_entry.pack(pady=5)

                tk.Label(edit_window, text="Assigned Courses:").pack(pady=5)
                courses_listbox = tk.Listbox(edit_window, selectmode="multiple", height=6)
                all_courses = self.db.get_courses()
                instructor_courses = [c for c in all_courses if c[2] == record_id]

                for i, course in enumerate(all_courses):
                    courses_listbox.insert(tk.END, f"{course[1]} ({course[0]})")
                    if course in instructor_courses:
                        courses_listbox.selection_set(i)
                courses_listbox.pack(pady=5)

                def save_changes():
                    try:
                        new_name = name_entry.get().strip()
                        new_age = int(age_entry.get().strip())
                        new_email = email_entry.get().strip()

                        if not all([new_name, new_age, new_email]):
                            messagebox.showerror("Error", "All fields are required!")
                            return

                        # Update instructor info
                        self.db.update_instructor(record_id, new_name, new_age, new_email)

                        # Update course assignments
                        selected_indices = courses_listbox.curselection()
                        for i, course in enumerate(all_courses):
                            if i in selected_indices:
                                self.db.update_course(course[0], course[1], record_id)
                            elif course[2] == record_id:
                                self.db.update_course(course[0], course[1], None)

                        self.load_data()
                        messagebox.showinfo("Success", "Instructor record updated successfully!")
                        edit_window.destroy()

                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

        elif record_type == "Course":
            course = next((c for c in self.db.get_courses() if c[0] == record_id), None)
            if course:
                new_name = simpledialog.askstring("Edit Course", "Enter new course name:", initialvalue=course[1])
                if new_name:
                    self.db.update_course(record_id, new_name, course[2])
                    self.load_data()
                    messagebox.showinfo("Success", "Course updated successfully!")

    def delete_data(self):
        """
        Delete a selected record from the school records.

        Provides confirmation dialog and deletes the selected
        student, instructor, or course from the database.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        record_type, name, record_id = self.tree.item(selected_item, "values")

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            try:
                if record_type == "Student":
                    self.db.delete_student(record_id)
                elif record_type == "Instructor":
                    self.db.delete_instructor(record_id)
                elif record_type == "Course":
                    self.db.delete_course(record_id)

                self.load_data()
                messagebox.showinfo("Success", f"{record_type} deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}")

    def load_data(self):
        """
        Load and display current school records in the treeview.

        Retrieves students, instructors, and courses from the database
        and populates the school records tab.
        """
        self.tree.delete(*self.tree.get_children())
        for student in self.db.get_students():
          self.tree.insert("", "end", values=("Student", student[1], student[0]))
        for instructor in self.db.get_instructors():
          self.tree.insert("", "end", values=("Instructor", instructor[1], instructor[0]))
        for course in self.db.get_courses():
          self.tree.insert("", "end", values=("Course", course[1], course[0]))

        self.refresh_course_list()

    def refresh_course_list(self):
        """
        Refresh the course lists in student and instructor tabs.

        Clears and repopulates course selection listboxes
        with the latest courses from the database.
        """
        # Clear current list and load fresh courses
        self.student_courses.delete(0, tk.END)
        self.instructor_courses.delete(0, tk.END)

        # Populate Listboxes with the latest courses
        for course in self.get_course_names():
            self.student_courses.insert(tk.END, course)
            self.instructor_courses.insert(tk.END, course)

    def clear_form(self, fields):
        """
        Clear input fields after successful record addition.

        Args:
            fields (list): List of input fields to be cleared
        """
        for field in fields:
            if isinstance(field, tk.Entry):  # For Entry widgets
                field.delete(0, tk.END)
            elif isinstance(field, tk.Listbox):  # For Listbox widgets
                field.selection_clear(0, tk.END)
            elif isinstance(field, ttk.Combobox):  # For Combobox widgets
                field.set("")

    def backup_database(self):
        """
        Create a backup of the school management database.

        Provides a file dialog for selecting backup location
        and copies the database file to the chosen path.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".db",
                                                 filetypes=[("SQLite Database", "*.db")])
        if file_path:
            shutil.copy("school_data.db", file_path)
            messagebox.showinfo("Success", f"Database backed up to {file_path}")


if __name__ == "__main__":
    """
    Entry point for the School Management System application.

    Instantiates the GUI and starts the main event loop.
    """
    app = SchoolManagementSystemGui()
    app.mainloop()
