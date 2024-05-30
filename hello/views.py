from django.http import HttpResponse

def index(request):
  """A simple view function returning a message."""
  return HttpResponse("Hello, World! This is a Django server.")
