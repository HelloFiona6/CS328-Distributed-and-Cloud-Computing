# gRPC - Multiplexing

A Multiplexing example for gRPC. In this example, the gRPC server offers multiple `ChillX` procedures that will sleep for different number of seconds. This simulates heavy-load tasks so that the multiplexing behavior can be examined.

## Requirements

- Check `pyproject.toml` or `requirements.txt` for Python requirements in the `server/` folder. Set up with `uv sync` **inside that folder**.

> If you are not working with `uv`, then just run `python -m pip install -r requirements.txt`.

## Write a `.proto` File

Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there is the story-telling procedure defined. The request and response message for the remote procedure are also defined at the bottom of the file.

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

**`ChillA` will sleep for 5 seconds and `ChillB` will sleep for 3 seconds.**

## Implement and Run the gRPC Client

Check the `client.py` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:

```bash
uv python client.py -a 1 -b 1
```

where `uv run python client.py --help` gives:

```text
usage: client.py [-h] [-a NUM_A_TASKS] [-b NUM_B_TASKS]

gRPC Multiplexing Example

options:
  -h, --help            show this help message and exit
  -a NUM_A_TASKS, --num-a-tasks NUM_A_TASKS
                        number of tasks for ChillA
  -b NUM_B_TASKS, --num-b-tasks NUM_B_TASKS
                        number of tasks for ChillB
```

## Execution & Result Analysis

By defualt, the server has a thread pool with `max_workers=3`. As a result, it can handle at most 3 RPC calls concurrently. Additional RPC calls will be queued for later when former RPC calls finish. Both scenarios will be tested.

### Enough Workers on Server

Running the client as:

```bash
uv run python client.py -a 1 -b 1
```

The client starts two concurrent tasks as 1 RPC call to `ChillA` and 1 RPC call to `ChillB`. The outputs of the **client** are shown below:

```text
INFO:root:2024-10-22 23:53:18.950616: Calling ChillA 0
INFO:root:2024-10-22 23:53:18.950987: Calling ChillB 0
INFO:root:2024-10-22 23:53:21.953852: ChillB 0 finished after 3.00 seconds
INFO:root:2024-10-22 23:53:23.953957: ChillA 0 finished after 5.00 seconds
INFO:root:Total execution time = 5.01 seconds.
```

It can be inferred that the two tasks are handled in parallel and the client program takes 5 seconds in total to finish. The calling timestamp for both RPC calls is around `23:53:18.95`. Everything is completed within one single HTTP/2 connection, thanks to multiplexing. Now check the **server** outputs as well:

```text
INFO:root:Server started on port 50051
INFO:root:2024-10-22 23:53:18.952881: ChillB 0 start
INFO:root:2024-10-22 23:53:18.952996: ChillA 0 start
INFO:root:2024-10-22 23:53:21.953162: ChillB 0 end
INFO:root:2024-10-22 23:53:23.953255: ChillA 0 end
```

It can be noticed that both remote procedures start around `23:53:18.95` as well, which means both RPC request messages are immediately sent to the server, thanks to multiplexing.

### More Calls Than Workers on Server

Running the client as:

```bash
uv run python client.py -a 2 -b 2
```

The client starts 4 concurrent tasks as 2 RPC calls to `ChillA` and 2 RPC calls to `ChillB`. The outputs of the **client** are shown below:

```text
INFO:root:2024-10-23 00:01:32.162843: Calling ChillA 0
INFO:root:2024-10-23 00:01:32.163383: Calling ChillA 1
INFO:root:2024-10-23 00:01:32.163625: Calling ChillB 0
INFO:root:2024-10-23 00:01:32.164461: Calling ChillB 1
INFO:root:2024-10-23 00:01:35.168143: ChillB 0 finished after 3.00 seconds
INFO:root:2024-10-23 00:01:37.167988: ChillA 0 finished after 5.00 seconds
INFO:root:2024-10-23 00:01:37.168243: ChillA 1 finished after 5.00 seconds
INFO:root:2024-10-23 00:01:38.167510: ChillB 1 finished after 6.00 seconds
INFO:root:Total execution time = 6.01 seconds.
```

Since the server can only have 3 workers at most, 1 of the 4 request messages will be queued by the server and executed later. That one is request `1` to `ChillB`, which uses 6 seconds to get the response message. As soon as request `0` to `ChillB` finishes, it spares the resource for this request to execute, which is why it takes 6 seconds (3 seconds for `B0` and then 3 seconds for `B1`). Now check the **server** outputs as well:

```text
INFO:root:Server started on port 50051
INFO:root:2024-10-23 00:01:32.166841: ChillA 0 start
INFO:root:2024-10-23 00:01:32.167158: ChillA 1 start
INFO:root:2024-10-23 00:01:32.167244: ChillB 0 start
INFO:root:2024-10-23 00:01:35.167469: ChillB 0 end
INFO:root:2024-10-23 00:01:35.168069: ChillB 1 start
INFO:root:2024-10-23 00:01:37.167249: ChillA 0 end
INFO:root:2024-10-23 00:01:37.167640: ChillA 1 end
INFO:root:2024-10-23 00:01:38.166953: ChillB 1 end
```

Note that as expected, request `B1` immediately starts after request `B0` ends. Also keep in mind that all 4 request messages are immediately sent to the server, thanks to multiplexing. `B1`, although not immediately executing, stays in a queue from the server.

> If either `A0` or `A1` is queued at the beginning, then the total execution time becomes 8 seconds.
