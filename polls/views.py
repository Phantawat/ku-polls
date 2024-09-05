from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Displays the latest five published polls on the index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions that are not in the future."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Shows the details of a specific poll if voting is allowed."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return only published questions that are not in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Redirects to the index if voting is not allowed, with an error message."""
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect('polls:index')
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """Displays the voting results for a specific poll."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Handles voting for a specific choice in a poll, ensuring only one vote per user."""
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Return an error message if no choice was selected
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })

    this_user = request.user

    # Handle the user's vote (update if exists, create if new)
    try:
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice  # Update the vote with the new choice
        vote.save()
        messages.success(request, f"Your vote was updated to '{selected_choice.choice_text}'")
    except Vote.DoesNotExist:
        # Create a new vote if no previous vote exists
        Vote.objects.create(user=this_user, choice=selected_choice)
        messages.success(request, f"You voted for '{selected_choice.choice_text}'")

    # Redirect to the results page after successful voting
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
