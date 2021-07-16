**Assumptions**

1. I assume that you have added your ssh-keys to your github account: `https://github.com/settings/keys`. In case you don't know how to do it, refer to this page: `https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh`
2. Node.js v14.16.0 (I prefer nvm as a version manager -- you can install multiple versions using it.). However, this version requirement is subject to change.
3. Python v3.6. or above

**Installation**

0. Clone the project using ssh url: `git@github.com:jumasheff/codomodo.git`
1. Create .env file from the provided template: `cp env_template .env`
2. Go to the project directory: `cd codomodo`
3. Install JavaScript dependencies: `npm install`
4. Create a virtual environment called `env`: `python3 -m venv env`
5. Activate the virtual environment: `source env/bin/activate`
6. Upgrade pip: `pip install --upgrade pip`
7. Install Python dependencies: `pip install -r requirements/requirements_dev.txt`
8. Open two terminal tabs/windows (whatever you prefer)
9. In the 1st terminal (in the project directory) activate the virtual environment (in case it's not activated) and install migrations: `./manage.py migrate`
10. Create a superuser: `./manage.py createsuperuser` (fill in all the fields)
11. In the same terminal load the fixtures (dummy data): `./manage.py loaddata fixtures/courses.json`
12. In the same terminal run the Django server: `./manage.py runserver`
13. In the 2nd terminal issue the following command (which will run a watcher.js whose job is to rebuild the project each time it detects some changes under the frontend/src folder): `npm start`
14. Now you can open your favorite editor and start writing your awesome code!

Happy coding!

**Quirks**

If you are having issues with `cffi`, try to upgrade pip (make sure env is activated): `pip install --upgrade pip`
Make sure you have a branch off of a fresh master.
If you already had the project installed, you may have issues caused by Spirit (forum) installation. Here are the steps for solving the issues:
1. Install Python dependencies: `pip install -r requirements/requirements_dev.txt`
2. Migrate: ./manage.py migrate 
3. Initiate Spirit installation: ./manage.py spiritinstall
4. Migrate once again: ./manage.py migrate 
5. If you haven't yet, create a superuser: `./manage.py createsuperuser` (fill in all the fields)
6. If you haven't yet, load the fixtures (dummy data): `./manage.py loaddata fixtures/courses.json`

**How we git**

Each task should be done within its own branch. For this, we keep our local master clean and synced. Let's walk throug an example. Imagine you are given a task related to creating a new page for editing an exercise. Your steps should be as follows:
1. Make sure you are on the `master` branch. When you issue the following command there should be an asterisk before the name of the branch `* master`: `git branch`
2. Make sure the branch is clean. After issue the following command you should see the text as follows: `git status`
    1. If it's not up to date, pull updates: `git pull origin master`
```
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```
3. Create a new branch: `git checkout -b create-exercise-editing-page`
4. Write your code. Commit as often as possible. Educate yourself: `https://sethrobertson.github.io/GitBestPractices/`
5. After you are done with the task, create a Pull Request (PR):
    1. Push your code to the repository, to a new remote branch with an identical name: `git push origin create-exercise-editing-page`
    2. Go to the repository and refresh the page. You should see a button called `Create a pull request`. Click on it and fill the form –– insert the task's URL to the text field and create a pull request.
    3. Send your PR's URL to a person who is responsible for the code (team lead?).
    4. Do not merge until the PR is approved. When it's approved, make sure it has no conflicts.
6. In case you have a conflicts (the same file or set of files was edited by you and your peer), in your machine switch to `master` (please, make sure that you are really on `master`), pull updates (`git pull origin master`) and go to your branch: `git checkout create-exercise-editing-page` and rebase from master: `git rebase master`.
7. Resolve conflicts. VSCode has a good tool, Github itself has its own one. A good video on the topic: `https://www.youtube.com/watch?v=JtIX3HJKwfo`. If you are resloving the conflict locally, edit the files, `git add` the resolved files, don't forget to `git rebase --continue` etc. Talk to your team lead in case you have questions.
8. Push the resolved code to your remote branch: `git push -f origin create-exercise-editing-page`. See `-f`? It means `force`, that is, you should force-push to your branch, because your local one's git history is different than the remote one.
9. Make sure that after rebasing the code still works.
10. If everything looks good, merge your branch to master.
11. Whoot!


### Creating a user via JWT

JWT payload should have this data:
```json
{
  "first_name": "Murat",
  "last_name": "Jumash",
  "username": "muratjumash",
  "email": "murat.some.email@gmail.com",
  "password": "$2y$10$s8yTdfhfYePKL7DoR4JZ0efYyPNHTPXak61UfaIpHdUM/GNoEIMlC"
}
```

Please, refer to this page to get info about JWT: https://jwt.io

We set up bcrypt with 10 round in order to be able to accept users created in Laravel.

That is, a user's data (which was created in any Laravel website) can be encrypted into a JWT using the secret key specified here, will be `created` in this website. That means, they will be able to use their credentials.

For that to happen, a friendly website should use our JWT_SECRET to pass their user data to our site:
```
https://codomodo.com/?token=jwt_token_with_payload
```
