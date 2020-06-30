from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils import timezone
from .validators import validate_file_size
from tinymce.models import HTMLField
# Create your models here.

class Questions(models.Model):
    title = models.CharField(max_length=150)
    question = HTMLField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    QUESTION_CHOICE = [('UG', (
        ('CS', 'Comp. Sci/ IT Engg.'),
        ('ECE', 'Electrical & Comm Engg.'),
        ('EEE', 'Electrical Engg.'),
        ('MH', 'Mechanical Engg'),
        ('GN', 'General'))
                        )]
    category = models.CharField(max_length=3, choices=QUESTION_CHOICE)
    attach_file1 = models.FileField(null=True, blank=True, upload_to='question_attachments',
                                    validators=[validate_file_size])
    attach_file2 = models.FileField(null=True, blank=True, upload_to='question_attachments',
                                    validators=[validate_file_size])
    votes = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return f'{self.get_category_display()}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Bookmarks(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Bookmark {self.question.title}'


class QuestionLikeVotes(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Like Votes: {self.question}'


class QuestionDislikeVotes(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'DisLike Votes: {self.question}'


class Answers(models.Model):
    answer = HTMLField()
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    attach_file1 = models.FileField(null=True, blank=True, upload_to='answer_attachments',
                                    validators=[validate_file_size])
    attach_file2 = models.FileField(null=True, blank=True, upload_to='answer_attachments',
                                    validators=[validate_file_size])
    verified = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='question', unique=True)

    def __str__(self):
        return f'Answer: {self.slug}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.question.slug})


class AnswerLikeVotes(models.Model):
    answer = models.OneToOneField(Answers, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Like Votes: {self.answer}'


class AnswerDislikeVotes(models.Model):
    answer = models.OneToOneField(Answers, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'DisLike Votes: {self.answer}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Reply: {self.author.username}, {self.answer}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.answer.question.slug})
