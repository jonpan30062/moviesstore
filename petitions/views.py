from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Petition, PetitionVote
from .forms import PetitionForm

def petition_list(request):
    """Display all petitions"""
    petitions = Petition.objects.all().order_by('-created_at')
    return render(request, 'petitions/petition_list.html', {'petitions': petitions})

def petition_detail(request, petition_id):
    """Display individual petition details"""
    petition = get_object_or_404(Petition, id=petition_id)
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = PetitionVote.objects.get(petition=petition, user=request.user)
        except PetitionVote.DoesNotExist:
            pass
    
    return render(request, 'petitions/petition_detail.html', {
        'petition': petition,
        'user_vote': user_vote
    })

@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petition_detail', petition_id=petition.id)
    else:
        form = PetitionForm()
    
    return render(request, 'petitions/create_petition.html', {'form': form})

@login_required
@require_POST
def vote_petition(request, petition_id):
    """Vote on a petition (AJAX endpoint)"""
    try:
        petition = get_object_or_404(Petition, id=petition_id)
        vote_value = request.POST.get('vote', 'true').lower() == 'true'
        
        # Check if user already voted
        vote, created = PetitionVote.objects.get_or_create(
            petition=petition,
            user=request.user,
            defaults={'vote': vote_value}
        )
        
        if not created:
            # User already voted, update their vote
            vote.vote = vote_value
            vote.save()
            message = f"Your vote has been updated to {'Yes' if vote_value else 'No'}"
        else:
            message = f"Your vote of {'Yes' if vote_value else 'No'} has been recorded"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'vote_count': petition.vote_count,
            'total_votes': petition.total_votes,
            'user_vote': vote_value
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error processing vote: {str(e)}'
        })