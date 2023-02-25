ECHO ----- Create virtual environment -----
python -m venv venv

ECHO ----- Activate virtual environment -----
call .\venv\Scripts\activate

ECHO ----- Install requirements.txt -----
pip install -r requirements.txt

ECHO ----- Execute script -----
python main_app.py

ECHO ----- Deactivate virtual environment -----
call deactivate
pause