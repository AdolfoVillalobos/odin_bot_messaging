import os
import asyncio
import logging

from dotenv import load_dotenv
from odin_messaging_bot.streaming_bot import MessagingBot


logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s:%(asctime)s:%(message)s")


async def main():

    nats_url = os.getenv("NATS_URL")
    stan_cluster_id = os.getenv("STAN_CLUSTER_ID")
    stan_client_id = os.getenv("STAN_CLIENT_ID")
    pod_name = os.getenv("POD_NAME")

    print(nats_url)

    ms1 = MessagingBot(botname="Accountant", nats_url=nats_url,
                       stan_cluster_id=stan_cluster_id, stan_client_id=stan_client_id, pod_name=2)
    ms2 = MessagingBot(botname="Accountant", nats_url=nats_url,
                       stan_cluster_id=stan_cluster_id, stan_client_id=stan_client_id, pod_name=1)

    await ms1.connect_nats_streaming(max_pub_acks_inflight=512)
    await ms2.connect_nats_streaming(max_pub_acks_inflight=512)

    async def cb(message):
        await ms1.sc.ack(message)
        logging.info(message.data)

    await ms2.publish(subject="hey", payload=b"heey", ack_wait=12)
    await ms1.subscribe(subject="hey", cb=cb, ack_wait=2, max_inflight=512, start_at="first")

    # await ms1.await_for_ping(microservice_channel="AccountantMicroservice")
    # await ms2.request_pong(microservice_channel="AccountantMicroservice")


if __name__ == "__main__":

    load_dotenv(".env")

    asyncio.run(main())
