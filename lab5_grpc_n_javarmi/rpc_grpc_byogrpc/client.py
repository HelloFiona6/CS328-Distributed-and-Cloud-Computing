import grpc

from assistant_pb2 import ReportStatsRequest
from assistant_pb2_grpc import AssistantServiceStub


def run():
  with grpc.insecure_channel('127.0.0.1:8082') as channel:
    stub = AssistantServiceStub(channel)
    request = ReportStatsRequest(
      user_name='Peter S', institution='SUSTech',
      values=[1, 1.5, 2, 2.5, 5, -1, -1.5, -2, -2.5, -3],
    )
    print('> Request:')
    print(request)
    res = stub.ReportStats(request)
    print('> Response:')
    print(res)


if __name__ == '__main__':
  """
  > Request:
  user_name: "Peter S"
  institution: "SUSTech"
  values: 1
  values: 1.5
  values: 2
  values: 2.5
  values: 5
  values: -1
  values: -1.5
  values: -2
  values: -2.5
  values: -3

  > Response:
  min_value: -3
  max_value: 5
  avg_value: 0.2
  message: "Hi Peter S from SUSTech! For [1.0, 1.5, 2.0, 2.5, 5.0, -1.0, -1.5, -2.0, -2.5, -3.0]: min=-3.0; max=5.0, avg=0.2"
  """
  run()
