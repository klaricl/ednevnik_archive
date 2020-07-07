from django.shortcuts import render

from appmessages.forms import ContactMessagesForm
from appmessages.models import ContactMessages
import smtplib
# Create your views here.

def contactMsgHandler(request):
    """Contacting the admin

    POST Data are provided from the index.html file.

    If the form is valid, the message will be saved in the ContactMessages model,
    and the message will be sent to the admin on the omikron.ednevnik@1988@gmail.com
    e-mail.

    returns: confirmation.html, "something went wrong"

    models: ContactMessages

    forms: ContactMessagesForm
    """

    if request.method == 'POST':
        ADMIN_MAIL_ACCOUNT = "omikron.ednevnik@gmail.com"
        ADMIN_MAIL_PASSWORD = "omikron123"
        ADMIN_MAIL_SMTP = 'smtp.gmail.com'
        ADMIN_MAIL_SMTP_PORT = 587

        # msg_form contains the data from the POST data
        msg_form = ContactMessagesForm(data = request.POST)

        if msg_form.is_valid():

            msg = msg_form.save()

            s = smtplib.SMTP(ADMIN_MAIL_SMTP, ADMIN_MAIL_SMTP_PORT)
            s.starttls()
            s.login(ADMIN_MAIL_ACCOUNT, ADMIN_MAIL_PASSWORD)
            message = msg.message

            
            s.sendmail("omikron.ednevnik@1988@gmail.com", ADMIN_MAIL_SMTP, message)
            s.quit()
            return render(request, "confirmation.html")
    else:
        return HttpResponse("something went wrong")
