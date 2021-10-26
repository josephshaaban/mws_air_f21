from django.contrib import admin

from air_app.models import QuestionAndAnswer


class QuestionAndAnswerAdmin(admin.ModelAdmin):
    """Admin view for `QuestionAndAnswer` model"""


admin.site.register(QuestionAndAnswer, QuestionAndAnswerAdmin)
