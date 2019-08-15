from work_at_olist.tasks import PricingRulesCreateTask


def test_should_create_pricing_rules_task():
    # GIVEN
    task = PricingRulesCreateTask()

    # WHEN
    result = task.delay()

    # THEN
    result.get()
    assert result.successful()
