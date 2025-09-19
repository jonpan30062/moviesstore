from django.contrib import admin
from .models import Petition, PetitionVote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie_name', 'created_by', 'created_at', 'vote_count', 'is_approved')
    list_filter = ('created_at', 'is_approved')
    search_fields = ('title', 'movie_name', 'description')
    readonly_fields = ('created_at', 'vote_count')

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'vote', 'created_at')
    list_filter = ('vote', 'created_at')
    search_fields = ('petition__title', 'user__username')