# gudlift-registration

## 1. Why

### The company Güdlft is developing a streamlined version of its flagship booking system for local and regional competition organizers. The goal is to simplify the administration of competitions, enabling clubs to register for events within their division. In this phase 1, we need to address issues and conduct tests to ensure that the features comply with the requirements.

## 2.Local Configuration
## Installation
### Getting the project on your local machine.
1. Clone the repository to your local machine.
```bash
git clone https://github.com/xrobotzyh/Python_Testing.git
```
2.Navigate to the cloned directory.
```bash
cd Python_Testing
```

### Create a virtual environment
1.Create a virtual environment named "env".
```bash
python3 -m venv env
```

### Activate and install your virtual environment
Activate the newly created virtual environment "env".
```bash
source env/bin/activate
```
Install the packages listed in requirements.txt.
```bash
pip install -r requirements.txt
```

### Run the server
```bash
python manage.py makemigrations
```
Apply the migrations.
```bash
python manage.py migrate
```

## Usage
### Start the server,Set the Flask application as an environment variable.
```bash
export FLASK_APP=server.py
```
### Run server
python -m flask run

## Test
Use the following information to test
```bash
pytest -v
```

## Thanks!