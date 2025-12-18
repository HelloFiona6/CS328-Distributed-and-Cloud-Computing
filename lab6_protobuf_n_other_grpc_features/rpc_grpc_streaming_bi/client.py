import asyncio
import logging

import grpc
from assistant_pb2_grpc import AssistantServiceStub
from assistant_pb2 import GuessIntRequest, GuessIntResponse


async def send_messages(stub: AssistantServiceStub):
  # producer-consumer queue
  response_queue = asyncio.Queue()
  first_guess = True
  valid_range_min = 1
  valid_range_max = 100

  async def get_guesses():
    async def manual_guess() -> int:
      while True:
        try:
          x = input('Guess: ')
          return int(x)
        except ValueError:
          logging.error(f'Invalid input {x}. Please enter a valid number.')
        except Exception as e:
          logging.error(f'An error occurred while guessing: {e}')

    async def auto_guess() -> int:
      nonlocal first_guess, valid_range_min, valid_range_max
      if first_guess:
        # first guess
        first_guess = False
        res = (valid_range_min + valid_range_max) // 2
        logging.info(f'Init guess: go for {res}')
        return res
      response: GuessIntResponse = await response_queue.get()
      if response.symbol is None or response.symbol == '':
        # ignore random messages
        return -1
      if response.symbol == '<':
        # guess < true: set min to guess+1
        valid_range_min = response.guess + 1
      elif response.symbol == '>':
        # guess > true: set max to guess-1
        valid_range_max = response.guess - 1
      else:
        logging.info('Guess already correct, no need to guess further.')
        return -2
      res = (valid_range_min + valid_range_max) // 2
      logging.info(f'Guessing: {res}')
      return res

    # get_guesses()
    while True:
      await asyncio.sleep(0.2)
      # guess = await manual_guess()
      guess = await auto_guess()
      if guess == -2:
        break
      if guess == -1:
        continue
      yield GuessIntRequest(guess=guess)

  # send_messages()
  # establish a bidirectional streaming connection
  try:
    response_stream = stub.GuessInt(get_guesses())
    async for response in response_stream:
      # type hinting for painless development
      response: GuessIntResponse = response
      print(response.message)
      # put response in the queue
      await response_queue.put(response)
  except Exception as e:
    response_stream.cancel()
    logging.info(f'Stopped by: {e}')


async def run():
  # aio: gRPC's Asynchronous Python API - non-blocking I/O operations
  async with grpc.aio.insecure_channel('127.0.0.1:50051') as channel:
    stub = AssistantServiceStub(channel)
    await send_messages(stub)

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  try:
    asyncio.run(run())
  except KeyboardInterrupt:
    logging.info('Stopped by keyboard input.')
