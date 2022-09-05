from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    @property
    def vote_count(self):
        return sum([choice.vote_count for choice in self.choice_set.all()])


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.TextField(null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice

    @property
    def vote_count(self):
        return self.vote_set.count()


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.choice.id} x {self.user.username}"

    class Meta:
        unique_together = (('user', 'choice'),)