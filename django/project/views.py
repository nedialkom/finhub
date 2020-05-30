from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User


def base(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/finhub')
        else:
            return render(request, 'finhub/welcome.html')


def login(request):
    if request.method == 'POST': # Sign in button is pushed
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
        user = authenticate(request, username=request.POST.get('email', None), password=request.POST.get('password', None))
        if user is not None: # correct credentials
            auth_login(request, user)
            return HttpResponseRedirect(reverse('base'))
        else: # Wrong username or password
            context = {'error' : 'Wrong credentials!', 'email' : request.POST.get('username', None)}
            # Return an 'invalid login' error message.
            return auth_views.LoginView.as_view(template_name='login/login.html', extra_context = context)(request)
    else: # Get request -> load the page
        email = request.GET.get('email', None)
        if email is None:
            return render(request, 'login/login.html')
        else:
            return render(request, 'login/login.html', {'email': email})


def signup(request):
    if request.method == 'POST': # Sign up button is pressed
        username = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        #Form validation
        if (username is not None) and (password is not None) and (password2 is not None): #non-blank fields
            try:
                user = User.objects.get(username=username)
                # if successful => existing user; else will rise exception -> new user to be registered
                context = {'email': username, 'message': "Existing user, try with another e-mail or Log in"}
                return render(request, 'login/signup.html', context=context)
            except User.DoesNotExist:
                if password == password2: #equal passwords
                    user = User.objects.create_user(username, username, password)
                    user.save()
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('base'))
                else:#not equal passwords
                    context = {'email': username, 'message': 'Passwords are not the same, try again!'}
                    return render(request, 'login/signup.html', context=context)
        else:#some of the fields are blank
            context = {'email':username, 'message':'Try again'}
            return render(request, 'login/signup.html', context=context)
    else: # Get request -> load the page
        username = request.GET.get('email', None)
        if username is None:
            return render(request, 'login/signup.html')
        else:
            return render(request, 'login/signup.html', {'email':username})


def search(request):
    if request.method == 'POST':
        search_filed = request.POST.get('search', None)
        if search_filed is None or search_filed == '':
            return HttpResponseRedirect(reverse('base'))
        """Add your search code here"""
        # Do search and return the answer to the template
        text = 'Search result for {}:'.format(search_filed)
        search_result = 'This is your result'
        return render(request, 'finhub/search.html', {'text':text, 'search_result':search_result})
    else:
        return HttpResponseRedirect(reverse('base'))