import os
import requests
from django.shortcuts import render
# Create your views here.
from django.http import Http404
from django.shortcuts import render
from dotenv import load_dotenv
from django.shortcuts import redirect



load_dotenv()

# landing page
def laodLandingPage(request):
    return render(request, "index.html")

#contact us
def send_email(request):
    from_user = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    print(from_user, email, message)
    print(os.getenv("MAILGUN_SANDBOX_ID"),os.getenv("MAILGUN_KEY"))
    res = requests.post(
		"https://api.mailgun.net/v3/{}/messages".format(os.getenv("MAILGUN_SANDBOX_ID")),
        auth=("api", os.getenv("MAILGUN_KEY")),
        data={"from": email,
            "to": ["hari._.s@icloud.com"],
            "subject": 'Excited user have some qureys '+from_user,
            "text": message})
    print(res.text)
    return redirect('server:laodLandingPage')
    
    # return render(request, "index.html")
