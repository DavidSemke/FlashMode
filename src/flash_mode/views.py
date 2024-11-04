from django.shortcuts import render
from django.urls import reverse

# from allauth.account.views import LoginView


def index(request):
    return render(request, "nonoverrides/index.html")


# class CustomLoginView(LoginView):
#     def get_success_url(self):
#         username = self.request.user.username
#         return reverse('dashboard:index', args=(username,))
