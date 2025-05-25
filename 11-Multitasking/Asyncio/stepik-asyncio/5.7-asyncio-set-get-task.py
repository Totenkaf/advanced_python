"""
Данный код устанавливает такое же имя задачи, как и скачанный файл,
это может облегчить отладку кода либо сделать код более информативным.
"""

import asyncio
import aiohttp


async def download_file(url):
    async with aiohttp.ClientSession() as session:  # Создание асинхронного HTTP-соединения
        async with session.get(url) as response:  # Отправка асинхронного GET-запроса
            filename = response.headers.get("content-disposition")  # Извлечение имени файла из заголовков
            if filename:
                filename = filename.split("filename=")[1]
            task = asyncio.current_task()
            task.set_name(f"Downloading {filename}")  # Установка имени текущей задачи

            # Открытие файла для записи бинарных данных
            with open(filename, "wb") as f:
                while True:
                    # Чтение и запись в файл содержимого ответа по частям
                    # читаем до тех пор, пока не придет пустой чанк данных
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    # записываем чанк в файл
                    f.write(chunk)
            # Обновление имени текущей задачи после завершения скачивания
            task.set_name(f"Downloaded {filename}")


async def main():
    urls = [
        "<https://www.example.com/file1.txt>",
        "<https://www.example.com/file2.txt>",
        "<https://www.example.com/file3.txt>"
    ]

    tasks = [asyncio.create_task(download_file(url)) for url in urls]
    await asyncio.gather(*tasks)


asyncio.run(main())
