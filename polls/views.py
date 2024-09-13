import logging

from django.http import HttpResponseRedirect
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
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Shows the details of a specific poll if voting is allowed."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return only published questions that are not in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Redirects to the index if voting is not allowed,
         with an error message."""
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect('polls:index')
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """Displays the voting results for a specific poll."""

    model = Question
    template_name = 'polls/results.html'


logger = logging.getLogger('polls')


@login_required
def vote(request, question_id):
    """Handles voting for a specific choice in a poll,
     ensuring only one vote per user."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.warning(f"User {request.user.username} failed to"
                       f" select a choice for question {question_id}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    this_user = request.user
    try:
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice
        vote.save()
        logger.info(f"User {this_user.username} changed "
                    f"their vote to choice {selected_choice.choice_text} for question {question_id}")
    except Vote.DoesNotExist:
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
        vote.save()
        logger.info(f"User {this_user.username} voted for choice"
                    f" {selected_choice.choice_text} for question {question_id}")

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
