"""
Напишите код, который симулирует асинхронную загрузку файлов с проверкой статуса задачи каждую секунду.
У вас есть коллекция из 20 файлов различных типов и размеров, которые нужно "загрузить".
"""

import asyncio

# Словарь файлов и их размеров
files = {
    "file1.mp4": 32,
    "image2.png": 24,
    "audio3.mp3": 16,
    "document4.pdf": 8,
    "archive5.zip": 40,
    "video6.mkv": 48,
    "presentation7.pptx": 12,
    "ebook8.pdf": 20,
    "music9.mp3": 5,
    "photo10.jpg": 7,
    "script11.py": 3,
    "database12.db": 36,
    "archive13.rar": 15,
    "document14.docx": 10,
    "spreadsheet15.xls": 25,
    "image16.gif": 2,
    "audioBook17.mp3": 60,
    "tutorial18.mp4": 45,
    "code19.zip": 22,
    "profile20.jpg": 9
}

NETWORK_SPEED_MB_IN_SEC = 8


async def download_file(filename: str, filesize_in_mb: int, network_speed_mb_in_sec: int):
    download_speed_in_sec = round(filesize_in_mb / network_speed_mb_in_sec, 3)
    print(
        f"Начинается загрузка файла: {filename}, "
        f"его размер {filesize_in_mb} мб, "
        f"время загрузки составит {download_speed_in_sec} сек",
    )
    await asyncio.sleep(download_speed_in_sec)
    print(f"Загрузка завершена: {filename}")


async def monitor_tasks(tasks):
    while True:
        for task in tasks:
            task_status_str = 'завершена' if task.done() else 'в процессе'
            print(f"Задача {task.get_name()}: {task_status_str}, Статус задачи {task.done()}")

        if all(task.done() for task in tasks):
            print("Все файлы успешно загружены")
            break

        await asyncio.sleep(1)  # Проверяем статус задачи каждую секунду


async def main():
    tasks = [
        asyncio.create_task(
            download_file(
                filename=filename,
                filesize_in_mb=filesize,
                network_speed_mb_in_sec=NETWORK_SPEED_MB_IN_SEC,
            ),
            name=filename,
        ) for filename, filesize in files.items()
    ]
    await monitor_tasks(tasks)
    print("Все файлы успешно загружены")

asyncio.run(main())
