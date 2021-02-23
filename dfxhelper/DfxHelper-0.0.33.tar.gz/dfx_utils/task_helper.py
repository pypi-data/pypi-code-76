import asyncio, logging
from datetime import datetime
from typing import List, Dict
from dfx_utils.klass_helper import BaseData
from dfx_utils.helper import random_str, json_friendly_loads


class TaskSetting:
    def __init__(self, setting: Dict = None, handlers: Dict = None):
        """
        :setting: {'redis': aio_redis_instance, 'task_tag': redis_task_tag}
            :redis_task_tag: default_value -> 'default'
        :handlers: {'handle_demo': demo}
            :demo: demo is function to handle job
        """
        self.__container = BaseData()
        if setting:
            self.__container.add(**setting)
        if handlers:
            self.__container.add(**handlers)

    def add(self, **kwargs):
        self.__container.add(**kwargs)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except:
            return self.__container.__getattribute__(item)

    def __call__(self):
        return self.__container()

    def __delitem__(self, key):
        self.__container.add(**{key: None})

    def __setitem__(self, key, value):
        self.__container.add(**{key: value})

    def __getitem__(self, item):
        return self().get(item)

    def get(self, item, default=None):
        return self.__getitem__(item) or default


class WorkerQueue(asyncio.Queue):
    def __init__(self, queues: List[str], setting: TaskSetting):
        super().__init__()
        self.setting, self.running = setting, True
        self.queues, self.tasks, self.task_futures = dict(), list(), list()
        # 全局并发限制 默认并发100
        self.task_limit_queue = asyncio.Queue(self.setting.runtime_limit or 100)
        for name in queues:
            self.queues[name] = asyncio.Queue()
            self.task_futures.append(asyncio.ensure_future(self.__deal_job(name)))
        self.task_futures.append(asyncio.ensure_future(self.__deal_queue()))

    def __task_callback(self, task):
        self.tasks.remove(task)

    async def __deal_job(self, name):
        queue = self.queues.get(name)
        handler = self.setting.get(name)

        if handler:
            while self.running and queue:
                job: BaseData = await queue.get()
                await self.task_limit_queue.put(0)
                try:
                    task = asyncio.create_task(handler(job()))
                    self.tasks.append(task)
                    task.add_done_callback(self.__task_callback)
                except Exception as e:
                    logging.exception(f'__deal_queue:{name}:' + str(datetime.now()), exc_info=e)
                await self.task_limit_queue.get()
            del self.setting[name]
        if queue:
            del self.queues[name]

    async def __deal_queue(self):
        setting_dict = self.setting()
        while self.running:
            job: BaseData = await self.get()
            if setting_dict.get(job.name) and self.queues.get(job.name):
                await self.queues[job.name].put(job)

    async def put(self, **kwargs) -> None:
        await super().put(BaseData(**kwargs))

    async def stop(self):
        self.running = False
        for key, queue in self.queues.items():
            await queue.put(BaseData(name=key))
        await self.put(name='stop')
        await asyncio.wait(self.task_futures)
        if self.tasks:
            await asyncio.wait(self.tasks)

    async def __call__(self):
        task_tag = self.setting.task_tag or 'default'
        while self.running and self.setting.redis:
            redis_job = await self.setting.redis.brpop(task_tag)
            await worker.put(**json_friendly_loads(redis_job))


if __name__ == '__main__':
    async def test(job: Dict):
        print('test', job)


    handlers = {'test': test, 'test1': test, 'test2': test}
    task_setting = TaskSetting({}, handlers)
    worker = WorkerQueue(list(handlers.keys()), task_setting)


    async def main():
        count = 0
        while count < 10:
            await worker.put(name='test', data=random_str(32))
            await worker.put(name='test1', data=random_str(32))
            await worker.put(name='test2', data=random_str(32))
            await asyncio.sleep(0.1)
            count += 1
        await worker.stop()


    asyncio.get_event_loop().run_until_complete(main())
