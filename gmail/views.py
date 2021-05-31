from django.contrib.auth import authenticate, login
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
def main(request):
    return render(request, 'gmail/index.html')
