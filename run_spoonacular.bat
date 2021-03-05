git clone https://github.com/sunnygopani/spoonacular_calculator.git
cd spoonacular_calculator
echo SPOONACULAR_API_KEY = "<YOUR_API_KEY>"  > .env
python -m venv svenv
svenv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python setup.py install
python setup.py develop