import logging

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Displays the latest five published polls on the index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions
         that are not in the future."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        """Add question status to the context."""
        context = super().get_context_data(**kwargs)
        for question in context['latest_question_list']:
            question.status = 'Open' if question.can_vote() else 'Closed'
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Shows the details of a specific poll if voting is allowed."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return only published questions that are not in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for question details.

        Redirect to index if voting is not allowed.
        Show last vote if authenticated.
        """
        try:
            question = self.get_object()
        except Http404:
            messages.error(request, "This question is not available.")
            return HttpResponseRedirect(reverse('polls:index'))

        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this question.")
            return HttpResponseRedirect(reverse('polls:index'))

        this_user = request.user
        last_vote = None
        if this_user.is_authenticated:
            try:
                last_vote = (Vote.objects.get
                             (user=this_user, choice__question=question).choice.id)
            except Vote.DoesNotExist:
                last_vote = None
        return render(request, self.template_name,
                      {'question': question, 'last_vote': last_vote})


class ResultsView(generic.DetailView):
    """Displays the voting results for a specific poll."""

    model = Question
    template_name = 'polls/results.html'


logger = logging.getLogger('polls')


@login_required
def vote(request, question_id):
    """Handles voting for a specific choice in a poll,
     ensuring only one vote per user and allowing updates."""
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        logger.warning(f"User {request.user.username} attempted to vote in a closed poll {question_id}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Voting is not allowed for this poll."
        })

    try:
        # Retrieve the selected choice from the POST request
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Log and render an error if the choice is invalid
        logger.warning(f"User {request.user.username} failed to select a choice for question {question_id}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })

    this_user = request.user

    try:
        # Check if the user has already voted for this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # Update the existing vote with the new choice
        vote.choice = selected_choice
        vote.save()
        logger.info(
            f"User {this_user.username} changed their vote to choice {selected_choice.choice_text}"
            f" for question {question_id}")
        messages.success(request, f"Your vote was updated to "
                                  f"'{selected_choice.choice_text}'")
    except Vote.DoesNotExist:
        # Create a new vote if the user has not voted yet
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
        vote.save()
        logger.info(
            f"User {this_user.username} voted for choice {selected_choice.choice_text}"
            f" for question {question_id}")
    messages.success(request, f"You voted for "
                              f"'{selected_choice.choice_text}'")
    # Redirect to the results page after voting
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            ip_addr = request.META.get('REMOTE_ADDR')
            logger.info(f"User {username} logged in from {ip_addr}")
            return redirect('polls:index')
        else:
            ip_addr = request.META.get('REMOTE_ADDR')
            logger.warning(f"Failed login attempt for {username} from {ip_addr}")
    return render(request, 'login.html')


def logout(request):
    """Handle user logout."""
    ip_addr = request.META.get('REMOTE_ADDR')
    logger.info(f"User {request.user.username} logged out from {ip_addr}")
    auth_logout(request)
    return redirect('polls:index')
