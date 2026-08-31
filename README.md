# Cybersecurity Simple Notes

## 1. Project description

Cybersecurity Simple Notes is a small Flask web application created for Project I of the University of Helsinki Cyber Security Base course. This application intentionally contains five security flaws for educational purposes.

## 2. Prerequisites

The application requires:

- Python 3
- pip
- Flask

## 3. Installation

Clone or download the repository and open a terminal in the project directory.

### Windows

Create a virtual environment:

```bash
py -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install Flask:

```bash
py -m pip install Flask
```

### Linux

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install Flask:

```bash
python3 -m pip install Flask
```

### macOS

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install Flask:

```bash
python3 -m pip install Flask
```

## 4. Database setup

The database structure is provided in `schema.sql`.

Before running the application for the first time, create `notes.db` from the schema.

### Windows

Make sure that the SQLite command-line tool is installed and available in `PATH`.

Then run:

```bash
sqlite3 notes.db < schema.sql
```

### Linux

If SQLite is not installed, install it first.

On Debian/Ubuntu-based systems:

```bash
sudo apt install sqlite3
```

Then create the database:

```bash
sqlite3 notes.db < schema.sql
```

### macOS

If SQLite is not available, it can be installed with Homebrew:

```bash
brew install sqlite
```

Then create the database:

```bash
sqlite3 notes.db < schema.sql
```

This creates the SQLite database file `notes.db` in the project directory using the tables defined in `schema.sql`.

## 5. Running the application

Make sure that the virtual environment is activated and that `notes.db` has been created.

### Windows

Run the application with:

```bash
py -m flask --app app run
```

### Linux and macOS

Run the application with:

```bash
python3 -m flask --app app run
```

After starting the server, open the following address in a web browser:

```text
http://127.0.0.1:5000
```

To stop the development server, press `Ctrl+C` in the terminal.
