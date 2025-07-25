import logging
import asyncio
import os
import time
from PIL import Image
from src.connectors.celery_connector import celery_app
from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager


@celery_app.task
def test_task(example: str):
    time.sleep(5)
    print(example)


@celery_app.task
def resize_image(image_path: str):
    logging.debug(f"Вызывается функция resize_image c {image_path=}")
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)

        logging.info(
            f"Изображение сохранено в следующих размерах {size} в папке {output_folder}"
        )


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.booking.get_bookings_with_today_checkin()
        logging.debug(f"{bookings=}")


@celery_app.task(name="booking_today_checkin")
def send_email_to_users_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
