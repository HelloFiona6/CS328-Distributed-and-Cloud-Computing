from concurrent import futures
import logging
import time
from datetime import datetime

import grpc
from assistant_pb2 import ChatMessage
from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server


class Assistant(AssistantServiceServicer):
  def ChillA(self, request: ChatMessage, context: grpc.RpcContext):
    logging.info(
      f'{datetime.now()}: {self.ChillA.__name__} {request.id} start')
    time.sleep(5)  # sleep for 5 sec
    logging.info(f'{datetime.now()}: {self.ChillA.__name__} {request.id} end')
    return ChatMessage(id=request.id, message=request.message)

  def ChillB(self, request: ChatMessage, context: grpc.RpcContext):
    logging.info(
      f'{datetime.now()}: {self.ChillB.__name__} {request.id} start')
    time.sleep(3)  # sleep for 3 sec
    logging.info(f'{datetime.now()}: {self.ChillB.__name__} {request.id} end')
    return ChatMessage(id=request.id, message=request.message)


def serve():
  port = '50051'
  max_workers = 3
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
  add_AssistantServiceServicer_to_server(Assistant(), server)
  server.add_insecure_port(f'[::]:{port}')
  server.start()
  logging.info(f'Server started on port {port}')
  server.wait_for_termination()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  serve()
