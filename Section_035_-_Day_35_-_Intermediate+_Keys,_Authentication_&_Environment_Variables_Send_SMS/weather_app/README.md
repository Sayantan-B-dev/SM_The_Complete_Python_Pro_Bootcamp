## Things to install:
- `pip install requests`
- `pip install python-dotenv`
- `pip install rich`
- `pip install twilio`

## Things to have in `.env` file:
- `API_ENDPOINT=http://api.weatherapi.com/v1/forecast.json`
- `API_KEY=****************`
- `TWILIO_PHONE_NUMBER=****************`
- `TWILIO_ACCOUNT_SID=****************`
- `TWILIO_AUTH_TOKEN=****************`
- `TWILIO_WHATSAPP_NUMBER=****************`
- `MY_PHONE_NUMBER=****************`
- `APP_MODE=cli | gui | sms`
- `SMS_MODE=whatsapp | sms`

## How to run:
- `APP_MODE=sms SMS_MODE=whatsapp python main.py`
- `APP_MODE=sms SMS_MODE=sms python main.py`
- `APP_MODE=gui python main.py`
- `APP_MODE=cli python main.py`

## Running without long command:
- go in .env file and set `APP_MODE` and `SMS_MODE` as you want
- then run `python main.py`
- `APP_MODE` can be set to `cli`, `gui`, `sms`
- `SMS_MODE` can be set to `whatsapp`, `sms`
