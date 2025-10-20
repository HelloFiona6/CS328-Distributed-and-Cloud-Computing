from concurrent import futures
import logging

import grpc

from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server
from assistant_pb2 import ReportStatsRequest, ReportStatsResponse


class Assistant(AssistantServiceServicer):
  def ReportStats(self, request: ReportStatsRequest, context):
    '''
    report_add calculates the min, max, avg of the provided numeric values, and gives a response
    in natural language.
    '''
    val_min = min(request.values)
    val_max = max(request.values)
    val_avg = sum(request.values) / len(request.values)
    resp_msg = f'Hi {request.user_name} from {request.institution}! For {request.values}: min={val_min}; max={val_max}, avg={val_avg}'
    return ReportStatsResponse(min_value=val_min, max_value=val_max, avg_value=val_avg, message=resp_msg)


def serve():
  port = '8082'
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_AssistantServiceServicer_to_server(Assistant(), server)
  server.add_insecure_port(f'[::]:{port}')
  server.start()
  logging.info(f'Server started, listening on {port}')
  server.wait_for_termination()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  serve()
