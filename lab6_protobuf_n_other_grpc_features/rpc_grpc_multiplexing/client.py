import logging
import time
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import grpc
from assistant_pb2_grpc import AssistantServiceStub
from assistant_pb2 import ChatMessage

MSG_DEFAULT = 'Hello World!'


def call_chill_a(stub: AssistantServiceStub, id: int):
  logging.info(f'{datetime.now()}: Calling ChillA {id}')
  start_t = time.time()
  _ = stub.ChillA(ChatMessage(id=id, message=MSG_DEFAULT))
  logging.info(
    f'{datetime.now()}: ChillA {id} finished after {time.time() - start_t:.2f} seconds')


def call_chill_b(stub: AssistantServiceStub, id: int):
  logging.info(f'{datetime.now()}: Calling ChillB {id}')
  start_t = time.time()
  _ = stub.ChillB(ChatMessage(id=id, message=MSG_DEFAULT))
  logging.info(
    f'{datetime.now()}: ChillB {id} finished after {time.time() - start_t:.2f} seconds')


def run(num_a_tasks: int, num_b_tasks: int):
  with grpc.insecure_channel('127.0.0.1:50051') as channel:
    stub = AssistantServiceStub(channel)
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
      # execute concurrently
      futures_a = []
      for ai in range(num_a_tasks):
        futures_a.append(executor.submit(call_chill_a, stub, ai))
      futures_b = []
      for bi in range(num_b_tasks):
        futures_b.append(executor.submit(call_chill_b, stub, bi))
      # wait for all to finish
      for futures_x in [futures_a, futures_b]:
        for future_i in futures_x:
          future_i.result()

  logging.info(
    f'Total execution time = {time.time() - start_time:.2f} seconds.')


if __name__ == '__main__':
  # python client.py -a 1 -b 1
  parser = argparse.ArgumentParser(description='gRPC Multiplexing Example')
  parser.add_argument('-a', '--num-a-tasks', type=int,
                      default=1, help='number of tasks for ChillA')
  parser.add_argument('-b', '--num-b-tasks', type=int,
                      default=1, help='number of tasks for ChillB')
  FLAGS, _ = parser.parse_known_args()
  logging.basicConfig(level=logging.INFO)
  run(num_a_tasks=FLAGS.num_a_tasks, num_b_tasks=FLAGS.num_b_tasks)
