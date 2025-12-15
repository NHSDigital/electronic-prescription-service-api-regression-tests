#!/usr/bin/env python3
"""
API Uptime Monitor - Runner Script

This script runs continuous monitoring of NHS APIs (e.g., PfP, EPS, etc.)
to assess uptime, performance, and behaviour during endpoint switchover events.

ACCEPTANCE CRITERIA:
- Provides automated test traffic to the PfP API in INT environment
- Monitors PfP service for the duration of endpoint switchover
- Records PfP API performance for the entire switchover period
- Generates impact report on PfP performance during switchover

USAGE:
    Basic monitoring (1 request per second to PfP in INT environment):
        poetry run python scripts/run_uptime_monitor.py

    For more options, use --help:
        poetry run python scripts/run_uptime_monitor.py --help

CSV OUTPUT FORMAT:
    Columns:
    - timestamp: ISO 8601 timestamp of request
    - status_code: HTTP status code (or ERROR if exception occurred)
    - response_time_ms: Response time in milliseconds
    - success: Boolean indicating if request was successful (200 status)
    - error_message: Error details (empty if successful)
    - endpoint_url: Full URL of the endpoint being monitored

    The CSV file is flushed after each write, ensuring data preservation
    even if the script crashes or is force-terminated.

STOPPING THE MONITOR:
    Press Ctrl+C to gracefully stop monitoring. The script will:
    1. Stop making requests
    2. Display summary statistics
    3. Preserve all data in the CSV file
    4. Exit cleanly

OUTPUT FILES:
    - CSV file: reports/uptime_monitor_<product>_YYYYMMDD_HHMMSS.csv
    - Console: Real-time monitoring output with statistics
"""

import argparse
import asyncio
import csv
import datetime
import os
import signal
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


@dataclass
class Report:
    """Container for monitoring statistics and metrics."""

    endpoint_url: str
    request_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    response_times: List[float] = field(default_factory=list)


@dataclass
class EndpointResult:
    status_code: str
    response_time_ms: float
    error_message: str = ""
    success: bool = field(init=False)
    timestamp: str = field(
        init=False, default_factory=lambda: datetime.datetime.now().isoformat()
    )

    def __post_init__(self):
        self.success = self.error_message == ""

    def to_csv_row(self, endpoint_url: str):
        """Return a list suitable for CSV writing."""
        return [
            self.timestamp,
            self.status_code,
            f"{self.response_time_ms:.2f}",
            self.success,
            self.error_message,
            endpoint_url,
        ]


def calculate_interval_from_rpm(rpm: int) -> float:
    """Convert requests per minute to interval in seconds."""
    return 60.0 / rpm


def get_endpoint_url(product: str, env: str) -> str:
    """Get the endpoint URL for the specified product and environment."""
    if product == "PFP-APIGEE":
        return f"https://{env}.api.service.nhs.uk/prescriptions-for-patients"
    raise ValueError(
        f"Unsupported product: {product}. Only PFP-APIGEE is currently supported."
    )


def validate_env(product: str, options: Dict):
    if options.get("interval") and options.get("rpm"):
        print("Error: Cannot specify both --interval and --rpm")
        sys.exit(1)

    product_key = (
        product.replace("-", "_").replace("APIGEE", "").replace("AWS", "").strip("_")
    )
    if product_key == "PFP":
        product_key = "PFP"

    client_id_key = f"{product_key}_CLIENT_ID"
    client_secret_key = f"{product_key}_CLIENT_SECRET"

    client_id = os.getenv(client_id_key)
    client_secret = os.getenv(client_secret_key)

    if not client_id or not client_secret:
        print(f"\nERROR: Missing required environment variables for {product}!")
        print(f"Please set {client_id_key} and {client_secret_key} in your .env file")
        print("See template.env for the required format")
        sys.exit(1)

    print(f"Using credentials: {client_id_key}={client_id[:10]}...")
    return client_id, client_secret


