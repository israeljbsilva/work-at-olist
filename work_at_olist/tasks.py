import celery

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


class PricingRulesCreateTask(celery.Task):
    name = 'pricing_rules_calculate_call_price'

    def run(self, *args, **kwargs):
        logger.info('Calculating the price of calls')
