import asyncio

reports = [
    {"name": "Алексей Иванов", "report": "Отчет о прибылях и убытках", "load_time": 5},
    {"name": "Мария Петрова", "report": "Прогнозирование движения денежных средств", "load_time": 4},
    {"name": "Иван Смирнов", "report": "Оценка инвестиционных рисков", "load_time": 3},
    {"name": "Елена Кузнецова", "report": "Обзор операционных расходов", "load_time": 2},
    {"name": "Дмитрий Орлов", "report": "Анализ доходности активов", "load_time": 10}
]


async def download_data(report):
    if report["name"] == "Дмитрий Орлов":
        try:
            # cancel asap, no await for loading
            await cancel_task(asyncio.current_task())
        # catch an error due to cancellation
        except asyncio.CancelledError:
            print(
                f"Загрузка отчета {report['report']} для пользователя {report['name']} остановлена. "
                f"Введите новые данные",
            )
    else:
        # emulate downloading
        await asyncio.sleep(report["load_time"])
        print(f"Отчет: {report['report']} для пользователя {report['name']} готов")


async def cancel_task(task: asyncio.Task):
    # not simultaneously, just an order to cancel
    task.cancel()
    # should propagate on next event loop iteration
    await asyncio.sleep(0)


async def main():
    tasks = [asyncio.create_task(download_data(report)) for report in reports]
    await asyncio.gather(*tasks)


asyncio.run(main())
