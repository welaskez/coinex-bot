import taskiq_aiogram
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from core.config import settings

broker = AioPikaBroker(url=settings.rmq.url)
scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])

taskiq_aiogram.init(broker, dispatcher="main:dp", bot="main:bot")
