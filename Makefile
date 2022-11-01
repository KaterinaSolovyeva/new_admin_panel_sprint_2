setup:
	docker-compose exec service python manage.py makemigrations
	docker-compose exec service python manage.py migrate
	docker-compose exec service python manage.py collectstatic --no-input

admin:
	docker-compose exec service python manage.py createsuperuser

load_data:
	docker-compose exec service bash -c "cd sqlite_to_postgres && python load_data.py"