Github Language
------------
This is a small command-line utility that allows you to determine a user's favourite language based on their github commits.


Installation
-----------

1. Install dependencies by running `pip install -r requirements.txt`

2. Make the file executable `chmod +x github_language.py`

3. Complete github_language.py with with your username and either provide your password, or generate an access token at 
  https://github.com/settings/applications#personal-access-tokens

4. Run tests with `python test_github_language.py`


Usage
-----

Run as `./github_language.py username`

Note: This will run fine without your user token, but will soon hit a rate limit

