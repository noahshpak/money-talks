# Money Talks

## Usage

I would recommend setting up a virtual environment for this but it's not totally necessary

`$ pip install -r requirements.txt`

## Get your OATH Token from Venmo
* Go to Chrome
* login to Venmo
* open dev tools
* go to network, refrech, filter for api and find the api feed request. When you hover over it, link should look like https://venmo.com/api/v5/users/{user_id}/feed  
    * right click > Copy Request Headers > paste these into a file called requestheaders.txt in this directory

# Run it

`$ python process_api.py `
