from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Create your views here.
# def registration(request):
#     title = "Registration"
#     if request.method == 'POST':
#         form = registrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.save()
#             password = form.cleaned_data.get('password1')
#             # login user after signing up
#             user = authenticate(username= user.username, password = password)
#             # login(request, user)
#             return redirect('login')
#         else:
#             msg = form.errors
#             messages.info(request, form.errors)
#             return redirect('register')
#     else:
#         form = registrationForm()
#         context = {'form': form, 'title': title}
#         return render(request, 'authentication/register.html', context=context)

# def userLogin(request):
#     title = "Login"
#     form = loginForm(request.POST)
#     context = {
#         'form': form,
#         'title': title,
#         }
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username = username, password = password)
#             login(request, user)
#             return redirect('home')
#         else:
#             print(form.errors)
#             messages.success(request, f"Accoutn doesn't exit")
#             msg = form.errors
#             messages.info(request, form.errors)
#                 # return redirect('register')
#             return redirect('login')
#     else:
#         return render(request, 'authentication/login.html', context=context)

# def logoutUser(request):
#     logout(request)
#     # messages.info(request, "Logged out successfully!")
#     return redirect('login')


def userLogin(request):
	if request.method == "GET":
		return render(request, "authentication/login.html")
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('home')
			else:
				return render(request, "authentication/login.html", context={"error": "User is not active"})
		else:
			return render(request, "authentication/login.html", context={"error": "Login credentials are incorrect"})


def logoutUser(request):
	logout(request)
	return redirect('login')


def registration(request):
	if request.method == "GET":
		return render(request, "authentication/register.html")
	if request.method == "POST":
		username = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if password1 != password2:
			return render(request, "authentication/register.html", context={'error': "Your passwords do not match. Please fill the form again."})

		if User.objects.filter(username=username):
			return render(request, "authentication/register.html", context={'error': "Username is already taken. Please choose another username."})

		new_user = User()
		new_user.username = username
		new_user.first_name = fname
		new_user.last_name = lname
		new_user.email = email
		new_user.set_password(password1)
		new_user.is_active = True
		new_user.save()

		return redirect('login')
