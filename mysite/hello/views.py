from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.

def cookieSet(request):
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    resp = HttpResponse('<p>Eat this cookie :)</p><p>view count='+str(visits)+' times </p>' +'<p> 69b7411e </p>')
    resp.set_cookie('Anor_Londo', random.randint(10000,9999999999))
    resp.set_cookie('dj4e_cookie', '69b7411e', max_age=1000)
    return resp
