import json
import random
import asyncio
import logging

from dataclasses import dataclass, field

from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s:%(asctime)s:%(message)s")


@dataclass
class MessagingBot:
    botname: str
    nats_url: str
    stan_cluster_id: str
    stan_client_id: str
    pod_name: str
    nc: NATS = field(default_factory=NATS)
    sc: STAN = field(default_factory=STAN)

    async def connect_nats_streaming(self):
        logging.info("Connecting Bot to NATS Streaming")
        try:
            random_number = random.randint(0, 1000)
            await self.nc.connect(servers=[self.nats_url])
            await self.sc.connect(
                cluster_id=self.stan_cluster_id,
                client_id=f"{self.stan_client_id}_{self.pod_name}_{random_number}",
                nats=self.nc,
            )
            logging.info("NATS Streaming Connected")
        except Exception as err:
            logging.error(err)

    async def cb_ack(self, message):
        logging.info(f"Recived ack: {message.guid}")

    async def subscribe(self, subject, durable_name=None, cb=None, start_at=None):
        sc = self.sc
        await sc.subscribe(
            subject=subject,
            durable_name=durable_name,
            cb=cb,
            manual_acks=True,
            start_at=start_at,
        )

    async def publish(self, subject, payload):
        sc = self.sc
        await sc.publish(subject=subject, payload=payload, ack_handler=self.cb_ack)

    async def close(self):
        await self.sc.close()
        await self.nc.close()

    async def unsuscribe(self):
        await self.sc.unsubscribe()

    async def retry_message(self, subject, failed_message):
        new_message = json.dumps(failed_message).encode()
        await asyncio.sleep(self.WAIT_RETRY_MESSAGE)
        await self.publish(subject, new_message)
