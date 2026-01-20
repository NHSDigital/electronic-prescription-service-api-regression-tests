import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout, redirect_stderr
import io
import logging
import os
import signal
import time
import behave.__main__ as behave_main

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


def run_behave_sync(command) -> tuple[int, str, str]:
    """Run Behave synchronously and capture stdout/stderr.

    Returns: (return_code, stdout_str, stderr_str)
    """
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    return_code = 1
    # Remove leading 'behave' token if present
    args = [a for a in command if a != "behave"]
    with redirect_stdout(buf_out), redirect_stderr(buf_err):
        result = behave_main.main(args)
    if isinstance(result, int):
        return_code = result
    elif isinstance(result, bool):
        return_code = 0 if result else 1
    else:
        return_code = 0
    return return_code, buf_out.getvalue(), buf_err.getvalue()


async def worker(
    queue: asyncio.Queue, executor: ThreadPoolExecutor, command, report
) -> None:
    """Async worker that consumes task_ids from the queue and runs checks sequentially
    in a single thread (via the provided executor)."""
    loop = asyncio.get_running_loop()
    while True:
        task_id = await queue.get()
        start_time = time.perf_counter()
        return_code, stdout_str, stderr_str = await loop.run_in_executor(
            executor, run_behave_sync, command
        )

        endpoint_result = EndpointResult(
            status=Status.PASS if return_code == 0 else Status.FAIL,
            response_time_ms=(time.perf_counter() - start_time) * 1000,
            error_message="" if return_code == 0 else (stderr_str or stdout_str)[:200],
        )

        await report.record_result(
            endpoint_result.success, endpoint_result.response_time_ms
        )
        print(
            f"EEEEEE task {task_id} completed in {endpoint_result.response_time_ms:.0f}ms"
        )
        queue.task_done()


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

    # Single-threaded executor to serialize blocking workloads (Behave-like)
    executor = ThreadPoolExecutor(max_workers=1)

    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    enqueued = 0
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

    # Start worker consuming from the queue
    worker_task = asyncio.create_task(worker(queue, executor, command, report))

    try:
        print("AAAAAA Starting async hello producer. Press Ctrl+C to stop.")
        while not stop_event.is_set():
            enqueued += 1
            print(f"BBBBBB hello (task {enqueued})")
            await queue.put(enqueued)
            print("DDDD Waiting for interval", interval)
            await asyncio.sleep(interval)
    finally:
        print("YYYY Waiting for queued tasks to complete...")
        # Wait for the queue to be fully processed
        await queue.join()
        # Stop the worker
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        executor.shutdown(wait=False)

        elapsed_wall = time.perf_counter() - start_wall
        elapsed_cpu = time.process_time() - start_cpu
        print(
            f"ZZZZZZ Stopped. tasks_enqueued={enqueued}, execution_time={elapsed_cpu:.3f}s, "
            f"elapsed_time={elapsed_wall:.3f}s"
        )


if __name__ == "__main__":
    asyncio.run(main())
