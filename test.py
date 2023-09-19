from website.views import send_email

try:
    send_email()
    print("It worked!")
except Exception as e:
    print("It didn't work!")
    print(str(e)) 