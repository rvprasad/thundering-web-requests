## Execution

Execute the following commands after installing Python 3, uWSGI, and Flask.

- `uwsgi -p 4 --http 0.0.0.0:1234 --module server:app`
