# Fleet Management

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

Create local_config.py file in base directory and include: SECRET_KEY, SQLALCHEMY_DATABASE_URI

Create db.
```bash
python manage.py db migrate
python manage.py db upgrade
```

Run server.
```bash
python main.py
```