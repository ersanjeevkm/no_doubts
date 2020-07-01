from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Questions, Answers, Reply, Bookmarks, QuestionLikeVotes, QuestionDislikeVotes, AnswerLikeVotes, \
    AnswerDislikeVotes
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from .signals import crnt_request


# question

class PostList(ListView):
    model = Questions
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class PostDetail(DetailView):
    model = Questions
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Questions
    fields = ['title', 'category', 'question', 'attach_file1', 'attach_file2']
    success_message = "Doubt Posted"

    def form_valid(self, form):
        form.instance.author = self.request.user
        crnt_request(self.request)
        return super().form_valid(form)


class EditPost(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Questions
    fields = ['title', 'category', 'question', 'attach_file1', 'attach_file2']
    success_message = "Doubt Updated"

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False


class DeletePost(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Questions
    template_name = 'posts/delete_post.html'
    success_message = 'Doubt Deleted'
    success_url = '/'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False


class UserPost(ListView):
    template_name = 'posts/user_post.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Questions.objects.filter(author=user).order_by('-date_posted')


# replies

class CreateReply(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reply
    fields = ['message']
    success_message = 'Replied to the answer'

    def form_valid(self, form):
        form.instance.author = self.request.user
        answer = get_object_or_404(Answers, slug=self.kwargs.get('slug'))
        form.instance.answer = answer
        return super().form_valid(form)


class EditReply(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    fields = ['message']
    success_message = "Reply Updated"

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False


class DeleteReply(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    template_name = 'posts/delete_reply.html'
    success_message = 'Reply Deleted'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.kwargs.get('slug')})


class UserReply(ListView):
    template_name = 'posts/user_reply.html'
    context_object_name = 'replies'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reply.objects.filter(author=user).order_by('-date_posted')


# answer

class CreateAnswer(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Answers
    success_message = 'Answer Posted'
    fields = ['answer', 'attach_file1', 'attach_file2']

    def form_valid(self, form):
        form.instance.author = self.request.user
        question = get_object_or_404(Questions, slug=self.kwargs.get('slug'))
        form.instance.question = question
        # email
        if self.request.user.profile.notifications:
            message = f'''
            *** This is an no-reply notification message from NO DOUBTS ***
            
            Hello {form.instance.question.author.username},
                '{form.instance.author.username}' has an answer to your Question :'{form.instance.question.title}'
    
            Check this link to find out {self.request.build_absolute_uri(reverse('post_detail', kwargs={'slug': form.instance.question.slug}))}
    
            If this isn't you please ignore this. Sorry for the inconvenience.
    
            If you didn't like to receive any such notifications select "Don't Notify Me" option under Notification panel here {self.request.build_absolute_uri(reverse('account'))}

            From, NO DOUBTS team.
            '''
            send_mail(
                subject=f"Someone has answered your Question {form.instance.question.title}",
                message=message,
                from_email='noreply.nodoubts@gmail.com',
                recipient_list=[form.instance.question.author.email],
                fail_silently=False,
            )

        return super().form_valid(form)


class EditAnswer(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Answers
    success_message = 'Answer Edited'
    fields = ['answer', 'attach_file1', 'attach_file2']

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False


class DeleteAnswer(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Answers
    template_name = 'posts/delete_answer.html'
    success_message = 'Answer Deleted'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.kwargs.get('qslug')})


class UserAnswer(ListView):
    template_name = 'posts/user_answer.html'
    context_object_name = 'answers'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Answers.objects.filter(author=user).order_by('-date_posted')


# category view

class CategoryView(ListView):
    template_name = 'posts/category_view.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Questions.objects.filter(category=self.kwargs.get('category')).order_by('-date_posted')


def filter_page(request):
    return render(request, 'posts/filter.html')


@login_required
def bookmark_post(request, slug):
    question = get_object_or_404(Questions, slug=slug)
    try:
        if request.user in question.bookmarks.users.all():
            messages.warning(request, 'You have already bookmarked this doubt')
        else:
            bookmark_object = Bookmarks.objects.get(question=question)
            bookmark_object.users.add(request.user)
            bookmark_object.save()
            messages.success(request, "Doubt bookmarked")
    except:
        bookmark_object = Bookmarks.objects.create(question=question)
        bookmark_object.save()
        bookmark_object.users.add(request.user)
        bookmark_object.save()
        messages.success(request, "Doubt bookmarked")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def remove_bookmark(request, slug):
    question = get_object_or_404(Questions, slug=slug)
    if request.user in question.bookmarks.users.all():
        bookmark_object = Bookmarks.objects.get(question=question)
        bookmark_object.users.remove(request.user)
        messages.success(request, 'Bookmark removed')
    else:
        messages.warning(request, 'You didn\'t bookmarked this doubt')
    return redirect(request.META['HTTP_REFERER'])


@login_required
def verify_answer(request, slug):
    answer = get_object_or_404(Answers, slug=slug)
    if request.user == answer.question.author:
        if not answer.verified:
            answer.verified = True
            answer.save()
            # email
            if request.user.profile.notifications:
                message = f'''
                        *** This is an no-reply notification message from NO DOUBTS ***
    
                        Hello {answer.author.username}, congratulations!
    
                        '{request.user.username}' has accepted your answer for : '{answer.question.title}'
    
                        Check this link to find out {request.build_absolute_uri(reverse('post_detail', kwargs={'slug': answer.question.slug}))}
    
                        If this isn't you please ignore this. Sorry for the inconvenience.
                        
                        If you didn't like to receive any such notifications select "Don't Notify Me" option under Notification panel here {request.build_absolute_uri(reverse('account'))}
                            
                        From, NO DOUBTS team.
                        '''
                send_mail(
                    subject=f"{answer.question.title}'s Author has accepted your Answer",
                    message=message,
                    from_email='noreply.nodoubts@gmail.com',
                    recipient_list=[answer.author.email],
                    fail_silently=False,
                )
            messages.success(request, 'You accepted the answer')
        else:
            messages.warning(request, 'This answer is already accepted')
        return redirect('post_detail', answer.question.slug)
    else:
        raise PermissionDenied


@login_required
def undo_verification(request, slug):
    answer = get_object_or_404(Answers, slug=slug)
    if request.user == answer.question.author:
        if answer.verified:
            answer.verified = False
            answer.save()
            messages.success(request, 'You have undone the accepted the answer')
        else:
            messages.warning(request, 'This answer is still not accepted')
        return redirect('post_detail', answer.question.slug)
    else:
        raise PermissionDenied


@login_required
def like_question(request, slug):
    question = get_object_or_404(Questions, slug=slug)
    try:
        question.questiondislikevotes.users.all()
        try:
            if request.user not in question.questiondislikevotes.users.all():
                if request.user not in question.questionlikevotes.users.all():
                    question.questionlikevotes.users.add(request.user)
                    question.votes += 1
                    question.save()
                    messages.success(request, 'You have liked the Doubt')
                else:
                    messages.warning(request, 'You have already liked the Doubt')
            else:
                question.questiondislikevotes.users.remove(request.user)
                question.votes += 1
                question.save()
                messages.success(request, 'You dislike is been Neutralized')

        except:
            q = QuestionLikeVotes(question=question)
            q.save()
            q.users.add(request.user)
            q.save()
            question.votes += 1
            question.save()
            messages.success(request, 'You have liked this Doubt')

    except:
        try:
            if request.user not in question.questionlikevotes.users.all():
                question.questionlikevotes.users.add(request.user)
                question.votes += 1
                question.save()
                messages.success(request, 'You have liked the Doubt')
            else:
                messages.warning(request, 'You have already liked the Doubt')

        except:
            q = QuestionLikeVotes(question=question)
            q.save()
            q.users.add(request.user)
            q.save()
            question.votes += 1
            question.save()
            messages.success(request, 'You have liked this Doubt')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def like_answer(request, slug):
    answer = get_object_or_404(Answers, slug=slug)
    try:
        answer.answerdislikevotes.users.all()
        try:
            if request.user not in answer.answerdislikevotes.users.all():
                if request.user not in answer.answerlikevotes.users.all():
                    answer.answerlikevotes.users.add(request.user)
                    answer.votes += 1
                    answer.save()
                    messages.success(request, 'You have liked the Answer')
                else:
                    messages.warning(request, 'You have already liked the Answer')
            else:
                answer.answerdislikevotes.users.remove(request.user)
                answer.votes += 1
                answer.save()
                messages.success(request, 'You dislike is been Neutralized')

        except:
            a = AnswerLikeVotes(answer=answer)
            a.save()
            a.users.add(request.user)
            a.save()
            answer.votes += 1
            answer.save()
            messages.success(request, 'You have liked this Answer')

    except:
        try:
            if request.user not in answer.answerlikevotes.users.all():
                answer.answerlikevotes.users.add(request.user)
                answer.votes += 1
                answer.save()
                messages.success(request, 'You have liked the Answer')
            else:
                messages.warning(request, 'You have already liked the Answer')

        except:
            a = AnswerLikeVotes(answer=answer)
            a.save()
            a.users.add(request.user)
            a.save()
            answer.votes += 1
            answer.save()
            messages.success(request, 'You have liked this Answer')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def dislike_question(request, slug):
    question = get_object_or_404(Questions, slug=slug)
    try:
        question.questionlikevotes.users.all()
        try:
            if request.user not in question.questionlikevotes.users.all():
                if request.user not in question.questiondislikevotes.users.all():
                    question.questiondislikevotes.users.add(request.user)
                    question.votes -= 1
                    question.save()
                    messages.success(request, 'You have disliked the Doubt')
                else:
                    messages.warning(request, 'You have already disliked the Doubt')
            else:
                question.questionlikevotes.users.remove(request.user)
                question.votes -= 1
                question.save()
                messages.success(request, 'You like is been Neutralized')

        except:
            q = QuestionDislikeVotes(question=question)
            q.save()
            q.users.add(request.user)
            q.save()
            question.votes -= 1
            question.save()
            messages.success(request, 'You have disliked this Doubt')

    except:
        try:
            if request.user not in question.questiondislikevotes.users.all():
                question.questiondislikevotes.users.add(request.user)
                question.votes -= 1
                question.save()
                messages.success(request, 'You have disliked the Doubt')
            else:
                messages.warning(request, 'You have already disliked the Doubt')

        except:
            q = QuestionDislikeVotes(question=question)
            q.save()
            q.users.add(request.user)
            q.save()
            question.votes -= 1
            question.save()
            messages.success(request, 'You have disliked this Doubt')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def dislike_answer(request, slug):
    answer = get_object_or_404(Answers, slug=slug)
    try:
        answer.answerlikevotes.users.all()
        try:
            if request.user not in answer.answerlikevotes.users.all():
                if request.user not in answer.answerdislikevotes.users.all():
                    answer.answerdislikevotes.users.add(request.user)
                    answer.votes -= 1
                    answer.save()
                    messages.success(request, 'You have disliked the Doubt')
                else:
                    messages.warning(request, 'You have already disliked the Doubt')
            else:
                answer.answerlikevotes.users.remove(request.user)
                answer.votes -= 1
                answer.save()
                messages.success(request, 'You like is been Neutralized')

        except:
            a = AnswerDislikeVotes(answer=answer)
            a.save()
            a.users.add(request.user)
            a.save()
            answer.votes -= 1
            answer.save()
            messages.success(request, 'You have disliked this Doubt')

    except:
        try:
            if request.user not in answer.answerdislikevotes.users.all():
                answer.answerdislikevotes.users.add(request.user)
                answer.votes -= 1
                answer.save()
                messages.success(request, 'You have disliked the Doubt')
            else:
                messages.warning(request, 'You have already disliked the Doubt')

        except:
            a = AnswerDislikeVotes(answer=answer)
            a.save()
            a.users.add(request.user)
            a.save()
            answer.votes -= 1
            answer.save()
            messages.success(request, 'You have disliked this Doubt')

    return redirect(request.META['HTTP_REFERER'])


class QuestionsSearchView(SearchView):
    template_name = 'posts/question_search.html'
    queryset = SearchQuerySet()
    form_class = SearchForm
    paginate_by = 10
