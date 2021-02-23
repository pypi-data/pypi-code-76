import asyncio, json, time
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor


class BaseData(object):
    def __init__(self, **kwargs):
        self += kwargs
        # 记录实例化时间，用于排序
        self.__created_at = time.time()

    def __add__(self, other: Dict):
        """ 使用加法的形式添加数据
        tmp = BaseData()
        tmp += {'a': 1}
        """
        if not isinstance(other, Dict):
            raise Exception('BaseData need dict')
        for key, val in other.items():
            self[key] = val
        return self

    def __lt__(self, other):
        """ 根据时间排序，默认升序排列 """
        return self.__created_at < other.__created_at

    def __getattribute__(self, item):
        """ 当访问的属性不存在时，返回 None """
        try:
            return super().__getattribute__(item)
        except Exception:
            return None

    def __getitem__(self, item):
        """ 该函数使实例可以像字典一样为属性赋值 """
        return getattr(self, item)

    def __setitem__(self, key, value):
        """ 该函数使实例可以像字典一样获取属性值 """
        setattr(self, key, value)

    def __delitem__(self, key):
        """ 该函数使实例可以像字典一样删除属性 """
        delattr(self, key)

    def __call__(self):
        """ 使实例可执行，返回一个属性字典 """
        ret = dict()
        for item in dir(self):
            if not item.startswith('_'):
                ret[item] = getattr(self, item)
        return ret

    def __str__(self):
        """ 序列化实例字典 """
        return json.dumps(self())


class Job:
    def __init__(self, _run=None, _callback=None, **kwargs):
        self.params = BaseData(_run=_run, _callback=_callback, **kwargs)

    def __call__(self):
        if self.params._run and asyncio.iscoroutinefunction(self.params._run):
            return asyncio.create_task(self.params._run(self.params))

    def __str__(self):
        return self.params.__str__()

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, item):
        return self.params[item]

    def __add__(self, other):
        self.params.__add__(other)
        return self


def async_callback(f):
    def wrap_callback(self, task):
        self.tasks.append(asyncio.create_task(f(self, task)))

    return wrap_callback


class Worker(asyncio.Queue):
    def __init__(self, worker_limit=1000, queue_limit=100):
        super().__init__(worker_limit)
        self.tasks = list()
        self.run_able = True
        self.put_able = True
        self.limit_queue = asyncio.Queue(queue_limit)
        self.main_task = asyncio.create_task(self.run())

    @async_callback
    async def __default_callback(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
        job: Job = task.result()
        if job and job._callback:
            if asyncio.iscoroutinefunction(job._callback):
                await job._callback(job)
            else:
                job._callback(job)
        await self.limit_queue.get()

    def shutdown_put(self):
        self.put_able = False

    async def stop(self):
        self.shutdown_put()
        while True:
            if self.empty(): break
            await asyncio.sleep(1)

        self.run_able = False
        await super().put(None)
        self.tasks.append(self.main_task)
        await asyncio.wait(self.tasks)
        self.tasks.clear()

    async def put(self, item) -> None:
        if self.put_able:
            await super(Worker, self).put(item)

    async def run(self):
        while self.run_able:
            job: Job = await self.get()
            if job:
                await self.limit_queue.put(0)
                task = job()
                if task:
                    self.tasks.append(task)
                    task.add_done_callback(self.__default_callback)


if __name__ == '__main__':
    async def do(job: Job):
        print('do job')
        return job


    async def callback(job: Job):
        print(f'callback: {job}')


    async def main():
        worker = Worker()
        for i in range(10000):
            job = Job(_run=do, _callback=callback, id=i)
            await worker.put(job)
        await worker.stop()


    asyncio.get_event_loop().run_until_complete(main())
