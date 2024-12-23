from allauth.account.views import LoginView, SignupView, LogoutView


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'


class CustomSignupView(SignupView):
    template_name = 'auth/signup.html'


class CustomLogoutView(LogoutView):
    template_name = 'auth/logout.html'


login = CustomLoginView.as_view()
signup = CustomSignupView.as_view()
logout = CustomLogoutView.as_view()
