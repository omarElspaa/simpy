set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
pytho manage.py migrate