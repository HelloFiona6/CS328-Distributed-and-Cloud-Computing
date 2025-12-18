import logging

import grpc
from assistant_pb2_grpc import AssistantServiceStub
from assistant_pb2 import CountRequest, CountResponse


def run():
  with grpc.insecure_channel('127.0.0.1:50051') as channel:
    stub = AssistantServiceStub(channel)
    request = CountRequest(from_val=6, step_sec=2)
    response_stream = stub.Count(request)
    try:
      while True:
        response: CountResponse = next(response_stream)
        logging.info(response.message)
    except KeyboardInterrupt:
      # ctrl+c to stop
      logging.info('Stream cancelled by user (Ctrl+C).')
    finally:
      response_stream.cancel()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  run()
