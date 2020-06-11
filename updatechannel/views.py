from django.shortcuts import render


def index_view(request):
    """ An example HTML page opening a websocket to the updatechannel. """

    return render(request, 'index.html', {})
