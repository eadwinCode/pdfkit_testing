import pdfkit
import platform
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string, get_template
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail as django_send_mail
from email_template.forms import CreatePDFTemplate


# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.75in',
#     'margin-right': '0.75in',
#     'margin-bottom': '0.75in',
#     'margin-left': '0.75in',
#     'encoding': "UTF-8",
#     'custom-header' : [
#         ('Accept-Encoding', 'gzip')
#     ],
#     'cookie': [
#         ('cookie-name1', 'cookie-value1'),
#         ('cookie-name2', 'cookie-value2'),
#     ],
#     'no-outline': None
# }

# read more on pdfkit options
pdfkit_options = {
    'page-size': 'A4',
    'margin-top': '0.20in',
    'margin-right': '0.20in',
    'margin-bottom': '0.20in',
    'margin-left': '0.20in',
}


class HomeView(generic.TemplateView):
    template_name = 'index.html'


class GenerateDownloadLink(generic.FormView):
    template_name = 'generate_link.html'
    form_class = CreatePDFTemplate

    def get_success_url(self):
        messages.info(self.request, 'Email sent, Please check your mail')
        return reverse('index')

    def form_valid(self, form):
        """Create download link and email user the link to download the agreement"""
        response = super().form_valid(form)
        subject = "Agreement Link"
        message = render_to_string('email_template.txt', {
            'email': form.cleaned_data['email'],
            'domain': self.request.build_absolute_uri(reverse('index'))[:-1]
        })
        recipient_list = ("eedev.toochos@gmail.com", 'dwanoreply@gmail.com')
        sender = "DWA Agreement <dwanoreply@gmail.com>"
        django_send_mail(subject=subject, message=message, from_email=sender,
                         recipient_list=recipient_list, fail_silently=False)
        return response


def get_pdf_content(html_content):
    if platform.system() == 'Windows'
        config = pdfkit.configuration(wkhtmltopdf=settings.WKTHTMLTOPDF_WINDOWS_PATH)
        return pdfkit.from_string(html_content, False, options=pdfkit_options, configuration=config,
                                  css=f"{settings.STATIC_ROOT}/css/bootstrap.min.css")
    
    return pdfkit.from_string(html_content, False, options=pdfkit_options, css=f"{settings.STATIC_ROOT}/css/bootstrap.min.css")


class DownloadPDFView(generic.View):
    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if not email:
            return Http404(Exception('Invalid url'))
        html = render_to_string("pdf_template.html", {'email': email})
        pdf = get_pdf_content(html)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
