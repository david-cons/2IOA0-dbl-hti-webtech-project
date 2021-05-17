# 2IOA0-dbl-hti-webtech-project
year 1 dbl project

## To run on your computer:
0. Open an empty directory with an IDE (VS Code)
1. Install python and Django: https://docs.djangoproject.com/en/3.2/intro/install/
2. Install git: https://git-scm.com/download/win
3. Clone the project: `git clone https://github.com/david-cons/2IOA0-dbl-hti-webtech-project`
4. Go to the source directory: `cd 2IOA0-dbl-hti-webtech-project/source`
5. Run the server: `python manage.py runserver`
6. Open a browser and go to port 8000: http://127.0.0.1:8000/

## To work with scss in the frontend:
0. Never change files in the 'build' directory, they will be overwritten when others compile their assets.
1. Install node: https://nodejs.org/en/download/
2. Go to static: `cd static`
3. Install node packages: `npm install`
4. After making changes to .scss files build the assest: `npm run build`