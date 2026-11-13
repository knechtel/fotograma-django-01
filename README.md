# Fotograma

Mini Instagram feito com Django e SQLite, com cadastro e login, feed de fotos, curtidas, comentários e perfis.

## Executar localmente

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Acesse http://127.0.0.1:8000/. As fotos enviadas ficam em `media/posts/` e os dados no banco `db.sqlite3`.
