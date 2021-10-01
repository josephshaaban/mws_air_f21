from django.db import models
from django.utils.translation import gettext_lazy as _


class QuestionAndAnswer(models.Model):
    class Meta:
        verbose_name_plural = _('Questions and answers')
        verbose_name = _('Question and answer')

    question_text = models.TextField(blank=False, null=False)
    answer_text = models.TextField(blank=False, null=False)
