from django.forms import ModelForm

from gmail.models import Gmail


class GmailForm(ModelForm):
    class Meta:
        model = Gmail
        fields =['reciever','subject','body','file']


# class UserAdminCreationForm(UserCreationForm):
#     """
#     A Custom form for creating new users.
#     """

    # class Meta:
    #     model = get_user_model()
    #     fields = ['email']
