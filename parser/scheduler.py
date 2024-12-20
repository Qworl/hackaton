import asyncio
from apscheduler.schedulers import asyncio as asyncio_scheduler

import parse


async def main():
    scheduler = asyncio_scheduler.AsyncIOScheduler()
    scheduler.add_job(parse.parse, 'interval', seconds=5 * 60)
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()


asyncio.run(main())
