** Assumptions **
1. I assume that you have added your ssh-keys to your github account: `https://github.com/settings/keys`. In case you don't know how to do it, refer to this page: `https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh`
2. Node.js v10.20.1 (I prefer nvm as a version manager -- you can install multiple versions using it.). However, this version requirement is subject to change.

** Installation **
1. Clone the project using ssh url: `git@github.com:jumasheff/codomodo.git`
2. Go to the project directory: `cd codomodo`
3. Install JavaScript dependencies: `npm install`
4. Create a virtual environment called `env`: `python3 -m venv env`
5. Activate the virtual environment: `source env/bin/activate`
6. Install Python dependencies: `pip install -r requirements/requirements_dev.txt`
7. Open 2 terminal tabs/windows (whatever you prefer)
8. In the 1st terminal (in the project directory) activate the virtual environment (in case it's not activated) and create a superuser: `./manage.py createsuperuser` (fill in all the fields)
9. In the same terminal load the fixtures (dummy data): `./manage.py loaddata fixtures/courses.json`
10. In the same terminal run the Django server: `./manage.py runserver`
11. In the 2nd terminal issue the following command (which will run a watcher.js whose job is to rebuild the project each time it detects some changes under the frontend/src folder): `npm start`
12. Now you can open your favorite editor and start writing your awesome code!

Happy coding!

** How we git **
Each task should be done within its own branch. For this, we keep our local master clean and synced. Let's walk throug an example. Imagine you are given a task related to creating a new page for editing an exercise. Your steps should be as follows:
1. Make sure you are on the `master` branch. When you issue the following command there should be an asterisk before the name of the branch `* master`: `git branch`
2. Make sure the branch is clean. After issue the following command you should see the text as follows: `git status`
```
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```
2.1. If it's not up to date, pull updates: `git pull origin master`
3. Create a new branch: `git checkout -b create-exercise-editing-page`
4. Write your code. Commit as often as possible. Educate yourself: `https://sethrobertson.github.io/GitBestPractices/`
5. After you are done with the task, create a Pull Request (PR):
5.1. Push your code to the repository, to a new remote branch with an identical name: `git push origin create-exercise-editing-page`
5.2. Go to the repository and refresh the page. You should see a button called `Create a pull request`. Click on it and fill the form –– insert the task's URL to the text field and create a pull request.
5.3. Send your PR's URL to a person who is responsible for the code (team lead?).
5.4. Do not merge until the PR is approved. When it's approved, make sure it has no conflicts.
6. In case you have a conflicts (the same file or set of files was edited by you and your peer), in your machine switch to `master` (please, make sure that you are really on `master`), pull updates (`git pull origin master`) and go to your branch: `git checkout create-exercise-editing-page` and rebase from master: `git rebase master`.
7. Resolve conflicts. VSCode has a good tool, Github itself has its own one. A good video on the topic: `https://www.youtube.com/watch?v=JtIX3HJKwfo`. If you are resloving the conflict locally, edit the files, `git add` the resolved files, don't forget to `git rebase --continue` etc. Talk to your team lead in case you have questions.
8. Push the resolved code to your remote branch: `git push -f origin create-exercise-editing-page`. See `-f`? It means `force`, that is, you should force-push to your branch, because your local one's git history is different than the remote one.
9. Make sure that after rebasing the code still works.
10. If everything looks good, merge your branch to master.
11. Whoot!