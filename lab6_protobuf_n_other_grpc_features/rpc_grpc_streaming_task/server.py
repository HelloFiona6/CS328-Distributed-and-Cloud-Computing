import time
from datetime import datetime
from concurrent import futures
import logging

import grpc
from assistant_pb2 import CountRequest, CountResponse
from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server


class Assistant(AssistantServiceServicer):
  def Count(self, request: CountRequest, context: grpc.ServicerContext):
    logging.info(f'Request: from={request.from_val}, step={request.step_sec}')
    cnt = request.from_val

    def on_rpc_done():
      logging.info(
        f'Response stream cancelled for request: from={request.from_val}, step={request.step_sec}')

    context.add_callback(on_rpc_done)

    while True:
      # pause for step_sec seconds
      time.sleep(request.step_sec)
      # increment counter by 1
      cnt += 1
      # build response
      msg = f'{datetime.now()}: count={cnt}'
      response = CountResponse(message=msg)
      # yield the response as a part of the server-side streaming
      yield response


def serve():
  port = '50051'
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_AssistantServiceServicer_to_server(Assistant(), server)
  server.add_insecure_port(f'[::]:{port}')
  server.start()
  logging.info(f'Server started on port {port}')
  server.wait_for_termination()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  serve()
