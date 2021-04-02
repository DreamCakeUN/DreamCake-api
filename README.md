# DreamCake-api

## API

 - Django
 - Djangorestframework
 - allauth
 - django-sslserver 
   - `python manage.py runsslserver`

## DB

- ### host

    - http://z4yross.hopto.org:49152/

- ### Nombre

    - DreamCake

 - ### Credenciales

	-	|USER      |PSWD       |
		|----------|-----------|
		| postgres | raspberry |

## CUSTOM URLS

| URL                  | VIEW                            |
|----------------------|---------------------------------|
| /stats/interactions/ | statistics_api.views.inte_count |
| /stats/posts/        | statistics_api.views.post_count |
| /stats/users/        | statistics_api.views.user_count |
