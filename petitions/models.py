from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    movie_name = models.CharField(max_length=255, help_text="Name of the movie you want to see added")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Whether admin has approved this petition")
    
    def __str__(self):
        return f"{self.title} - {self.movie_name}"
    
    @property
    def vote_count(self):
        return self.petitionvote_set.filter(vote=True).count()
    
    @property
    def total_votes(self):
        return self.petitionvote_set.count()

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)  # True for yes, False for no
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('petition', 'user')  # One vote per user per petition
    
    def __str__(self):
        vote_type = "Yes" if self.vote else "No"
        return f"{self.user.username} voted {vote_type} on {self.petition.title}"