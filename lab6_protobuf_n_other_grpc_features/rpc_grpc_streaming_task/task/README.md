# gRPC - Remote Counter

This is a task from the gRPC - Server-side Streaming example.

The students will be given the `local_procedure.py` file. The goal is to refactor the local procedure into a remote procedure hosted by the `AssistantService` gRPC service. For more info, check the `local_procedure.py` file directly.

## Task

Refactor this local procedure `count` into a gRPC procedure. This procedure belongs to a
gRPC service called `AssistantService`. Then, use a gRPC client to test the remote procedure.

## Expected Behavior

1. The server accepts the `from_val` and `step_sec` from a single unary request, and pushes the
   response message (i.e., the counter update mesasage) to a response stream.
2. The client calls the unary-stream remote procedure `Count` and receives a reponse stream (as
   a generator in Python). It keeps pulling message from the response stream and log it to the
   client's console until a keyboard interrupt (i.e., Ctrl+C) happens to cancel the response stream.
3. (Optional) Try to simulate all logging messages of the local procedure in the gRPC implementation.
   The gRPC server will log the request info before handling the request, and the event cancellation
   after the response stream is manually cancelled by the client. The client will log all counter
   update messages from the server as soon as they are retreived.

### Breaking the Outputs

Starting the **server** outputs the following message:

```text
INFO:root:Server started on port 50051
```

Starting the **client** outputs from time to time the following messages:

```text
INFO:root:2024-10-22 01:24:03.377470: count=7
INFO:root:2024-10-22 01:24:05.377893: count=8
INFO:root:2024-10-22 01:24:07.378323: count=9
INFO:root:2024-10-22 01:24:09.378861: count=10
INFO:root:2024-10-22 01:24:11.379389: count=11
...
```

As soon as the client starts, the **server** outputs one more message:

```text
INFO:root:Request: from=6, step=2
```

When `Ctrl+C` is pressed from the **client** console, it outputs:

```text
INFO:root:Stream cancelled by user (Ctrl+C).
```

At the same time, the **server** outputs:

```text
INFO:root:Response stream cancelled for request: from=6, step=2
```

### Server Output

```text
INFO:root:Server started on port 50051
INFO:root:Request: from=6, step=2
INFO:root:Response stream cancelled for request: from=6, step=2
```

### Client Output

```text
INFO:root:2024-10-22 01:46:35.411120: count=7
INFO:root:2024-10-22 01:46:37.411666: count=8
INFO:root:2024-10-22 01:46:39.412099: count=9
INFO:root:2024-10-22 01:46:41.412596: count=10
INFO:root:2024-10-22 01:46:43.413001: count=11
...
INFO:root:Stream cancelled by user (Ctrl+C).
```

## Hints

1. Client can actively "cancel" an RPC call when she no longer wants to receives messages from
   the response stream. Check: https://grpc.io/docs/guides/cancellation/. Besides, [this link](https://github.com/grpc/grpc/blob/74538378b495e4777006b0c424550c6468a72238/examples/python/cancellation/client.py#L68) shows
   a sample usage.
2. When the client cancels a response stream, the corresponding RPC call immediately finishes.
   To be able to log the event cancellation message from the server, a callback function can be configured to perform the final logging. The callback function will be assigned to this RPC call via the `context` parameter. [This link](https://chromium.googlesource.com/external/github.com/grpc/grpc/+/HEAD/examples/python/cancellation/README.md#responding-to-cancellations-from-a-servicer-thread) shows a sample usage.
