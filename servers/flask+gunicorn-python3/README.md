## Execution

Execute the following commands after installing Python 3, Gunicorn, and Flask.

- `gunicorn -w 4 -b 0.0.0.0:1234 server:app`
