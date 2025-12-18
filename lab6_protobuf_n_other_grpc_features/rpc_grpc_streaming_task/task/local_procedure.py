'''
TASK: refactor this local procedure `count` into a gRPC procedure. This procedure belongs to a
gRPC service called `AssistantService`. Then, use a gRPC client to test the remote procedure.

Expected Behavior:
1. The server accepts the `from_val` and `step_sec` from a single unary request, and pushes the
  response message (i.e., the counter update mesasage) to a response stream.
2. The client calls the unary-stream remote procedure `Count` and receives a reponse stream (as
  a generator in Python). It keeps pulling message from the response stream and log it to the
  client's console until a keyboard interrupt (i.e., Ctrl+C) happens to cancel the response stream.
3. (Optional) Try to simulate all logging messages of the local procedure in the gRPC implementation.
  The gRPC server will log the request info before handling the request, and the event cancellation
  after the response stream is manually cancelled by the client. The client will log all counter
  update messages from the server as soon as they are retreived.

Hints:
1. Client can actively "cancel" an RPC call when she no longer wants to receives messages from
  the response stream. Check: https://grpc.io/docs/guides/cancellation/. Besides, this link shows
  a sample usage: https://github.com/grpc/grpc/blob/master/examples/python/cancellation/client.py#L68.
2. When the client cancels a response stream, the corresponding RPC call immediately finishes. To be
  able to log the event cancellation message from the server, a callback function can be configured
  to perform the final logging. The callback function will be assigned to this RPC call via the
  `context` parameter. This link shows a sample usage:
  https://chromium.googlesource.com/external/github.com/grpc/grpc/+/HEAD/examples/python/cancellation/README.md#responding-to-cancellations-from-a-servicer-thread.
'''
import time
import logging
from datetime import datetime

def count(from_val: int, step_sec: int) -> None:
  '''
  Progresses a counter from a starting value, adding 1 after every stepping seconds. 
  '''
  logging.info(f'Request: from={from_val}, step={step_sec}')
  cnt = from_val
  try:
    while True:
      # pause for step_sec seconds
      time.sleep(step_sec)
      # increment counter by 1
      cnt += 1
      # log the counter update
      msg = f'{datetime.now()}: count={cnt}'
      logging.info(msg)
  except KeyboardInterrupt:
    # ctrl+c to stop
    logging.info('Process cancelled by user (Ctrl+C).')
  finally:
    logging.info(f'Process cancelled for request: from={from_val}, step={step_sec}')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  """
  INFO:root:Request: from=6, step=2
  INFO:root:2024-10-22 03:13:33.013209: count=7
  INFO:root:2024-10-22 03:13:35.012208: count=8
  INFO:root:2024-10-22 03:13:37.012531: count=9
  INFO:root:2024-10-22 03:13:39.012810: count=10
  INFO:root:2024-10-22 03:13:41.013144: count=11
  ...
  INFO:root:Process cancelled by user (Ctrl+C).
  INFO:root:Process cancelled for request: from=6, step=2
  """
  count(from_val=6, step_sec=2)
