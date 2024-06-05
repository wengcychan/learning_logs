from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


"""We apply login_required() as a decorator to the topics() view function by prepending
login_required with the @ symbol. As a result, Python knows to run the code in login_required()
before the code in topics(). If the user isn't logged in, they're redirected to the login page."""


@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    # Query: Use the get() method to retrieve the topic requested by the user.
    topic = Topic.objects.get(id=topic_id)
    # Query: Get all the entries associated with the topic and order them by date_added.
    # The minus sign in front of date_added sorts the results in reverse order,
    # which will display the most recent entries first.
    entries = topic.entry_set.order_by('-date_added')
    # Store the topic and entries in the context dictionary, which we’ll pass to the template.
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


"""this function takes in the request object as its parameter.
When the user initially requests this page, their browser will send a GET request. 
Once the user has filled out and submitted the form, their browser will submit a POST request.
Depending on the request, we know whether the user is requesting a blank form 
(GET) or asking us to process a completed form (POST).
"""


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            # redirect() function takes in the name of a view and redirects the user to the page associated with that view.
            return redirect('learning_logs:topics')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def edit_topic(request, topic_id):
    """ Edit an existing topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        """ Initial request; pre-fill form with the current topic.
        The argument instance=topic tells Django to create the form,
        prefilled with information from the existing topic object.
        The user will see their existing data and be able to edit that data.
        """
        form = TopicForm(instance=topic)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)


""" The new_entry() view function is similar to new_topic(), 
but it takes an additional parameter: topic_id, which stores the
value it receives from the url. 
"""


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        """ If form is valid, we need to set the entry object's topic attribute
        before saving it to the database. When we call save(), we pass commit=False
        argument to tell Django to create a new entry object and assign it to 
        new_entry without saving it to the database yet. We then set the topic
        attribute of new_entry to the topic we pulled from the database at the beginning of the function.
        Then we call save() with no arguments to save the new entry to the database
        with the correct associated topic.
        """
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            """ The redirect() call requires two arguments: the name of the view
            we want to redirect to and the argument that view function requires
            """
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """ Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        """ Initial request; pre-fill form with the current entry.
        The argument instance=entry tells Django to create the form,
        prefilled with information from the existing entry object.
        The user will see their existing data and be able to edit that data.
        """
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
