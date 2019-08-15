import os
import sys
from logging import getLogger

from celery import Celery

from django.conf import settings
from kombu import Exchange, Queue

from work_at_olist.tasks import PricingRulesCreateTask


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')


def setup_app(celery_app):
    work_at_olist_register_exchange = Exchange('e.work_at_olist', type='direct')

    pricing_rules_queue = Queue('q.pricing_rules.calculate_call_price',
                                exchange=work_at_olist_register_exchange,
                                routing_key='pricing_rules',
                                durable=True)

    celery_app.conf.task_queues = (pricing_rules_queue, )


def create_app():
    app = Celery('work-at-olist')
    logger = getLogger(__name__)
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.log.setup(loglevel=logger.level)

    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    setup_app(app)
    app.register_task(PricingRulesCreateTask())
    return app


app = create_app()

if __name__ == '__main__':  # pragma: no cover
    argv = sys.argv + ['-A', 'config.celery_app', 'worker', '--loglevel', 'debug', '-n', 'work-at-olist']
    app.start(argv)
