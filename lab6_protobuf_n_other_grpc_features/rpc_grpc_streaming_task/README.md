# gRPC - Remote Counter

A Server-side Streaming task for gRPC. In this example, the gRPC server offers a counting service. Starting from a given number, the server adds 1 to the number for every step seconds, where the step value is also given by the client. The gRPC client calls this remote procedure to "subscribe" to the counting service and retrieves the counting report strings in a streaming fashion.

## Requirements

- Check `pyproject.toml` or `requirements.txt` for Python requirements in the `server/` folder. Set up with `uv sync` **inside that folder**.

> If you are not working with `uv`, then just run `python -m pip install -r requirements.txt`.

## Write a `.proto` File

Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there is the counting procedure defined. The request and response message for the remote procedure are also defined at the bottom of the file.

More info on Proto Best Practices is provided here: https://protobuf.dev/programming-guides/dos-donts/.

## Generate Message Classes and Client Stub

Run:

```bash
uv run python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. assistant.proto
```

- `protoc` is already installed in `grpc_tools`.
- `-I` specifies `./` as the path to import the proto files.
- The following 3 flags look similar but have actually different purposes:
  - `--python_out` specifies where to generate the Python **message** classes. It will create `*_pb2.py` files for specifically the **messages** defined in the proto files. Required even when gRPC is not used.
  - `--pyi_out` specifies where to generate Python **type hinting** `.pyi` files. It will create `*_pb2.pyi` files for Python IDEs to perform type suggestions and error checking. It is optional but provides better coding experience.
  - `--grpc_python_out` specifies where to generate **gRPC service** templates and client stubs for the defined services in the proto files. It will create `*_pb2_grpc.py` files that handle the gRPC communication logic between client and server. It is optional for users using Protobuf without gRPC.

As a result, 3 files will be generated:

1. `assistant_pb2.py` for the Python message classes.
2. `assistant_pb2.pyi` for the Python IDEs to support type hinting.
3. `assistant_pb2_grpc.py` for the gRPC service stubs.

For more information/options on `protoc`, check the Hello World part.

## Implement and Run the gRPC Server

Check the `server.py` file where an `Assistant` implements the registered procedures from `AssistantServiceServicer`. In the serving function, the gRPC server uses a thread pool executor to enable concurrent request handling. The server is served at port=`50051` via:

```bash
uv run python server.py
```

In the `Count` precedure implementation, Python uses `yield` to generate responses once in a while. A callback function is added to the context so that when the client actively cancels the response stream, we can gracefully verify that the procedure finishes normally.

## Implement and Run the gRPC Client

Check the `client.py` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:

```bash
uv run python client.py
```

In the client, Python retrieves a response stream by calling the remote procedure `Count`. Then, `next()` is used to retrieve arrived response mesasges once in a while. When we press `Ctrl+C` via keyboard, the client will gracefully exit by cancelling the response stream from the server.

## Execution & Result Analysis

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