def display_summary_statistics(
    csv_filename: str,
    target_interval: float,
    actual_duration: float,
    report: Report,
):
    """Display summary statistics after monitoring ends."""
    separator = "=" * 80
    print(f"\n{separator}")
    print("Monitoring stopped by user")
    print(separator)

    if report.request_count > 0:
        uptime_pct = (report.success_count / report.request_count) * 100
        avg_response = (
            sum(report.response_times) / len(report.response_times)
            if report.response_times
            else 0
        )
        min_response = min(report.response_times) if report.response_times else 0
        max_response = max(report.response_times) if report.response_times else 0

        # Calculate percentiles
        sorted_times = sorted(report.response_times) if report.response_times else []
        p95 = sorted_times[int(len(sorted_times) * 0.95)] if sorted_times else 0
        p99 = sorted_times[int(len(sorted_times) * 0.99)] if sorted_times else 0

        # Calculate actual interval and RPM
        actual_interval = (
            actual_duration / report.request_count if report.request_count > 0 else 0
        )
        actual_rpm = (
            (report.request_count / actual_duration) * 60 if actual_duration > 0 else 0
        )
        target_rpm = 60.0 / target_interval if target_interval > 0 else 0

        print(f"\n{separator}")
        print("MONITORING SUMMARY")
        print(separator)
        print(f"Total Requests:      {report.request_count}")
        print(f"Successful:          {report.success_count} ({uptime_pct:.2f}%)")
        failed_pct = (report.failure_count / report.request_count) * 100
        print(f"Failed:              {report.failure_count} ({failed_pct:.2f}%)")
        print("\nResponse Times (ms):")
        print(f"  Average:           {avg_response:.2f}ms")
        print(f"  Minimum:           {min_response:.2f}ms")
        print(f"  Maximum:           {max_response:.2f}ms")
        print(f"  95th Percentile:   {p95:.2f}ms")
        print(f"  99th Percentile:   {p99:.2f}ms")
        print("\nThroughput:")
        print(f"  Target Interval:   {target_interval:.2f}s ({target_rpm:.1f} req/min)")
        print(f"  Actual Interval:   {actual_interval:.2f}s ({actual_rpm:.1f} req/min)")
        print(f"  Total Duration:    {actual_duration:.1f}s")
        print(f"\nDetailed log saved to: {csv_filename}")
        print(f"{separator}\n")


def get_command(options: Dict) -> List[str]:
    arm64_setting = os.getenv("ARM64", "False")

    command = [
        "behave",
        "-D",
        f"product={options['product']}",
        "-D",
        f"env={options['env']}",
        "-D",
        f"arm63={arm64_setting}",
        "-D",
        f"output_dir={options['output_dir']}",
        "--tags",
        "uptime_monitor",
        "--no-capture",
        "--no-logcapture",
        "-f",
        "plain",
        options["feature_file"],
    ]
    return command


def get_config(args: list[str]) -> Dict:
    parser = argparse.ArgumentParser(
        description="Run API uptime monitor for endpoint switchover testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--product",
        default="PFP-APIGEE",
        help="Product to monitor. Options: PFP-APIGEE, EPS-FHIR, EPS-FHIR-PRESCRIBING, "
        "EPS-FHIR-DISPENSING, PSU, CPTS-FHIR",
    )

    parser.add_argument(
        "--env",
        default="int",
        help="Environment to monitor (default: int). Options: internal-dev, internal-qa, int, ref",
    )

    parser.add_argument(
        "--interval",
        type=float,
        help="Request interval in seconds (e.g., 1.0 for 1 request per second). "
        "Mutually exclusive with --rpm",
    )

    parser.add_argument(
        "--rpm",
        type=int,
        help="Requests per minute (e.g., 30 for 30 requests/minute). "
        "Mutually exclusive with --interval",
    )

    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Output directory for CSV files (default: reports)",
    )

    parser.add_argument(
        "--feature-file",
        default="features/pfp/view_prescriptions.feature",
        help="Feature file to use for monitoring (default: features/pfp/view_prescriptions.feature)",
    )

    return vars(parser.parse_args())


def get_interval(options: Dict) -> float:
    if options.get("rpm"):
        interval = calculate_interval_from_rpm(options["rpm"])
        print(f"Using --rpm {options['rpm']} (interval: {interval:.1f} seconds)")
    elif options.get("interval"):
        interval = options["interval"]
    else:
        # Default to 1 request per second
        interval = 1.0
    return interval


def init_report_file(product: str, output_dir: str) -> str:
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    product_slug = product.replace("-", "_").lower()
    csv_filename = os.path.join(
        output_dir, f"uptime_monitor_{product_slug}_{timestamp_str}.csv"
    )

    os.makedirs(output_dir, exist_ok=True)

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            [
                "timestamp",
                "status_code",
                "response_time_ms",
                "success",
                "error_message",
                "endpoint_url",
            ]
        )
    return csv_filename


