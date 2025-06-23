import os
import json
import asyncio
import aio_pika

from moderation import detect_banned_words

AMQP_URL = os.getenv("AMQP_URL")
QUEUE_IN = "ad-moderation-requested-event"
ROUTING_RESULT = "ad-moderated-event"

async def amqp_worker():
    connection = await aio_pika.connect_robust(AMQP_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_IN, durable=True)

    result_queue = await channel.declare_queue(ROUTING_RESULT, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    payload = json.loads(message.body.decode())
                except json.JSONDecodeError:
                    continue

                ad_id = payload.get("adId")
                content = payload.get("content", "")
                print(f"Got event id : {ad_id} ")
                if not ad_id:
                    continue
                result = detect_banned_words(content)

                event = {
                    "adId": ad_id,
                    "response": {
                        "bannedWordsDetected": result
                    }
                }

                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(event).encode(),
                        content_type="application/json"
                    ),
                    routing_key=ROUTING_RESULT
                )
                print(f"Published event for id {ad_id}")