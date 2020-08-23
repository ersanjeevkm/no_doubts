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
    QUESTION_CHOICE = [('Engg - UG (BE/B.Tech)', (
        ('BM', 'Bio-Medical Engg.'),
        ('CI', 'Civil Engg.'),
        ('CSE', 'Comp. Sci/ IT Engg.'),
        ('EEE', 'Elec. & Electronics Engg.'),
        ('ECE', 'Electronics & Comm Engg.'),
        ('GE', 'Geo Informatics'),
        ('IE', 'Industrial Engg.'),
        ('MF', 'Manufacturing Engg.'),
        ('MS', 'Material Science & Engg.'),
        ('MH', 'Mechanical Engg'),
        ('MI', 'Mining Engg.'),
        ('PT', 'Printing Tech.'),
    )),
     ('Engg - PG (ME/M.Tech)', (
        ('AEM', 'Applied Electronics'),
        ('BMM', 'Bio-Medical Engineering (M.E.)'),
        ('CMM', 'Coastal Management'),
        ('CSM', 'Communication Systems'),
        ('CAM', 'Computer Aided Design'),
        ('CIM', 'Computer Integrated Manuf.'),
        ('CSM', 'Computer Science & Engg. (M.E.)'),
        ('CEM', 'Construction Engg. & Management'),
        ('CNM', 'Control & Instrumentation Engg.'),
        ('ESM', 'Embedded Systems Tech.'),
        ('EEM', 'Energy Engineering'),
        ('EDM', 'Engineering Design'),
        ('ENM', 'Environmental Engineering'),
        ('EMM', 'Environmental Management'),
        ('GIM', 'Geo-Informatics (M.E.)'),
        ('HVM', 'High Voltage Engineering'),
        ('HWM', 'Hydrology & Water Resources Engg.'),
        ('IEM', 'Industrial Engineering'),
        ('ITM', 'Information Technology (M.E.)'),
        ('ICM', 'Internal Combustion Engg.'),
        ('IWM', 'Irrigation Water Management'),
        ('MSM', 'Manufacturing System & Management'),
        ('MEM', 'Medical Electronics'),
        ('MTM', 'Multimedia Technology'),
        ('NSM', 'Nano Science and Technology'),
        ('OCM', 'Optical Communication Engg.'),
        ('POM', 'Polymer Science and Engineering'),
        ('PEM', 'Power Electronics and Drives'),
        ('PSM', 'Power Systems Engineering'),
        ('PTM', 'Printing Technology (M.E.)'),
        ('PDM', 'Product Design & Development'),
        ('QEM', 'Quality Engg. and Management'),
        ('RAM', 'Refrigeration & Air Conditioning'),
        ('RSM', 'Remote Sensing'),
        ('SEM', 'Software Engineering'),
        ('SMM', 'Soil Mechanics & Foundation Engg.'),
        ('STM', 'Structural Engineering'),
        ('SOR', 'System Engg. & Operation Research'),
        ('UEM', 'Urban Engineering'),
        ('VDM', 'VLSI Design'),
        ('GN', 'General')
     ))]
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
