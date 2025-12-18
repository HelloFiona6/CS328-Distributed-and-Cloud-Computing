from concurrent import futures
import logging
import time

import grpc
from assistant_pb2 import TellStoryRequest, TellStoryResponse
from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server


class Assistant(AssistantServiceServicer):
  def __init__(self) -> None:
    super().__init__()
    self.encoding = 'utf-8'      # encoding format of the story text into bytes
    # where to read the story (to simulate story generation)
    self.story_fn = 'alice.txt'
    self.buffer_size = 1024      # buffer size in bytes when reading the story file
    self.peek_size = 10          # buffer size in bytes for logging purpose

  def TellStory(self, request: TellStoryRequest, context: grpc.RpcContext):
    # Send back a greeting message
    logging.info(
      f'Received story-telling request from {request.user_name}, {request.institution}.')
    greeting = f'Hi {request.user_name} from {request.institution}! Here\'s your story:\n\n'
    yield TellStoryResponse(text_chunk=greeting.encode(self.encoding))
    # simulating story generation time
    time.sleep(3)
    # read the file with a buffer size and send the buffer data back
    logging.info(f'Start streaming {self.story_fn}')
    with open(self.story_fn, 'rb') as f:
      while True:
        # read a text chunk as a data buffer
        chunk = f.read(self.buffer_size)
        if not chunk:  # EOF
          logging.info('[EOF]')
          break
        logging.info('Read %d bytes: %s ...' % (self.buffer_size,
                     chunk[:self.peek_size].decode(self.encoding)))
        yield TellStoryResponse(text_chunk=chunk)
        time.sleep(0.05)
    # ending note
    ending = '\nThat\'s it! Hope you like the story~\n'
    yield TellStoryResponse(text_chunk=ending.encode(self.encoding))
    logging.info(
      f'Finishes streaming {self.story_fn} for {request.user_name} from {request.institution}.')
    # finsh the RPC call via cancellation
    context.cancel()


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
