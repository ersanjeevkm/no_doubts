from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import RegistrationForm, AccountForm, ProfileForm, crnt_user
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower


def registration(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Logout to access this page!')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully. Login to continue.')
                return redirect('account')
            context = {'form': form}
        else:
            form = RegistrationForm()
            context = {'form': form}
        return render(request, 'users/registration.html', context)


class Login(SuccessMessageMixin, LoginView):
    success_message = 'Logged in successfully!'
    redirect_authenticated_user = True
    template_name = 'users/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'


@login_required
def account(request):
    crnt_user(request.user)

    if request.user.profile.field:
        field_update = False
    else:
        field_update = True

    if request.method == 'POST':
        u_form = AccountForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            messages.success(request, 'Account update successful.')
            return redirect('account')
        context = {'u_form': u_form, 'p_form': p_form, 'msg': field_update}
    else:
        u_form = AccountForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

        context = {'u_form': u_form, 'p_form': p_form, 'msg': field_update}
    return render(request, 'users/account.html', context)


class FilterUser(ListView):
    template_name = 'users/filter_user.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.order_by(Lower('username')).all()


class UserBookmarks(ListView):

    template_name = 'users/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.bookmarks_set.order_by('-question__date_posted').all()


class Password_reset(UserPassesTestMixin, PasswordResetView):
    template_name = 'users/password_reset.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True


class Password_reset_done(UserPassesTestMixin, PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True


class Password_reset_confirm(UserPassesTestMixin, PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True


class Password_reset_complete(UserPassesTestMixin, PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True


def user_stats(request, username):
    user = User.objects.get(username=username)
    doubt_votes = 0
    answer_votes = 0
    doubt_solved = 0

    for question in user.questions_set.all():
        doubt_votes += question.votes
    for answer in user.answers_set.all():
        answer_votes += answer.votes
    for question in user.questions_set.all():
        if question.answers_set.filter(verified=True).first():
            doubt_solved += 1
    answer_verf = user.answers_set.filter(verified=True).count

    return render(request, 'users/user_stats.html',
                  {'user': user, 'doubt_votes': doubt_votes, 'answer_votes': answer_votes, 'answer_verf': answer_verf,
                   'doubt_solved': doubt_solved})
