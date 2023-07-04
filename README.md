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
Go to `App Settings` > `Create new client secret`. You should see a long string.

### Store this info

You should save your Tink credentials now. You will need both the client ID and the client secret. Create a file and call it `.env`. Your file should look like this (no spaces between the equal signs):

```
TINK_CLIENT_ID=yourtinkid
TINK_CLIENT_SECRET=yourtinksecret
```

### Start integrating with your banks

First of all, create a user in your Tink app:

```
tinksync --create
```

Then, start connecting your banks.
```
tinksync --connect
```

This will produce a link as an output. Follow it, and follow the instructions to connect your first bank.

Have more banks? That's perfect, that's why Tink (and this app) were made. Just re-run `tinksync --connect` and follow the instructions again to connect to another bank. (Do not reuse the same link as the first time). Repeat the operation as many times as you need to connect to all your bank accounts. Easy peasy 🙃.

### Check your integration

Run the following command to see all the accounts you have successfully connected.

```
tinksync --accounts
```

```
Example:
>> Monzo > 1234.56 GBP > OK
>> Amex Gold - 1001 > -200.00 GBP > OK
>> Revolut EUR > 32.10 EUR > OK
```


If you don't see one or a few, no worries. Just wait a few mins and retry running `tinksync --accounts`, the connection might take a few minutes to be fully established. 

To see your latest transactions (across all your accounts) run:
```
tinksync --transactions
```

```
Example:
>> Japan Centre Ceramics Sushi > 2023-07-01 > -12.75 GBP 
>> TfL Travel Charge > 2023-07-01 > -8.1 GBP 
>> Mm Re Cl Cos Grl > 2023-06-30 > -27.3 GBP 
>> Mm Re Cl Cos Grl > 2023-06-30 > -5.8 GBP
```