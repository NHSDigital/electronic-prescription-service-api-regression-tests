import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal
import time
import requests

from run_uptime_monitor import (
    EndpointResult,
    Report,
    Status,
    get_command,
    get_config,
    get_endpoint_url,
    get_interval,
    validate_env,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
logger = logging.getLogger(__name__)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
print(f"Log level set to: {log_level}")


async def hello_task(task_id: int, command, report, executor) -> None:
    start_time = time.perf_counter()
    print(f"BBBBBB hello (task {task_id})")

    def make_http_request():
        """Make a blocking HTTP request."""
        try:
            # Use httpbin.org delay endpoint to simulate a slow request (3 seconds)
            response = requests.get("https://httpbin.org/delay/3", timeout=10)
            return response.status_code, response.text[:100], None
        except Exception as e:
            return 500, None, str(e)

    # Run HTTP request in executor to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    status_code, response_text, error = await loop.run_in_executor(
        executor, make_http_request
    )

    endpoint_result = EndpointResult(
        status=Status.PASS if status_code == 200 else Status.FAIL,
        response_time_ms=(time.perf_counter() - start_time) * 1000,
        error_message="" if status_code == 200 else (error or "")[:100],
    )

    await report.record_result(
        endpoint_result.success, endpoint_result.response_time_ms
    )
    print(
        f"EEEEEE task {task_id} completed in {endpoint_result.response_time_ms:.0f}ms"
    )


async def main() -> None:
    start_wall = time.perf_counter()
    start_cpu = time.process_time()

    options = get_config()
    validate_env(options["product"], options)
    interval = get_interval(options)
    endpoint_url = get_endpoint_url(options["product"], options["env"])
    command = get_command(options)
    # csv_filename = init_report_file(options["product"], options["output_dir"])
    report = Report(endpoint_url=endpoint_url)

    # Create a thread pool with enough threads for concurrent execution
    # Each task takes ~3s, so if interval is 1s, we need at least 3-4 threads
    max_concurrent_tasks = max(20, int(10 / interval))
    executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)

    tasks: list[asyncio.Task] = []
    count = 0
    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()

    def _handle_stop() -> None:
        print("XXXX Stopping")
        stop_event.set()

    # Register signal handlers (Linux/Unix). Also handle SIGTERM so we can test.
    try:
        loop.add_signal_handler(signal.SIGINT, _handle_stop)
        loop.add_signal_handler(signal.SIGTERM, _handle_stop)
    except NotImplementedError:
        # Fallback for platforms where asyncio signal handlers aren't supported
        pass

    try:
        print("AAAAAA Starting async hello tasks. Press Ctrl+C to stop.")
        while not stop_event.is_set():
            count += 1
            t = asyncio.create_task(hello_task(count, command, report, executor))
            print("CCCC Started task", count)
            tasks.append(t)
            print("DDDD Waiting for interval", interval)
            await asyncio.sleep(interval)
    finally:
        print(f"YYYY Waiting for {len(tasks)} tasks to complete...")
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        executor.shutdown(wait=False)

        elapsed_wall = time.perf_counter() - start_wall
        elapsed_cpu = time.process_time() - start_cpu
        print(
            f"ZZZZZZ Stopped. tasks_run={count}, execution_time={elapsed_cpu:.3f}s, elapsed_time={elapsed_wall:.3f}s"
        )


if __name__ == "__main__":
    asyncio.run(main())
