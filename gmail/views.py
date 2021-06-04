from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
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


def view(request):
    return render(request, 'gmail/email.html')


def registration(request):
    """ registration page """
    return render(request, 'gmail/register.html')


def save_register(request):
    """saving details """
    if request.method == "POST":
        user = MyUser.objects.create_user(email=request.POST['email'], password=request.POST['password'])
        Registration.objects.create(myuser=user)
        return render(request, 'gmail/index.html')
    else:
        return render(request, 'gmail/index.html', {'error': 'you are not eigible for this job'})


def login_request(request):
    """ save login details"""

    email = request.POST['email']
    password = request.POST['password']
    # email = request.POST['email']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'gmail/email.html')


    else:
        return render(request, 'gmail/index.html', {'error': 'Invalid username or password'})


def compose(request):
    """ composing mail """
    user = request.user
    print(user.id)
    form = GmailForm
    return render(request, 'gmail/compose.html', {'form': form, 'user': user})


# def save_mail(request):
#     """ saving mils"""
#     if request.method == 'POST':
#         subject = request.POST.get('subject')
#         body = request.POST.get('message')
#         # file = request.POST.get('file')
#         reciever = request.POST.get('email')
#         send_mail(subject, body, settings.EMAIL_HOST_USER,
#                   [reciever], fail_silently=False)
#         import pdb
#         # pdb.set_trace()
#         Gmail.objects.create(sender=request.user,
#                              subject=subject,
#                              reciever=MyUser.objects.get(email=reciever),
#                              body=body)
#         return render(request, 'gmail/email.html', {'email': reciever})
#
#     return render(request, 'gmail/index.html')


@login_required(login_url='/gmail/')
def inbox(request):
    """ mail inbox """
    mail = Gmail.objects.filter(reciever=request.user).filter(is_spam=False)
    return render(request, 'gmail/inbox.html', {'mail': mail})


@login_required(login_url='/gmail/')
def sent_mail(request):
    user = request.user
    mail = user.email
    # user = MyUser.objects.get(myuser=request.user)
    print(mail)
    print(type(mail))
    sent = Gmail.objects.filter(sender=user).filter(is_spam=False)
    print([each for each in sent])
    # print(mail)
    import pdb
    # pdb.set_trace()
    """ sent mails"""
    # sent = Gmail.objects.filter(sender='mail')
    # pdb.set_trace()

    return render(request, 'gmail/sent_mail.html', {'mail': sent})


@login_required(login_url='/gmail/')
def make_spam(request, id):
    """ making spam mails"""
    Gmail.objects.filter(id=id).update(is_spam=True)

    return render(request, 'gmail/inbox.html')


@login_required(login_url='/gmail/')
def spam(request):
    """ spam mails """
    user = request.user
    data = Gmail.objects.filter(is_spam=True).filter(reciever=user)
    return render(request, 'gmail/spam.html', {'mail': data})


def logout_page(request):
    """ logout page"""
    logout(request)
    return HttpResponseRedirect('/gmail/')


@login_required(login_url='/gmail/')
def make_unspam(request, id):
    """ making spam mails"""
    Gmail.objects.filter(id=id).update(is_spam=False)
    return render(request, 'gmail/inbox.html')


def make_draft(request, id):
    """ making drafts """
    Gmail.objects.filter(id=id).update(is_draft=True)
    return render(request, 'gmail/email.html', {'msg': 'message saved as draft'})


def draft(request):
    data = Gmail.objects.filter(is_draft=True)
    print(data)
    return render(request, 'gmail/draft.html', {'data': data})


def make_trash(request, id):
    Gmail.objects.filter(id=id).update(is_trash=True)
    return render(request, 'gmail/email.html')


def trash(request):
    user = request.user
    data = Gmail.objects.filter(is_trash=True).filter(reciever=user).filter(sender=user)
    return render(request, 'gmail/trash.html', {'data': data})


def make_untrash(request, id):
    Gmail.objects.filter(id=id).update(is_trash=False)
    return render(request, 'gmail/email.html')


def delete(request, id):
    Gmail.objects.filter(id=id).delete()
    return render(request, 'gmail/email.html')


def save_draftmail(request):
    """ saving mils"""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('message')
        # file = request.POST.get('file')
        reciever = request.POST.get('email')
        # send_mail(subject, body, settings.EMAIL_HOST_USER,
        #           [reciever], fail_silently=False)
        import pdb
        # pdb.set_trace()
        Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body, is_draft=True)
        return render(request, 'gmail/email.html', {'email': reciever})

    return render(request, 'gmail/index.html')


def save_mail(request):
    """TO send the mails from user"""
    if request.method == "POST":
        if request.POST["send"] != "cancel":
            # form = MailsForm(request.POST)
            # user = Registration.objects.get(myuser=request.user)
            subject = request.POST.get('subject')
            body = request.POST.get('message')
            # file = request.POST.get('file')
            reciever = request.POST.get('email')
            send_mail(subject, body, settings.EMAIL_HOST_USER,
                      [reciever], fail_silently=False)
            Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body, is_draft=True)
            return render(request,"gmail/email.html")
        else:
            # user = Registration.objects.get(myuser=request.user)
            subject = request.POST.get('subject')
            body = request.POST.get('message')
            # file = request.POST.get('file')
            reciever = request.POST.get('email')
            send_mail(subject, body, settings.EMAIL_HOST_USER,
                      [reciever], fail_silently=False)
            Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body,is_draft=True)
            return render(request, "gmail/email.html")
    else:
        return render(request, "gmail/compose.html")
