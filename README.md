============
Spooonacular
============

This tool finds recipes for ingredients and computes a total estimate on the cost for the missing ingredients for the recipes you like::


Build information
=================

Prerequisites:

* Python > 3.0 
* GitHub

Steps to create the build:

* Open a terminal

* Clone the project using git clone command
	$ git clone https://github.com/sunnygopani/spoonacular_calculator.git
* Change directory to the git project that was cloned.
	$ cd spoonacular_calculator
	
* Create a .env file to store the Api Key
	And enter the following in the file
	SPOONACULAR_API_KEY = "<YOUR_API_KEY>"
	OR
	echo SPOONACULAR_API_KEY = "<YOUR_API_KEY>"  > .env
	
* Create and activate a virtual environment.
	$ python -m venv svenv
	$ svenv\Scripts\activate.bat
	
* Install and upgrade python pip for installing the required modules.
	$ python -m pip install --upgrade pip

* Install all the dependencies from requirements.txt
	$ pip install -r requirements.txt

* Install and build from the setup.py file
	$ python setup.py install
	$ python setup.py develop

* Run the project either directly using:
	$ spoonacular_script
	or by using python command
	$ py app.py
	
* Once done you may deactivate the virtual environment using,
	$ deactivate


Running directory via shell script
==================================

Steps:

1. Use the below command
	$ run_spoonacular

2. Update the API Key in the .env file with your Spoonacular Api Key

3. Activate the virtual environment:
	$ svenv\Scripts\activate.bat
	
4. Run the project either directly using:
	$ spoonacular_script
	or by using python command
	$ py app.py
