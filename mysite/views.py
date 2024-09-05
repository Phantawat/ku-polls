from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            # login the user
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
        messages.error(request,
                       'Please check username and password again.'
                       ' Your password can\'t be too similar to your '
                       'other personal information, '
                       'must contain at least 8 characters. '
                       'can\'t be a commonly used password.'
                       'and can\'t be entirely numeric.')
        return redirect('signup')

    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})