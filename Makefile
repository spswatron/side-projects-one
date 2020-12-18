git:
	git add .
	git commit -m 'work'
	git push

heroku:
	git init
	git add . && git commit -m 'aa-backend'
	heroku git:remote -a ursas-backend
	git push heroku master

flask:
	 /Users/ashleychang/PycharmProjects/flaskServer/venv/bin/python -m flask run

pdb:
	 /Users/ashleychang/PycharmProjects/flaskServer/venv/bin/python3 -m pdb app.py

migrate:
	/Users/ashleychang/PycharmProjects/flaskServer/venv/bin/python manage.py db migrate

init:
	/Users/ashleychang/PycharmProjects/flaskServer/venv/bin/python manage.py db init
