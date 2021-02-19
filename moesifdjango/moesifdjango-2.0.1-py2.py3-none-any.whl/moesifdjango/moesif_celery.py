
class MoesifCelery:

    def __init__(self):
        pass

    @classmethod
    def init_celery(cls, settings):
        CELERY = False
        simple_queue = None
        if settings.MOESIF_MIDDLEWARE.get('USE_CELERY', False):
            try:
                import celery
                from .tasks import async_client_create_event

                # try:
                #     get_broker_url = settings.BROKER_URL
                #     if get_broker_url:
                #         BROKER_URL = get_broker_url
                #     else:
                #         BROKER_URL = None
                # except AttributeError:
                #     BROKER_URL = settings.MOESIF_MIDDLEWARE.get('CELERY_BROKER_URL', None)
                #
                # self.add_job(settings, BROKER_URL)
                from kombu import Connection
                try:
                    BROKER_URL = settings.BROKER_URL
                    if BROKER_URL:
                        CELERY = True
                    else:
                        CELERY = False
                except AttributeError:
                    BROKER_URL = settings.MOESIF_MIDDLEWARE.get('CELERY_BROKER_URL', None)
                    if BROKER_URL:
                        CELERY = True
                    else:
                        print("USE_CELERY flag was set to TRUE, but BROKER_URL not found")
                        CELERY = False

                try:
                    conn = Connection(BROKER_URL)
                    simple_queue = conn.SimpleQueue('moesif_events_queue')
                except:
                    print("Error while connecting to - {0}".format(BROKER_URL))
            except:
                print("USE_CELERY flag was set to TRUE, but celery package not found.")
                CELERY = False
        return CELERY, simple_queue

    # @classmethod
    # def exit_handler(self, moesif_events_queue, scheduler):
    #     try:
    #         # Close the queue
    #         moesif_events_queue.close()
    #         # Shut down the scheduler
    #         scheduler.shutdown()
    #     except:
    #         # if DEBUG:
    #         print("Error while closing the queue or scheduler shut down")
    #
    # def add_job(self, settings):
    #     CELERY = False
    #     if settings.MOESIF_MIDDLEWARE.get('USE_CELERY', False):
    #         if BROKER_URL:
    #             try:
    #                 from apscheduler.schedulers.background import BackgroundScheduler
    #                 from apscheduler.triggers.interval import IntervalTrigger
    #                 from kombu import Connection
    #                 from kombu.exceptions import ChannelError
    #                 import atexit
    #                 import logging
    #                 from .tasks import async_client_create_event
    #
    #                 scheduler = BackgroundScheduler(daemon=True)
    #                 scheduler.start()
    #                 try:
    #                     conn = Connection(BROKER_URL)
    #                     moesif_events_queue = conn.SimpleQueue('moesif_events_queue')
    #                     scheduler.add_job(
    #                         func=lambda: async_client_create_event(moesif_events_queue),
    #                         trigger=IntervalTrigger(seconds=5),
    #                         id='moesif_events_batch_job',
    #                         name='Schedule events batch job every 5 second',
    #                         replace_existing=True)
    #
    #                     # Avoid passing logging message to the ancestor loggers
    #                     logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    #                     logging.getLogger('apscheduler.executors.default').propagate = False
    #
    #                     # Exit handler when exiting the app
    #                     atexit.register(lambda: self.exit_handler(moesif_events_queue, scheduler))
    #                 except:
    #                     # if DEBUG:
    #                         print("Error while connecting to - {0}".format(BROKER_URL))
    #             except:
    #                 # if DEBUG:
    #                     print("Error when scheduling the job")
    #         else:
    #             # if DEBUG:
    #                 print("Unable to schedule the job as the BROKER_URL is not provided")
