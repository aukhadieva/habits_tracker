python3 -m venv venv
source venv/bin/activate
pip3 poetry install
python manage.py migrate
python3 manage.py collectstatic --no-input
deactivate