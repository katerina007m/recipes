For running the project:
1. Clone the repository
2. Install the requirements
3. Make migrations if needed: python mysite/manage.py migrate
4. Run python mysite/manage.py runserver
5. Go to http://127.0.0.1:8000

The list of endpoints:

1) myauth/ login/ [name='login'] (POST) (the post form has "username" and "password")
2) myauth/ logout/ [name='logout'] (POST)
3) myauth/ about-me/ [name='about-me'] (GET)
4) myauth/ register/ [name='register'] (POST) (the post form has "username", "email", "first_name", "last_name", "password1", "password2",)
5) recipe_site/ (GET)
6) recipe_site/recipe/<pk>/ (GET)
7) recipe/add/ (GET)
8) recipe/add/ (POST) (the post form has "name", "description", "steps", "cook_time", "image", "categories")
9) recipe/edit/<pk>/ (POST) (the post form has "name", "description", "steps", "cook_time", "image", "categories" but they are optional)
10) recipe/delete/<pk>/ (POST)
