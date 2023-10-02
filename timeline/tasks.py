from datetime import timedelta, datetime

from django.db.models import Exists, OuterRef

from elk.celery import app as celery
from market.models import Class
from crm.models import Customer
from mailer.owl import Owl
from timeline.signals import class_starting_student, class_starting_teacher

from elk.logging import logger

@celery.task
def notify_15min_to_class():
    for i in Class.objects.starting_soon(timedelta(minutes=30)).filter(pre_start_notifications_sent_to_teacher=False).distinct('timeline'):
        for other_class_with_the_same_timeline in Class.objects.starting_soon(timedelta(minutes=30)).filter(timeline=i.timeline):
            """
            Set all other starting classes as notified either.
            """
            other_class_with_the_same_timeline.pre_start_notifications_sent_to_teacher = True
            other_class_with_the_same_timeline.save()
        class_starting_teacher.send(sender=notify_15min_to_class, instance=i)

    for i in Class.objects.starting_soon(timedelta(minutes=30)).filter(pre_start_notifications_sent_to_student=False):
        i.pre_start_notifications_sent_to_student = True
        i.save()
        class_starting_student.send(sender=notify_15min_to_class, instance=i)


@celery.task
def send_inactivity_warnings():
    """
        Send warning about money spending for week-inactive students
    """

    customers_not_studied_last_week = Customer.objects.with_subscriptions() \
        .had_classes_in_past(days_ago=7) \
        .filter(got_inactivity_warning=False, customer_email__isnull=False)

    # FIXME: I have no idea how to determine which customers had their lesson and which had it sheduled but not came
    # i see that in case when customer cancelled lesson -- timeline is delited, but what if it didnt show up?
    # I'll assume that teacher cancells lesson if student didnt show up
    # IRL i'll just ask how business operates

    # FIXME: For similar reason no idea how its supposed to handleone-off lessons (with type SingleLessonProduct), so i just dont

    # FIXME: How to notify customers without email?

    successfully_warned_customer_ids = []
    for customer in customers_not_studied_last_week:
        try:
            owl = Owl(
                template='mail/inactivity_warning.html',
                ctx={},
                to=[customer.user.email],
                timezone=customer.user.crm.timezone,
            )
            owl.send()
            successfully_warned_customers.append(customer_id)
        except Exception as e:
            logger.error(f"Error sending inactivity email to student {user.id}: {e}")

    Customer.objects.filter(id__in=successfully_warned_customers).update(got_inactivity_warning=True)
