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

## Getting your Google Oauth2 credential

Using your Google account, go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) to get your 
API credentials. 

<img align="center" width="600" src="https://github.com/matthew-ardi/item-catalog/blob/master/md-images/google-cred.JPG">
<br>

Make sure that you do the following set up in the restriction section of the credential configuration:

<img align="center" width="600" src="https://github.com/matthew-ardi/item-catalog/blob/master/md-images/google-restriction.JPG">


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

<br>

### Environment Variables


Variables | details
--- | ---
GOOGLE_CLIENT_ID | *< Your Google API client ID >*
GOOGLE_CLIENT_SECRET | *< Your Google API client secret >*

you will need to export the environment variables above while you are in the virtual environment
```
(venv)$ export GOOGLE_CLIENT_ID=<your client ID>
(venv)$ export GOOGLE_CLIENT_SECRET=<your client secret>
```

Then you should be able to run the web server. 
```
(venv)$ ./web.py
```
The web can be accessed at 
```
http://localhost:5000/dashboard/
```
## Notes about the web pages
___
You will need to log in using your Google Account to access the following features
1. Add new items.
2. Delete items.
3. Accessing API endpoints.


## Accessing API endpoints
There are 2 API endpoints without parameters that you can access through the browser urls:

API endpoints | details
--- | --- 
```http://localhost:5000/catalog/all_categories.json``` | return all categories metadata
```http://localhost:5000/catalog/all_items.json``` |return all items metadata

Additional 3 API endpoints with parameters:

**1. Get a Category**

```
http://localhost:5000/catalog/<category id>/category.json
```
Field | Type | Description
--- | --- | ---
```category id``` | integer | the id of the category

**2. Get an item**
```
http://localhost:5000/catalog/<categories id>/<item id>/item.json
```
Field | Type | Description
--- | --- | ---
```categories id``` | integer | the id of the category
```item id``` | integer | the id of the item

**3. Get all items in a category**
```
http://localhost:5000/catalog/<categories id>/all_items.json
```
Field | Type | Description
--- | --- | ---
```categories id``` | integer | the id of the category

## Resetting database
To reset the database to the original version, do the following steps in order
1. Remove the database
```
(venv)$ rm catalog_items.db
```
2. set up the new database
```
(venv)$ ./models.py
```
3. Populate database with the default categories
```
(venv)$ ./populate_db.py
```
> Be aware that you might encounter [Potential Problems](#potential-problems)

### Potential Problems
___
the following errors may occur:
```
/usr/bin/env: ‘python\r’: No such file or directory
```
if you received the error above while trying to run the programs, do the following step:

1. open the python file that you are trying to run using vim or vi
2. Administer the following command
```
:set ff=unix
```
3. exit the vim or vi editor
```
:wq
```
> you need to go through the steps above for every python file that you will execute

### Issues
Please feel free to post a tracking issue if you find any problem related to this repository.
