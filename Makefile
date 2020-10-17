git:
	git add .
	git commit -m 'work'
	git push

heroku:
	git init
	git add . && git commit -m 'aa-backend'
	heroku git:remote -a ursas-backend
	git push heroku master