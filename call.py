from twilio.rest import Client


def call_to_user(phone_code,to_number):
    try:
        # Your Twilio account SID and auth token
        account_sid = 'AC75f288908ba8728dacaf1eb2718d5ef1'
        auth_token = 'a9da8c23973211bcd196b03ccc7514aa'

        # Create a Twilio client with your account SID and auth token
        client = Client(account_sid, auth_token)

        # The phone number to call from (in E.164 format and must be a Twilio verified phone number)
        from_number = '+15074364355'

        # Make the phone call
        call = client.calls.create(
            to=str(phone_code)+str(to_number),
            from_=from_number,
            url='http://demo.twilio.com/docs/voice.xml'  # TwiML instructions for the call
            )

        # Print the call SID
        print(call.sid)
    except:
        call = "connection_error"
        
    return call
