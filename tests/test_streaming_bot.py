# import unittest
# import asyncio
# from dotenv.main import load_dotenv

# from odin_messaging_bot.streaming_bot import MessagingBot

# import nest_asyncio

# nest_asyncio.apply()


# class TestMessagingBot(unittest.IsolatedAsyncioTestCase):
#     async def asyncSetUp(self):
#         load_dotenv(".env")
#         self.loop = asyncio.get_running_loop()
#         credentials = NatsStreamingEnv()
#         self.bot = MessagingBot(botname="ODINTestBot", credentials=credentials)
#         await self.bot.connect_nats_streaming()

#     async def test_connect_nats_streaming(self):
#         self.assertEqual(self.bot.botname, "ODINTestBot")
#         self.assertTrue(self.bot.nc.is_connected)
#         self.assertTrue(self.bot.sc._conn_id != None)

#     async def test_bot_basic_subscriptions(self):
#         msgs = []

#         for i in range(0, 1):
#             await self.bot.publish(subject="hi", payload=b"hello")

#         future = asyncio.Future(loop=self.loop)

#         async def cb(msg):
#             nonlocal future
#             nonlocal msgs
#             msgs.append(msg)
#             if len(msgs) >= 1:
#                 future.set_result(None)

#         await self.bot.subscribe(subject="hi", cb=cb)
#         await asyncio.wait_for(future, 10, loop=self.loop)

#         self.assertEqual(len(msgs), 1)
#         self.assertTrue(True)
