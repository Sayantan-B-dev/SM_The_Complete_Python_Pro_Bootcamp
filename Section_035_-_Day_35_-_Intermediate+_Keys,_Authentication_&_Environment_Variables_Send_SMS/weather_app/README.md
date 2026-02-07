# Things to install:
- `pip install requests`
- `pip install python-dotenv`
- `pip install rich`
- `pip install twilio`

# Things to have in `.env` file:
- `API_ENDPOINT=http://api.weatherapi.com/v1/forecast.json`
- `API_KEY=****************`
- `TWILIO_PHONE_NUMBER=****************`
- `TWILIO_ACCOUNT_SID=****************`
- `TWILIO_AUTH_TOKEN=****************`
- `TWILIO_WHATSAPP_NUMBER=****************`
- `MY_PHONE_NUMBER=****************`
- `APP_MODE=cli | gui | sms`


# Running without defining in command:
- go in .env file and set `APP_MODE` and `SMS_MODE` as you want
<hr>

- then run `python -B main.py`
- `-B` is used to suppress the `.pyc` and not creating `.pyc` files all over the project
- `find . -type d -name "__pycache__" -exec rm -r {} +` on gitbash can be used to remove all `.pyc` files
<hr>

- `APP_MODE` can be set to `cli`, `gui`, `sms`
- `SMS_MODE` can be set to `whatsapp`, `sms`


# How to run with defining in command:
- `APP_MODE=sms SMS_MODE=whatsapp python -B main.py`
- `APP_MODE=sms SMS_MODE=sms python -B main.py`
- `APP_MODE=gui python -B main.py`
- `APP_MODE=cli python -B main.py`