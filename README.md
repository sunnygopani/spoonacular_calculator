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
	<br />$ git clone https://github.com/sunnygopani/spoonacular_calculator.git
* Change directory to the git project that was cloned.
	<br />$ cd spoonacular_calculator
	
* Create a .env file to store the Api Key
	<br />And enter the following in the file
	<br />SPOONACULAR_API_KEY = "<YOUR_API_KEY>"
	<br />OR
	<br />echo SPOONACULAR_API_KEY = "<YOUR_API_KEY>"  > .env
	
* Create and activate a virtual environment.
	<br />$ python -m venv svenv
	<br />$ svenv\Scripts\activate.bat
	
* Install and upgrade python pip for installing the required modules.
	<br />$ python -m pip install --upgrade pip

* Install all the dependencies from requirements.txt
	<br />$ pip install -r requirements.txt

* Install and build from the setup.py file
	<br />$ python setup.py install
	<br />$ python setup.py develop

* Run the project either directly using:
	<br />$ spoonacular_script
	<br />or by using python command
	<br />$ py app.py
	
* Once done you may deactivate the virtual environment using,
	<br />$ deactivate


Running directory via shell script
==================================

Steps:

1. Use the below command
	<br />$ run_spoonacular

2. Update the API Key in the .env file with your Spoonacular Api Key

3. Activate the virtual environment:
	<br />$ svenv\Scripts\activate.bat
	
4. Run the project either directly using:
	<br />$ spoonacular_script
	<br />or by using python command
	<br />$ py app.py
