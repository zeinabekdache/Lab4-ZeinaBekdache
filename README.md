# Lab4-ZeinaBekdache
This is a Python-based desktop application built using Tkinter for the GUI and SQLite for the database. The project also includes Sphinx for generating documentation.

Prerequisites
Make sure you have the following installed:

Python 3.13
Tkinter (usually comes pre-installed with Python, if not you install it manually)
SQLite 
Sphinx for documentation

### Install the Required Python Packages in a Virtual Environment

1. Clone the repository
  ```bash
  git clone <repo-url>
  ```  
2. Create and activate virtual environment
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. Install dependencies:
   - sphinx
   - sqlite3
   - tkinter
4. run the app
   ```bash
   python3 tkinter_gui.py
   ```

### Generating Docs
```bash
sphinx-quickstart # initializes your sphinx docs
make html # builds your html documentation
```

Author: This project is owned by Zeina Bekdache
