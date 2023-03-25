from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.http.response import FileResponse

from .models import MyBots
from .models import Comments
from .models import MyProjects
from .forms import CommentForm
from .models import Certificate
from .utils import send_telegram
from .utils import get_client_ip
from .libs.telebot import telebot
from .forms import GetInTouchForm


def home_view(request):
    """The Home View"""
    if settings.APP_ENV == 'production':
        client_ip, user_agent = get_client_ip(request)
        send_telegram(**{
            "client_ip": client_ip,
            "user_agent": user_agent,
        })

    return render(request, 'main/home.html')


def about_view(request):
    """Th About View"""
    items = Comments.objects.all()

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('about-my-self')

    else:
        form = CommentForm()

    context = {
        "form": form,
        "items": items,
    }
    return render(request, 'main/about.html', context)


def comment_remove_view(request, primary_key):
    """The Comment Remove View"""
    if request:
        comment = Comments.objects.get(id=primary_key)
        comment.delete()

    return redirect('about-my-self')


def my_resume_download_view(request):
    """The My Resume Download View
        uses for download resume."""
    if request:
        filename = './static/resume.pdf'
        response = FileResponse(open(filename, 'rb'))

        return response


def my_projects_view(request):
    """The My Projects View
        uses for see projects."""
    projects = MyProjects.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'main/my-projects.html', context)


def my_bot_projects_view(request):
    """The My Bot Projects View
        uses for see my bot projects
    """
    projects = MyBots.objects.all()
    context = {
        'projects': projects
    }

    return render(request, 'main/my-projects-bot.html', context)


def contact_page_view(request):
    """The Contact Page View
        uses for contact with me
    """
    form = GetInTouchForm()

    if request.method == 'POST':
        form = GetInTouchForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            text = f"The person who sent the message: {obj}\nEmail: {obj.email}\nMessage text: {obj.body}" # noqa
            resp = telebot.send_message(text)
            if resp.status_code == 200:
                messages.success(
                    request, 'Your message has been sent successfully, I will reply you soon!') # noqa
                return HttpResponseRedirect('contact-me')
            else:
                mess: str = "There was a problem sending the message,"
                mess += "Please, try again later."
                messages.error(request, mess)

    context = {
        "form": form
    }

    return render(request, 'main/contact-me.html', context)


class CertificateListView(ListView):
    template_name = "sections/certificates.html"
    queryset = Certificate.objects.all()
    context_object_name = 'certificates'


class CertificateDetailView(DetailView):
    model = Certificate
    template_name = "sections/certificates.html"
