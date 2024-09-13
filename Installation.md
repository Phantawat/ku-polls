## KU Polls Installation Guide

This guide provides step-by-step instructions for setting up and running the KU Polls application.

## Prerequisites

* Python 3.9 or newer is required.
* All necessary Python packages are listed in [requirements.txt](./requirements.txt).

## Setup Instructions

### 1. Clone the Repository

Begin by cloning the repository to your local machine:
```bash
git clone https://github.com/Phantawat/ku-polls.git
```

### 2. Navigate to the Project Directory

Change into the project directory:
```bash
cd ku-polls
```

### 3. Create a Virtual Environment

Set up a virtual environment to manage dependencies:
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Activate the virtual environment to isolate your project dependencies.
- On Windows:
```bash
venv\Scripts\activate
```
- On Linux/Mac:
```bash
source venv/bin/activate
```

### 5. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 6. Create the `.env` Configuration File

Set up your environment variables by creating a `.env` file in the project root (where `manage.py` is located)
or copy the 'sample.env' file

- On Windows:
```bash
copy sample.env .env
```
- On Linux/Mac:
```bash
cp sample.env .env
```
Edit your `.env` file. following the Guideline.
type `exit()` to exit the shell mode.

### 7. Apply Migrations

Run the following command to apply database migrations:
```bash
python manage.py migrate
```

### 8. Load Initial Data

Install pre-defined data using fixtures:
#### Data for Question and Choices only (no Votes)
```bash
python manage.py loaddata data/polls-v4.json 
```
#### Data for Votes
```bash
python manage.py loaddata data/votes-v4.json polls.vote    
```
#### Data For User data:
```bash
python manage.py loaddata data/users.json
```
#### Or load all data files in one command:
```bash
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```
