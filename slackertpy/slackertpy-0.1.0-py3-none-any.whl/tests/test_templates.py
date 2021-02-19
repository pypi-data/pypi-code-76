from slackertpy import templates


def test_create_notification_assert_built():
    notification = templates.notification(text='This test ran successfully',
                                          title='Test Notification')
    assert isinstance(notification, dict)
    assert len(notification['blocks']) == 2


def test_create_job_start_assert_built():
    alert = templates.job_start(
        title='Test',
        desc='Desc of the process',
        overview={
            'key': 123,
            'key-str': 'value-str'
        }
    )

    assert isinstance(alert, dict)

    # title, desc, overview and a divider that comes before a section
    assert len(alert['blocks']) == 4


def test_create_job_executed_assert_built():
    alert = templates.job_executed(
        title='Title',
        desc='Description',
        result='Positive',
        overview={
            'key': 'value'
        },
        stats={
            'stat': 987
        }
    )
    assert isinstance(alert, dict)
    assert len(alert['blocks']) == 7


def test_create_job_error_assert_built():
    error_alert = templates.job_error(
        title='Process',
        error='Critical failure',
        notify_user_ids=['user1', 'user2'],
        alert_emoji=False
    )
    assert isinstance(error_alert, dict)
    # title, result, user notification section, divider and error output
    assert len(error_alert['blocks']) == 5

