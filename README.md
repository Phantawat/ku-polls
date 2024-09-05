## KU Polls: Online Survey Questions 
[![Django Tests](https://github.com/Phantawat/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/Phantawat/ku-polls/actions/workflows/django.yml)
[![Pylint](https://github.com/Phantawat/ku-polls/actions/workflows/pylint.yml/badge.svg)](https://github.com/Phantawat/ku-polls/actions/workflows/pylint.yml)


An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation

Follow these steps to set up and install the necessary dependencies for the project:
[Installation Guide](./Installation.md).

## Running the Application

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
2. Open the application in your browser at http://localhost:8000/ or 127.0.0.1:8000.
3. To stop the server, press `Ctrl+C` in the terminal.
4. When you're done, deactivate the virtual environment:
   ```bash
   deactivate
   ```
The KU Polls application is now set up and running! You should see available polls on the index page.

## Running Tests
To run the application's test suite, use the following command:

```bash
python manage.py test polls
```


## Demo User Accounts

Sample polls and users data are included. There are 4 demo accounts:

| Username | Password |
|:---------|---------:|
|  demo1   | hackme11 |
|  demo2   | hackme22 |
|  demo3   | hackme33 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki).

- [Vision Statement](../../wiki/Vision-and-Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../ku-polls/wiki/Project-Plan)
- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)
- [Domain models](../../wiki/Domain-model)
