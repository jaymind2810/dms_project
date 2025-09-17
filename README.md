<div align="center">

# Ecommerce Website
</div>

## Overview

Web application using django framework.

Applicaton For Document Management Tool


## Cloning the repository

- Clone the repository using the command below :

```bash
git clone https://github.com/jaymind2810/dms_project.git

```

- Move into the directory where we have the project files : 
```bash
cd dms_project
```

- Create a virtual environment :
```bash
# Let's install virtualenv first
sudo apt install python3-venv

# Then we create our virtual environment
python3 -m venv venv
```

- Activate the virtual environment :
```bash
source venv/bin/activate
```

- Install the requirements :
```bash
pip install -r requirements.txt
```

#

### Import Database

```bash
mysql -u root -p dms_db < dms_db.sql
```


### Running the App

- for make migrations the App
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

- for create super user for App
```bash
python3 manage.py createsuperuser
```

- for run server
```bash
python3 manage.py runserver
```

- Then, the development server will be started at http://127.0.0.1:8000/

- You will find docs management here at http://127.0.0.1:8000/docs/









