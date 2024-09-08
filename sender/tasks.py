from datetime import datetime, timedelta

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from time import strftime
from dotenv import load_dotenv
import smtplib
import os

from sender.models import Sender, DeliveryAttempt

load_dotenv()


def send_messages():
    mailings = Sender.objects.all()

    for send_mail_for_customers in mailings:

        mailing_list_recipients = []

        if send_mail_for_customers.first_message <= datetime.date.today() <= send_mail_for_customers.last_message:
            header = send_mail_for_customers.message.header
            message = send_mail_for_customers.message.body
            mails = send_mail_for_customers.clients.all()

            # Если рассылка отправляется впервые, то заполняю дату первой отправки и ставлю дату следующей отправки в
            # зависимости от её периодичности отправки
            if not send_mail_for_customers.first_message:
                send_mail_for_customers.first_message = strftime('%Y-%m-%d %H:%M:%S')

                # Если рассылку надо отправлять каждый день
                if str(send_mail_for_customers.frequency) == Sender.FREQUENCIES[0][0]:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=1)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждую неделю
                elif str(send_mail_for_customers.frequency) == Sender.FREQUENCIES[1][0]:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=7)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждый месяц
                else:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=30)
                    send_mail_for_customers.save()

                # Отправляю рассылки
                for mailing in mails:
                    try:
                        send_mail(
                            subject=header,
                            message=message,
                            from_email=os.getenv('mail'),
                            recipient_list=[mailing],
                            fail_silently=False,
                        )

                        # Создаю получателя и добавляю его в список получивших письмо
                        recipient = f'{mailing} - письмо отправлено'
                        mailing_list_recipients.append(recipient)

                    except smtplib.SMTPException as e:

                        # Создаю получателя и добавляю его в список не получивших письмо
                        recipient = f'{mailing} - письмо не отправлено в связи с {e}'
                        mailing_list_recipients.append(recipient)


                # Создаю новый экземпляр модели попытки рассылки и пишу что он успешный
                DeliveryAttempt.objects.create(attempt_datetime=strftime('%Y-%m-%d %H:%M:%S'),
                                       sender=send_mail_for_customers, mail_server_response=mailing_list_recipients)

            # Если рассылка отправляется не первый раз, то смотрю дату следующей рассылки, которую установил выше,
            # сравниваю с часом в который необходимо отправить рассылку и с минутой в которую необходимо отправить
            # рассылку
            elif send_mail_for_customers.date_letter_was_sent == datetime.date.today():

                # Если рассылку надо отправлять каждый день
                if str(send_mail_for_customers.frequency) == Sender.FREQUENCIES[0][0]:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=1)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждую неделю
                elif str(send_mail_for_customers.frequency) == Sender.FREQUENCIES[1][0]:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=7)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждый месяц
                else:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=30)
                    send_mail_for_customers.save()

                # Отправляю рассылку пользователям
                for mailing in mails:
                    try:
                        send_mail(
                            subject=header,
                            message=message,
                            from_email=os.getenv('mail'),
                            recipient_list=[mailing]
                        )

                        # Создаю получателя и добавляю его в список получивших письмо
                        recipient = f'{mailing} - успешно получил рассылку'
                        mailing_list_recipients.append(recipient)

                    except smtplib.SMTPException as e:

                        # Создаю получателя и добавляю его в список не получивших письмо
                        recipient = f'{mailing} - не получил рассылку в связи с {e}'
                        mailing_list_recipients.append(recipient)

                        # Создаю новый экземпляр модели попытки рассылки и пишу что он успешный
                    DeliveryAttempt.objects.create(date_and_time_of_last_mailing_attempt=strftime('%Y-%m-%d %H:%M:%S'),
                                           mailing=send_mail_for_customers,
                                           attempt_status=mailing_list_recipients)