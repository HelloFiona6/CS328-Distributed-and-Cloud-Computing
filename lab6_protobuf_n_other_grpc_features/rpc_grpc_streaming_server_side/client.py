import logging
import sys
import time

import grpc
from assistant_pb2_grpc import AssistantServiceStub
from assistant_pb2 import TellStoryRequest, TellStoryResponse


def run():
  with grpc.insecure_channel('127.0.0.1:50051') as channel:
    stub = AssistantServiceStub(channel)
    request = TellStoryRequest(user_name='Peter S', institution='SUSTech')
    logging.info(
      f'Requesting with user_name={request.user_name}, institution={request.institution}')
    response_stream = stub.TellStory(request)
    try:
      while True:
        response: TellStoryResponse = next(response_stream)
        stream_print(data=response.text_chunk)
      ### can also use the following implementation ###
      # for response in response_stream:
      #   stream_print(data=response.text_chunk)
    except grpc.RpcError as e:
      if e.code() == grpc.StatusCode.CANCELLED:
        logging.info('Stream cancelled by server. Exiting gracefully.')
      else:
        logging.error(f'An error occurred: {e}')
    finally:
      logging.info('Finished requesting.')


def stream_print(data: bytes, encoding='utf-8', buffer_size=5, step_sec=0.1):
  """ Flush bytes to stdout with a buffer size every stepping seconds """
  data_str = data.decode(encoding)
  for i in range(0, len(data_str), buffer_size):
    end = min(i + buffer_size, len(data_str))
    sys.stdout.write(data_str[i:end])
    sys.stdout.flush()
    time.sleep(step_sec)


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  run()
