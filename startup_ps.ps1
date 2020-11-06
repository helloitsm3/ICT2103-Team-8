venv\Scripts\activate.ps1
$env:FLASK_APP="main.py" 
$env:FLASK_ENV="development"
python -m flask run