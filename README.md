### Job Pale Mtaa

#### Setup

- Create and Activate a Virtual Environment using `pipenv shell`
- Install the dependencies using `pipenv install`
- All the requirements are catered for in the `Pipfile` and `Pipfile.lock` files.

- Initializa DB by making migrations and migrating them using: 

    `python manage.py makemigrations`

    `python manage.py migrate`

- Create an admin instance using `python manage.py createsuperuser`