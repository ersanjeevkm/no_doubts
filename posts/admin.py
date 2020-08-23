from django.contrib import admin
from .models import Questions, Answers, Reply, Bookmarks, QuestionLikeVotes, QuestionDislikeVotes, AnswerLikeVotes, \
    AnswerDislikeVotes

# Register your models here.
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Reply)
admin.site.register(Bookmarks)
admin.site.register(QuestionLikeVotes)
admin.site.register(AnswerLikeVotes)
admin.site.register(QuestionDislikeVotes)
admin.site.register(AnswerDislikeVotes)
