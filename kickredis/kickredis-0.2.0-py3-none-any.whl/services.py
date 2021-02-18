import logging
import asyncio
import lightbus.api

from lightbus.transports.redis.event import RedisEventTransport
from kickredis.registry import Question, QuestionHandle
from kickredis.runtime import kicker_runtime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d - %(name)s/%(threadName)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("kicker.services")


class AnalyticsService(lightbus.Api):
    event_transport = RedisEventTransport(service_name="", consumer_name="")

    def __init__(self):
        self.qn = 0
        self.questions_map = {}

    class Meta:
        name = "AnalyticsService"

    async def new_question(self, query, is_start) -> QuestionHandle:
        return await self.run_question()

    async def run_question(self):
        log.debug("run_question")
        q = Question(self._gen_id())
        task = asyncio.create_task(q.run(self.event_transport))
        self.questions_map[q.id] = task
        return q.getHandle()

    def _gen_id(self) -> str:
        self.qn += 1
        return f"q_id_{self.qn}"


async def runFlow():
    bus = lightbus.create()
    bus.client.register_api(AnalyticsService())
    await bus.client.start_worker()
    log.info("==== Kick Runtime Started ====")


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(runFlow())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown")


if __name__ == "__main__":
    # asyncio.run (main1(), debug=True)
    main()
