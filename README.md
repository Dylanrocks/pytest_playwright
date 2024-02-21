
# Automation Project

## Prerequisites

Before running the tests, ensure that you have the following prerequisites:<br />

Python installed (version 3.12.X)<br />
Pip package manager installed<br />
Git installed<br />

## Project Structure

The repository contains:<br />
- `apps_pages` folder: classes for page in the app
- `config ` folder: Contains config parser and .ini
- `core` folder: generic elements classes and utilis
- `tests ` folder: UI tests


## Setup

1. Clone the Repository:
```
git clone https://github.com/Dylanrocks/pytest_playwright.git
```

2.Navigate to the project directory

3.Create a virtual environment:
```
py -m venv env
```

3.Activate the virtual environment:
```
.\env\Scripts\activate
```

4.Install project  Dependencies:<br />
```
pip install -r requirements.txt
```


## Running Tests
```
pytest --html=report.html
```

## Viewing Test Results
Open report.html  in project directory

