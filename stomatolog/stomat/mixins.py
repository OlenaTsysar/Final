from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class EditUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="Editor").exists() or user.is_superuser