import os
import asyncio
import logging
import ujson


from dotenv import load_dotenv
from odin_messaging_bot.jetstream_bot import JetStreamMessagingBot

from nats.errors import TimeoutError

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s:%(asctime)s:%(message)s")


async def main():

    nats_url = os.getenv("NATS_URL")

    async def cb(msg):
        await msg.ack()

    ms1 = JetStreamMessagingBot(botname="Accountant", nats_url=nats_url)
    ms2 = JetStreamMessagingBot(botname="BotOperator", nats_url=nats_url)

    await ms1.connect()
    await ms2.connect()

    await ms1.js.add_stream(name="foo", subjects=["foo"])

    for _ in range(0, 10):
        ack = await ms1.js.publish("foo",  stream="foo", payload="hello world".encode())
        logging.info(f"First 10 msgs: {ack.seq}")

    await ms2.js.subscribe(subject="foo", stream="foo", cb=cb)
    for _ in range(0, 10):
        ack = await ms1.js.publish("foo",  stream="foo", payload="bye world".encode())
        logging.info(f"Last 10 msgs: {ack.seq}")

    await ms1.nc.close()


if __name__ == "__main__":

    load_dotenv(".env")

    asyncio.run(main())
