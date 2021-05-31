from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

# # from gmail.forms import UserAdminCreationForm
#
#
# # def register(req):
# #     form = UserAdminCreationForm()
# #     if req.method == 'POST':
# #         form = UserAdminCreationForm(req.POST)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('register')
# #     return render(req, 'gmail/register.html', {'form': form})
#
#
# # Create your views here.
#
# def login_request(request):
#     return render(request, 'gmail/login.html')
#
#
# def login_validate(request):
#     email = request.POST['email']
#     # username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, email=email, password=password)
#     if user is not None:
#         login(request, user)
#         if Employee.objects.filter(user=user).exists():
#             return HttpResponseRedirect('/office/details/')
#         else:
#             return render(request, 'office/login.html', {'error': 'Invalid username or password'})
#
#     else:
#         return render(request, 'office/login.html', {'error': 'Invalid username or password'})
#
#
# def main(request):
#     return render(request,'gmail/main.html')
from account import settings
from gmail.forms import GmailForm
from gmail.models import MyUser, Gmail, Registration


def main(request):
    """ index page were we can have login view"""
    return render(request, 'gmail/index.html')


def registration(request):
    """ registration page """
    return render(request, 'gmail/register.html')


def save_register(request):
    """saving details """
    if request.method == "POST":
        MyUser.objects.create_user(email=request.POST['email'], password=request.POST['password'])
        Gmail.objects.create(phone=request.POST['mobile'])
        return render(request, 'gmail/index.html')
    else:
        return render(request, 'gmail/index.html', {'error': 'you are not eigible for this job'})


def login_request(request):
    """ save login details"""

    username = request.POST['username']
    password = request.POST['password']
    # email = request.POST['email']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render('gmail/email.html')


    else:
        return render(request, 'gmail/index.html', {'error': 'Invalid username or password'})


def compose(request):
    form = GmailForm
    return render(request, 'gmail/compose.html', {'form': form})


def save_mail(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('message')
        file = request.POST.get('file')
        reciever = request.POST.get('email')
        send_mail(subject, body, file, settings.EMAIL_HOST_
        [reciever], fail_silently=False)
        Gmail.objects.create(sender=MyUser,
                             subject=subject,
                             receiver=reciever,
                             file=file,
                             body=body)
        return render(request, 'gmail/mail_sent.html')

    return render(request, 'gmail/index.html')


def inbox(request):
    mail=Gmail.objects.filter(reciever=request.myuser.email)
    return render(request,'gmail/inbox.html',{'mail':mail})

def sent_mail(request):
    user = Registration.objects.get(user=request.user)
    sent = Gmail.objects.filter(sender=user)
    return render(request,'sent_mail.html',{'mail':sent})