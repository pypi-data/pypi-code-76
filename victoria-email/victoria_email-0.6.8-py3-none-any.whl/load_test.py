"""load_test

The functionality of the load testing command.
Allows sending emails to an endpoint at a specified rate for a specified time.

Interfaces with an Azure function on the backend (https://github.com/glasswall-sre/going-postal)
that exposes an HTTP endpoint for sending mail.

The backend will return HTTP 200 in the event of a successful send, and 5xx
otherwise.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import asyncio
import random

from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from itertools import cycle

import aiohttp
import roundrobin

from .core.util import generate_random_numbers, generate_random_uuids
from .schemas import LoadTestConfig, Distribution, Function, EmailConfig

@dataclass
class TestResult:
    """Data class to store the result of a single test.

    Attributes:
        status (int): The HTTP status code returned from the Azure function.
        message (str): The message returned from the Azure function.
        time (datetime): The time this test result was created.
        function_endpoint (Function): function endpoint used
    """
    status: int
    message: str
    time: datetime
    function_endpoint: Function


async def run_single_test(session: aiohttp.ClientSession, endpoint: str,
                          recipient: str, sender: str, function_endpoint: Function,
                          load_test_config: LoadTestConfig) -> TestResult:
    """Asynchronously run a single test by async invoking the backend Azure
    function. Return a TestResult object containing the results of the test.

    Args:
        session: The opened aiohttp session used for all requests.
        endpoint: The SMTP endpoint to send mail to.
        recipient: The email address to send to.
        sender: The email address to send from.
        function_endpoint: Function endpoint and function code
        load_test_config: The config of the load tester.

    Returns:
        TestResult: The result of the test.
    """
    # extract the endpoint and port from the given endpoint
    split_endpoint = endpoint.split(":")
    endpoint = split_endpoint[0]
    port = split_endpoint[1] if len(
        split_endpoint) > 1 else "25"  # default port 25

    # build the request body with the data provided

    req_body = {
        "endpoint": endpoint,
        "port": int(port),
        "tenant_ids": [str(tenant_id) for tenant_id in load_test_config.tenant_ids],
        "recipient": recipient,
        "sender": sender,
        "timeout": load_test_config.timeout,
        "load": {
            "distribution": [
                {
                    "file": str(distribution.file),
                    "weight": int(distribution.weight)
                }
                for distribution in load_test_config.load.distribution
            ],
            "attachment_count": [int(x) for x in load_test_config.load.attachment_count]
        }
    }

    # perform the POST to run the test
    try:
        async with session.post(
                function_endpoint.function,
                json=req_body,
                params={"code": function_endpoint.mail_send_function_code},
                timeout=aiohttp.ClientTimeout(total=None)) as resp:
            time_now = datetime.now()
            return TestResult(resp.status, await resp.text(), time_now, function_endpoint)
    except aiohttp.ClientConnectorError as error:
        time_now = datetime.now()
        return TestResult(504, str(error), time_now, function_endpoint)

    except Exception as error:
        return TestResult(0, str(error), time_now, function_endpoint)


async def perform_load_test(frequency: int, endpoint: str, duration: int,
                            recipient: str, sender: str, tenant_ids: list,
                            load_test_config: LoadTestConfig, plugin_cfg: EmailConfig) -> None:
    """Asynchronously run a load test with a given frequency and duration.

    Args:
        frequency: How many tests to run per second.
        endpoint: The SMTP endpoint to send to.
        duration: How long in seconds to run the test.
        recipient: The email address to send to.
        sender: The email address to send with.
        tenant_ids: Tenant ids.
        load_test_config: The config for the load tester.
    """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(
            total=None)) as session:
        # between each test we wait for 1/frequency seconds
        wait_interval = 1.0 / frequency
        if not tenant_ids:
            tenant_ids = load_test_config.tenant_ids if len(
                load_test_config.tenant_ids) > 0 else generate_random_uuids()
        distributions = Distribution.get_random_distributions(load_test_config, plugin_cfg)
        load_test_config.load.attachment_count = load_test_config.load.attachment_count if None else generate_random_numbers()
        load_test_config.tenant_ids = tenant_ids

        # perform the tests spread out along the time period

        successful_tests = 0
        unresolvable_exceptions = []
        total_tests = int(frequency * duration)
        number_of_intervals = total_tests
        errors = True
        retry_count = 0
        max_retries = len(load_test_config.mail_send_function_endpoints)
        while errors and retry_count < max_retries:
            tasks = []
            if load_test_config.mail_send_function_endpoints:
                # functions_cycle = cycle(load_test_config.mail_send_function_endpoints)
                intervals_processed = 0
                functions_cycle = roundrobin.basic(load_test_config.mail_send_function_endpoints)
                while intervals_processed < number_of_intervals:
                    # Create a task to run a single test asynchronously
                    function_endpoint = functions_cycle()
                    load_test_config.load.distribution = [random.choice(distributions)]
                    tasks.append(
                        asyncio.create_task(
                            run_single_test(
                                session,
                                endpoint,
                                recipient,
                                sender,
                                function_endpoint,
                                load_test_config
                            )
                        )
                    )

                    intervals_processed += 1
                    percent_done = (intervals_processed / number_of_intervals) * 100
                    print(f"{intervals_processed} / {number_of_intervals}\t\t\t\t{percent_done:02f}%")
                    await asyncio.sleep(wait_interval)

            else:
                print("\n\nFunction endpoints aren't available")

            print("\n")
            # Wait for the tasks to complete
            if not tasks:
                errors = False
                continue
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            test_results = []

            for task in done:
                # If there were any exceptions, raise the first one
                error = task.exception()
                if error is not None:
                    raise error
                # Otherwise add the result to the list
                test_results.append(task.result())

            # Compile the amount of successful tests to show the user
            num_successful = reduce(lambda cur, result: cur + (1 if result.status == 200 else 0), test_results, 0)
            successful_tests += num_successful
            print(f"{num_successful} / {number_of_intervals} tests were successfully sent")

            # If there were any non-successful tests, print the reasons
            errors_range = list(range(400, 500)) + [504]
            if num_successful < number_of_intervals:

                failed_sends = [result for result in test_results if result.status != 200]
                number_of_intervals = len(
                    [test for test in failed_sends if test.status in errors_range])

                unresolvable_exceptions += [test for test in failed_sends if test.status not in errors_range]
                removed_endpoints = []
                # FOR DEBUG
                # print("\nReasons for failures:")
                for failed_result in failed_sends:
                    # FOR DEBUG
                    # print(
                    #     f"\t{failed_result.time.isoformat()} - {failed_result.status} error - {failed_result.message}")
                    # print(
                    #     f"\t{failed_result.time.isoformat()} - {failed_result.status} status ")
                    # if not failed_result.message:
                    #     print(failed_result)

                    if failed_result.status in errors_range and failed_result.function_endpoint in load_test_config.mail_send_function_endpoints:
                        load_test_config.mail_send_function_endpoints.remove(failed_result.function_endpoint)
                        removed_endpoints.append(failed_result.function_endpoint)
                print("\n")
                for function_endpoint in removed_endpoints:
                    print(f'{function_endpoint.function} - Failed to send tests')
                if not number_of_intervals:
                    break
            else:
                errors = False

        print(f"total {successful_tests} / {total_tests} tests were successfully sent")

        # FOR DEBUG
        if len(unresolvable_exceptions):
            print("\nUnresolvable failures:")

            for failed_result in unresolvable_exceptions:
                print(f"\t{failed_result.time.isoformat()} - {failed_result.status} error - {failed_result.message}")

        if not retry_count < max_retries:
            print('\nMax retries exceeded')
