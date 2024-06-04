from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

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