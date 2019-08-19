import datetime

from work_at_olist import tasks


def test_calculate_call_price_more_than_one_day():
    # GIVEN
    timestamp_start = '2018-02-28T21:57:13'
    timestamp_start = datetime.datetime.strptime(timestamp_start, '%Y-%m-%dT%H:%M:%S')

    timestamp_end = '2018-03-01T22:10:56'
    timestamp_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')

    # WHEN
    call_price, call_duration = tasks.calculate_call_price(timestamp_start, timestamp_end)

    # THEN
    assert "{0:.2f}".format(call_price) == '87.03'
    assert str(call_duration) == '1 day, 0:13:43'


def test_calculate_reduced_tariff_call_price():
    # GIVEN
    timestamp_start = '2019-08-16T22:01:00'
    timestamp_start = datetime.datetime.strptime(timestamp_start, '%Y-%m-%dT%H:%M:%S')

    timestamp_end = '2019-08-17T05:59:00'
    timestamp_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')

    # WHEN
    call_price, call_duration = tasks.calculate_call_price(timestamp_start, timestamp_end)

    # THEN
    assert "{0:.2f}".format(call_price) == '0.36'
    assert str(call_duration) == '7:58:00'


def test_calculate_price_of_standard_time_call():
    # GIVEN
    timestamp_start = '2019-08-16T06:00:00'
    timestamp_start = datetime.datetime.strptime(timestamp_start, '%Y-%m-%dT%H:%M:%S')

    timestamp_end = '2019-08-16T22:00:00'
    timestamp_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')

    # WHEN
    call_price, call_duration = tasks.calculate_call_price(timestamp_start, timestamp_end)

    # THEN
    assert "{0:.2f}".format(call_price) == '86.76'
    assert str(call_duration) == '16:00:00'
