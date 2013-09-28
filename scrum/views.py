from django.views.generic import TemplateView

class WhiteBoardView(TemplateView):
    template_name = 'scrum/whiteboard.html'
