class Enqueue(dict):

    __cmd = 'Enqueue'

    def __init__(self, queue_id, action_url, wait_url):
        super().__init__()
        self.__setitem__(Enqueue.__cmd, {})
        self.queue_id(queue_id)
        self.action_url(action_url)
        self.wait_url(wait_url)

    def queue_id(self, queue_id):
        self.__getitem__(Enqueue.__cmd)['queueId'] = queue_id
        return self

    def action_url(self, action_url):
        self.__getitem__(Enqueue.__cmd)['actionUrl'] = action_url
        return self

    def wait_url(self, wait_url):
        self.__getitem__(Enqueue.__cmd)['waitUrl'] = wait_url
        return self

    def notification_url(self, notification_url):
        self.__getitem__(Enqueue.__cmd)['notificationUrl'] = notification_url
        return self
