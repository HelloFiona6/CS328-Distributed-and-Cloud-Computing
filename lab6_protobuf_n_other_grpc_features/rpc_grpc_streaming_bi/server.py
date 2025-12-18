import logging
import asyncio
import random

import grpc
from assistant_pb2 import GuessIntRequest, GuessIntResponse
from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server


class Assistant(AssistantServiceServicer):
  def __init__(self) -> None:
    super().__init__()

  async def GuessInt(self, request_iterator, context):
    def on_rpc_done(ctx):
      logging.info('Guessing service finished.')

    # register callback function
    context.add_done_callback(on_rpc_done)

    # send back a greeting message
    logging.info('Received number guessing request.')
    true_int = random.randint(1, 100)
    logging.info(f'True value is {true_int}.')
    yield GuessIntResponse(message='Guessing start! Try an integer between 1 and 100.')
    # respond to guesses
    async for request in request_iterator:
      # type hinting for painless development
      request: GuessIntRequest = request
      # check result
      symbol = '=' if request.guess == true_int else (
        '<' if request.guess < true_int else '>')
      logging.info(
        f'User guessed {request.guess} {symbol} {true_int} (true value).')
      yield GuessIntResponse(message='Your guess %d %s true value.%s' % (
        request.guess, symbol, ' Congratulations!!!' if symbol == '=' else ''
      ), guess=request.guess, symbol=symbol)
      # if correct, guessing finished
      if symbol == '=':
        return


# graceful shutdown for grpc aio server
_cleanup_coroutines = []


async def serve():
  port = '50051'
  # aio: gRPC's Asynchronous Python API - non-blocking I/O operations
  server = grpc.aio.server()  # no need for ThreadPoolExecutor in asyncio
  add_AssistantServiceServicer_to_server(Assistant(), server)
  server.add_insecure_port(f'[::]:{port}')
  # wait for the server start
  await server.start()
  logging.info(f'Server started on port {port}')

  # https://github.com/grpc/grpc/pull/26622/files#diff-a71e80ec63a3fbeff2bdf255101f67e3b77d794424851f153ca4afa271c8ee6bR46-R51
  async def graceful_shutdown():
    logging.info('Server gracefully shutting down...')
    await server.stop(3)
    logging.info('Server gracefully shut down.')

  _cleanup_coroutines.append(graceful_shutdown())

  # wait for termination asynchronously
  await server.wait_for_termination()

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(serve())
  except KeyboardInterrupt:
    loop.run_until_complete(*_cleanup_coroutines)
  finally:
    loop.close()
