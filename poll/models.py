from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User

class Poll(models.Model):
    POLL_TYPES = [
        ('mcq', 'Multiple Choice Question'),
        ('tf', 'True or False'),
        ('comment', 'Comment'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    question = models.CharField(max_length=500)
    poll_type = models.CharField(max_length=10, choices=POLL_TYPES)
    duration = models.PositiveIntegerField(
        help_text='Duration in hours',
        validators=[MinValueValidator(1)]
    )
    result_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > (self.created_at + timezone.timedelta(hours=self.duration))
    
class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.poll.question[:30]} - {self.text[:20]}"
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'poll')  # prevents double-voting per poll per user
        
    def __str__(self):
        return f"{self.user.email} - {self.poll.question[:30]} - {self.option.text[:20]}"
    