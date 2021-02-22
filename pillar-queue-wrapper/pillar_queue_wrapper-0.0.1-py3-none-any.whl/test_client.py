import os

import pytest
import concurrent.futures
import time

from pillar_queue import Queue


def delete_all_messages_from_queue(queue):
    while True:
        message = queue.receive_message(wait_time=1)
        if message is None:
            break


def instantiate_queue(name="testqueue.fifo"):
    q = Queue(
        name=name,
        aws_access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_access_secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    q.wait_for_accuracy = True
    delete_all_messages_from_queue(q)
    return q


def insert_message_into_queue_for_testing(queue):
    queue.send_message()


def test_Queue_init():
    q = instantiate_queue()

    delete_all_messages_from_queue(q)

    assert(q.name == "testqueue.fifo")
    assert(q.aws_default_region == 'us-east-1')
    assert(len(q) == 0)


def test_send_message():
    q = instantiate_queue()
    success = q.send_message(message='hello')
    assert success


def test_equals():
    q = instantiate_queue()
    q2 = instantiate_queue()
    assert(q == q2)


def test_receive_message():
    q = instantiate_queue()
    assert(len(q) == 0)
    message = q.receive_message(wait_time=1, delete_message=True)
    assert(message is None)

    q.send_message('hello')
    message = q.receive_message(wait_time=1, delete_message=True)
    assert(message)
    assert(message.body == 'hello')
    assert(len(q) == 0)

    q.send_message('hello')
    message = q.receive_message(wait_time=1, delete_message=False)
    assert(message)
    assert(message.body == 'hello')
    assert(len(q) == 1)

    message = q.receive_message(wait_time=1, delete_message=True)
    assert(len(q) == 0)

    start_time = time.perf_counter()
    message = q.receive_message(wait_time=1, delete_message=True)
    time_delta = time.perf_counter() - start_time

    assert(time_delta < 1.5)
    assert(message is None)

    start_time = time.perf_counter()
    message = q.receive_message(wait_time=10, delete_message=True)
    time_delta = time.perf_counter() - start_time

    assert(time_delta < 12)
    assert(message is None)


def test_wait_for_message():
    q = instantiate_queue()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(q.wait_for_message)
        q.send_message(message='hello')
        message = future.result()
        assert(message)
        assert(message.body == 'hello')


def test_num_messages():

    q = instantiate_queue()
    assert(len(q) == 0)

    q.send_message(message='hello')
    assert(len(q) == 1)

    q.send_message(message='world')
    assert(len(q) == 2)


def test_purge():
    q = instantiate_queue()

    # case where queue is empty to begin with
    success = q.purge()
    assert(success)
    assert(len(q) == 0)

    # case where queue is not empty
    q.send_message(message='hello')
    assert(len(q) == 1)

    success = q.purge()
    assert(success)
    assert(len(q) == 0)

    q.send_message(message='hello')
    q.send_message(message='hello')
    assert(len(q) == 2)

    success = q.purge()
    assert(success)
    assert(len(q) == 0)

