# Task Manager

A small task/ticket manager built around Django, Jinja server-rendered HTML, and
Tailwind CSS. Page navigation and form submissions use normal HTTP requests;
the application does not use HTMX, Alpine.js, or a client-side JavaScript
framework.

## Technology

- Python 3.14 or newer
- Django 6.1
- Jinja 3.1+
- SQLite for local data
- Tailwind CSS 3, built locally with npm
- `uv` for Python dependencies and virtual environments

## Get started

Install Python 3.14+, [`uv`](https://docs.astral.sh/uv/), and Node.js/npm.
From the repository root:

```sh
# Install the project and its development dependency group from uv.lock.
uv sync

# Install the pinned JavaScript build dependencies from package-lock.json.
npm ci

# Create local configuration.
cp .env.example .env
```

Set `SECRET_KEY` in `.env` to a private random value. For example, generate one
with:

```sh
uv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the generated value into `.env`. Keep `.env` private; it is ignored by
Git. `.env.example` is only a template and should not contain real secrets.
`DEBUG` should be `True` for local development. Set `ALLOWED_HOSTS` to
comma-separated host names, for example `localhost,127.0.0.1`.

Initialize the local database and create an administrator account:

```sh
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

Build the CSS and start Django:

```sh
npm run build:css
uv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>. The Django admin is at
<http://127.0.0.1:8000/admin/>.

## Everyday commands

Run these from the repository root.

### Tailwind CSS

```sh
# One-time build; writes the stylesheet served by Django.
npm run build:css

# Keep the stylesheet up to date while editing templates (use a second terminal).
npm run watch:css
```

Tailwind reads class names from application and project HTML/Jinja templates
using `tailwind.config.js`. The input file is `static/css/input.css`; the
generated, locally served file is `static/css/output.css`. Rebuild after
changing templates if the watcher is not running.

### Django

```sh
# Start the development server.
uv run python manage.py runserver

# Apply database migrations.
uv run python manage.py migrate

# Create an administrator account.
# Note: Remember to assign role from the admin panel.
uv run python manage.py createsuperuser

# Run all Django tests.
uv run python manage.py test

# Run only a particular app's tests.
uv run python manage.py test tickets
uv run python manage.py test accounts

# Check Django configuration.
uv run python manage.py check

# Create migrations after changing models, then apply them.
uv run python manage.py makemigrations
uv run python manage.py migrate

# Custom test users creation script for various scenarios.
uv run python manage.py create_test_users
```

### Python lint

Ruff is part of the `uv` development dependency group:

```sh
uv run ruff check accounts config tickets
```

### Python dependencies

Add or remove Python dependencies with `uv`, not `pip`. For example:

```sh
uv add package-name
uv add --dev development-tool
uv remove package-name
uv sync
```

`uv.lock` records resolved versions. Keep it in sync with `pyproject.toml` and
commit both when dependencies change:

```sh
uv lock
uv lock --check
```

## Application behavior

### Accounts

- Sign up at `/accounts/signup/`.
- Log in at `/accounts/login/`.
- Log out using the POST form in the page header.
- Users are based on the project’s custom `accounts.User` model, which adds a
  role (`admin`, `manager`, or `member`) and creation/update timestamps.
- After login or signup, users go to the ticket list unless login supplied a
  valid local `next` URL. External redirect URLs are not accepted.
- Custom test users creation script `accounts/management/commands/create_test_users.py`
  for testing various user type scenarios to be invoked from django's `manage.py`.

### Tickets

- The ticket list is at `/` and is restricted to authenticated users. It shows
  tickets assigned to the current user.
- Create a ticket at `/tickets/create/`.
- View a ticket at `/tickets/<id>/`.
- Edit a ticket at `/tickets/<id>/update/`.
- Change its status by submitting the status form.
- Delete a ticket by opening `/tickets/<id>/delete/` and confirming with a
  POST. A GET request only displays the confirmation page.
- Ticket statuses are `To-Do`, `In Progress`, `On hold`, and `Completed`.
- Ticket creation, editing, status updates, and deletion are permission
  protected. Django permissions are named `add_supportticket`,
  `change_supportticket`, and `delete_supportticket` in the `tickets` app.
  Use Django admin or groups to grant the required permissions to users.

All page changes use standard Django views, full-page responses, regular HTML
forms, CSRF tokens, and redirects. No endpoint depends on a special request
header or partial-page response.

## Frontend and templates

- `templates/base.html` is the shared page layout and loads
  `static/css/output.css`.
- Project-level account templates are in `templates/accounts/` and
  `templates/registration/`.
- Ticket page templates are in `tickets/jinja2/tickets/`, including shared
  row markup under `tickets/jinja2/tickets/partials/`.
- The Jinja environment is configured in `config/jinja2.py`. It makes Django's
  `url()` reverse lookup and `static()` helper available to templates and
  receives Django's request, auth, and messages context processors.
- Django's built-in template backend remains configured for Django-provided
  templates such as the admin.
- Tailwind uses its default utility classes and scans the project HTML/Jinja
  templates. There is no runtime Tailwind CDN dependency.
- No JavaScript is currently required for the documented application flows.

When adding a template, use the Jinja syntax already used by application pages,
keep form submissions as ordinary `method="post"` forms with CSRF tokens, and
run `npm run build:css` so Tailwind includes any new utility classes.

## Backend layout

- `config/` contains Django settings, root URL configuration, WSGI/ASGI entry
  points, and Jinja configuration.
- `accounts/` contains the custom user model, signup/login/logout forms and
  views, URLs, and tests.
- `tickets/` contains the ticket model, forms, views, URLs, templates,
  migrations, admin registration, and tests.
- `templates/` contains shared and project-level templates.
- `static/css/input.css` is the Tailwind input; `static/css/output.css` is the
  generated stylesheet served by Django.
- `pyproject.toml` declares Python dependencies and project settings;
  `uv.lock` pins the Python environment.
- `package.json` and `package-lock.json` declare and pin the Tailwind build
  toolchain.

The default database is `db.sqlite3` at the repository root. It is local
development data and is ignored by Git.

## Tests

The test suite uses Django's built-in test runner and a temporary test
database. It covers server-rendered ticket and authentication pages, ticket
creation/editing/status/deletion, login redirects, and POST-only logout.
Run the complete suite with:

```sh
uv run python manage.py test
```

## Deployment note

The development server is for local use only. Before deployment, use a
production WSGI/ASGI server, set a strong private `SECRET_KEY`, set
`DEBUG=False`, configure `ALLOWED_HOSTS`, and collect/serve static assets using
the deployment platform's static-file setup:

```sh
uv run python manage.py collectstatic
```
