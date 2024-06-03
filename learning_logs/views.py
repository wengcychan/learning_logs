from django.shortcuts import render
from .models import Topic

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