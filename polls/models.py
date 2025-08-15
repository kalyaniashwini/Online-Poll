from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        if not user.is_authenticated:
            return False
        return not Vote.objects.filter(user=user, poll=self).exists()

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        alert_class = ['primary', 'secondary', 'success', 'danger', 'dark', 'warning', 'info']
        total = self.get_vote_count
        for choice in self.choice_set.all():
            num = choice.get_vote_count
            percentage = 0
            if total:
                percentage = (num / total) * 100
            res.append({
                'alert_class': secrets.choice(alert_class),
                'text': choice.choice_text,
                'num_votes': num,
                'percentage': percentage,
            })
        return res

    def __str__(self):
        return self.text

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
