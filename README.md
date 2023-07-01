# tinksync

## How to

### Clone this repo
You may want to activate a virtual environment. Run:
```
python -m venv venv
source venv/bin/activate
```
Then install the package:
```
pip install .
```

### Create an account with Tink
Quite straightforward. Here's the link [link](https://console.tink.com/signup) for you.

### Create a production app with Tink
Navigate to the Tink console. Create a new production app and give it an exciting name, like `personal-budget`. Select the app type to be `production`. These scripts and API integrations were tested in the sandbox first for you 😘.

### Create an account secret
Go to `App Settings` > `Create new client secret`. You should see a long string. Store this info as described below. 

### Store this info

You should save your Tink credentials now. You will need both the client ID and the client secret. Create a file and call it `.env`. Your file should look like this (no spaces between the equal signs):

```
TINK_CLIENT_ID=yourtinkid
TINK_CLIENT_SECRET=yourtinksecret
```

### Start integrating with your banks

First of all, create a user in your Tink app:

```
python -m tinksync.cli --create
```

Then, start connecting your banks.