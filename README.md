# CS50 Web Programming Projects

This branch contains a collection of projects completed as part of Harvard's CS50 Web Programming with Python and JavaScript course. The projects cover a range of web development concepts, including frontend design, backend logic, database integration, authentication, user interaction, and application architecture.

Each project is self-contained and demonstrates a different aspect of modern web development.

## Projects Included

### 1. SEARCH [Search](https://cs50.harvard.edu/web/projects/0/search/)

A front-end project inspired by Google-style search pages, including:
- basic search page
- image search page
- advanced search page

This project focuses on HTML and CSS layout design and static page behavior.

### 2. COMMERCE [Commerce]([https://cs50.harvard.edu/web/projects/0/search/](https://cs50.harvard.edu/web/projects/2/commerce/)
A Django-based auction marketplace similar to eBay, featuring:
- user registration and login
- creating listings
- bidding on items
- watchlist functionality
- categories and listing pages
- comments and listing management

This project demonstrates backend development, database modeling, authentication, and Django templates.

### 3. MAIL [MAIL](https://cs50.harvard.edu/web/projects/3/mail/)
A simple email client built with Django and JavaScript, including:
- inbox
- sent mail
- archive functionality
- sending emails
- viewing message details
- single-page interactions without full page reloads

This project focuses on building dynamic user interfaces and client-side behavior.

### 4. NETWORK [NETWORK](https://cs50.harvard.edu/web/projects/4/network/)
A social networking web app inspired by Twitter/X, featuring:
- user accounts
- creating posts
- viewing all posts
- viewing posts from followed users
- user profile interactions
- follow system

This project covers Django models, user relationships, and interactive front-end behavior.

### 5. WIKI [WIKI](https://cs50.harvard.edu/web/projects/1/wiki/)
An encyclopedia-style web app built with Django, featuring:
- entry listing
- search functionality
- viewing encyclopedia entries
- creating new pages
- editing existing entries
- Markdown-based content rendering

This project highlights backend routing, templates, and content management.

---

## Tech Stack

These projects use a combination of:
- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite

---

## Folder Structure

- `SEARCH/` — static HTML/CSS search interface
- `COMMERCE/` — Django auction website
- `MAIL/` — Django + JavaScript mail app
- `NETWORK/` — Django social network
- `WIKI/` — Django encyclopedia app

---

## How to Run

### Static project
For the `SEARCH` project, you can open the HTML files directly in a browser, or run:

```bash
cd SEARCH
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

### Django projects
Each Django project has its own `manage.py` file. Run them with:

```bash
cd COMMERCE
python manage.py runserver
```

```bash
cd MAIL
python manage.py runserver
```

```bash
cd NETWORK
python manage.py runserver
```

```bash
cd WIKI
python manage.py runserver
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8000
```

If needed, first initialize the database:

```bash
python manage.py migrate
```

---

## Notes

- These projects were created as part of CS50's Web Programming course.
- Each project is meant to demonstrate different web development concepts and project patterns.
- Some projects are static front-end work, while others are full-stack Django applications.

---

## Summary

This repository showcases a range of web development skills, from building static pages to creating full database-backed web apps with Python and Django. It is a strong portfolio of CS50 Web Programming work and demonstrates practical experience with both frontend and backend development.