async def execute_request(
    command: List[str],
    timeout: int,
    report: Report,
    csv_filename: str,
    request_number: int,
) -> None:
    """
    Execute a single monitoring request asynchronously.

    Args:
        command: The behave command to execute
        timeout: Timeout for the request in seconds
        report: Report object to update with results
        csv_filename: Path to CSV file for logging
        request_number: Sequential request number for display
    """
    start_time = time.time()

    try:
        # Run behave asynchronously
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            return_code = process.returncode

            endpoint_result = EndpointResult(
                status_code="PASS" if return_code == 0 else "FAIL",
                response_time_ms=(time.time() - start_time) * 1000,
                error_message="" if return_code == 0 else stderr.decode()[:100],
            )

            if endpoint_result.success:
                report.success_count += 1
            else:
                report.failure_count += 1

            report.response_times.append(endpoint_result.response_time_ms)

        except asyncio.TimeoutError:
            process.kill()
            await process.wait()

            endpoint_result = EndpointResult(
                status_code="TIMEOUT",
                response_time_ms=(time.time() - start_time) * 1000,
                error_message=f"Request timed out after {timeout} seconds",
            )
            report.failure_count += 1
            report.response_times.append(endpoint_result.response_time_ms)

    except Exception as e:  # pylint: disable=broad-except
        endpoint_result = EndpointResult(
            status_code="ERROR",
            response_time_ms=(time.time() - start_time) * 1000,
            error_message=str(e)[:100],
        )
        report.failure_count += 1
        report.response_times.append(endpoint_result.response_time_ms)

    # Write to CSV immediately (with flush for crash safety)
    with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(endpoint_result.to_csv_row(report.endpoint_url))
        csvfile.flush()
        os.fsync(csvfile.fileno())

    # Console output
    status_symbol = "✓" if endpoint_result.success else "✗"
    uptime_pct = (report.success_count / report.request_count) * 100
    avg_response_time = (
        sum(report.response_times) / len(report.response_times)
        if report.response_times
        else 0
    )

    print(
        f"[{endpoint_result.timestamp}] {status_symbol} Request #{request_number} | "
        f"Status: {endpoint_result.status_code} | "
        f"Response: {endpoint_result.response_time_ms:.2f}ms | "
        f"Uptime: {uptime_pct:.2f}% | "
        f"Avg: {avg_response_time:.2f}ms"
    )

    if not endpoint_result.success:
        print(f"  └─ Error: {endpoint_result.error_message}")


async def run_monitoring_loop_async(
    env: str, product: str, command: List[str], interval: float, csv_filename: str
) -> None:
    """
    Execute the monitoring loop asynchronously, allowing concurrent requests.

    Args:
        env: Environment to monitor
        product: Product to monitor
        command: The behave command to execute
        interval: Time to wait between launching requests (seconds)
        csv_filename: Path to CSV file for logging
    """
    separator = "=" * 80
    print(f"\n{separator}")
    print("Starting API Uptime Monitor (Async Mode)")
    print(f"Product: {product}")
    print(f"Environment: {env}")
    print(f"Interval: {interval} seconds")
    print(f"Output CSV: {csv_filename}")
    print("Press Ctrl+C to stop monitoring and view summary")
    print(f"{separator}\n")

    endpoint_url = get_endpoint_url(product, env)
    report = Report(endpoint_url=endpoint_url)
    timeout = 30  # Timeout for each request in seconds
    monitoring_start_time = time.time()

    while True:
        report.request_count += 1
        request_number = report.request_count

        # Launch request asynchronously (doesn't block)
        asyncio.create_task(
            execute_request(command, timeout, report, csv_filename, request_number)
        )

        # Wait for interval before launching next request
        try:
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            # Wait for pending requests to complete
            print("\n\nStopping monitor, waiting for pending requests...")
            await asyncio.sleep(2)

            monitoring_end_time = time.time()
            actual_duration = monitoring_end_time - monitoring_start_time
            display_summary_statistics(
                csv_filename,
                interval,
                actual_duration,
                report,
            )
            break


def run_monitoring_loop(
    env: str, product: str, command: List[str], interval: float, csv_filename: str
) -> None:
    """
    Wrapper to run the async monitoring loop with proper signal handling.

    Args:
        env: Environment to monitor
        product: Product to monitor
        command: The behave command to execute
        interval: Time to wait between requests (seconds)
        csv_filename: Path to CSV file for logging
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    main_task = loop.create_task(
        run_monitoring_loop_async(env, product, command, interval, csv_filename)
    )

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        main_task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(main_task)
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()


def main():
    options = get_config(sys.argv)
    validate_env(options["product"], options)
    run_monitoring_loop(
        options["env"],
        options["product"],
        get_command(options),
        get_interval(options),
        init_report_file(options["product"], options["output_dir"]),
    )


if __name__ == "__main__":
    main()
