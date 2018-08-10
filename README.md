# Item Catalog
An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
You will need the following dependencies installed on your system to run the programs:
- Python 2.7
- Virtualenv
- Google account
- Google Oauth2 credential (Google API)

to install virtualenv:
```
sudo apt-get install virtualenv
```

## Initial Configuration
You will need to install all required dependencies that is recorded on ```requirements.txt```. To do so, Create your virtual environment:
```
virtualenv venv
```
> if you are running on vagrant, you need to use ```--always-copy``` flag

Then, enter the virtual environment:
```
source venv/bin/activate
```
Finally, install the dependencies in your virtual environment:
```
pip install -r requirements.txt
```
>make sure you are in the root directory of this project where ```requirements.txt``` exist

## Getting your Google API credential
