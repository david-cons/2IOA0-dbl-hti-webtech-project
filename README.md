# 2IOA0-dbl-hti-webtech-project
year 1 dbl project

## To run on your computer:
0. Open a directory with an IDE (VS Code)
1. Install git: https://git-scm.com/download/win
2. Clone the project: `git clone https://github.com/david-cons/2IOA0-dbl-hti-webtech-project`
3. Go to the directory: `cd 2IOA0-dbl-hti-webtech-project/source`
4. Install Python
5. Install pipenv to use a sort of virtual environment `pip install pipenv` (you may need to add it to your PATH)
6. Install libaries `pipenv install`
7. Run the server: `python manage.py runserver`
8. Open a browser and go to port 8000: http://127.0.0.1:8000/

## To work with scss in the frontend:
0. Never change files in the 'build' directory, they will be overwritten when others compile their assets.
1. Install node: https://nodejs.org/en/download/
2. Go to static: `cd static`
3. Install node packages: `npm install`
4. After making changes to .scss files build the assest: `npm run build`
