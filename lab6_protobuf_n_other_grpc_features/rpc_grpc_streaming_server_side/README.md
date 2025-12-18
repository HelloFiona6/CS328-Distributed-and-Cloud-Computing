# gRPC - Server-side Streaming

A Server-side Streaming example for gRPC. In this example, the gRPC server offers a story-telling service. The client will call the `TellStory` procedure from the server and streams the text from the response stream to the console, simulating the typing behavior.

## Requirements

- Check `pyproject.toml` or `requirements.txt` for Python requirements in the `server/` folder. Set up with `uv sync` **inside that folder**.

> If you are not working with `uv`, then just run `python -m pip install -r requirements.txt`.

## Write a `.proto` File

Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there is the story-telling procedure defined. The request and response message for the remote procedure are also defined at the bottom of the file.

**Specifically, the RPC procedure specifies to use a `stream` response in its definition.**

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

**In the `TellStory` precedure implementation, Python uses `yield` to generate responses once in a while. The complete story is divided into byte chunks as multiple responses.**

The server will output the following text to the console upon an RPC call:

```text
INFO:root:Server started on port 50051
INFO:root:Received story-telling request from Peter S, SUSTech.
INFO:root:Start streaming alice.txt
INFO:root:Read 1024 bytes: [Alice's A ...
INFO:root:Read 1024 bytes: y TOOK A W ...
INFO:root:Read 1024 bytes: of the wel ...
...
INFO:root:Read 1024 bytes: mmer days. ...
INFO:root:[EOF]
INFO:root:Finishes streaming alice.txt for Peter S from SUSTech.
```

## Implement and Run the gRPC Client

Check the `client.py` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:

```bash
uv run python client.py
```

**In the client, Python retrieves a response stream by calling the remote procedure `TellStory`. Then, `next()` is used to retrieve arrived response mesasges once in a while. The retrieved text is streamed to `sys.stdout` to simulate the typing behavior.**

The client will output the following text partially in a streaming fashion:

```text
INFO:root:Requesting with user_name=Peter S, institution=SUSTech
Hi Peter S from SUSTech! Here's your story:

[Alice's Adventures in Wonderland by Lewis Carroll 1865]

CHAPTER I. Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'
...
Lastly, she pictured to herself how this same little sister of hers
would, in the after-time, be herself a grown woman; and how she would
keep, through all her riper years, the simple and loving heart of her
childhood: and how she would gather about her other little children, and
make THEIR eyes bright and eager with many a strange tale, perhaps even
with the dream of Wonderland of long ago: and how she would feel with
all their simple sorrows, and find a pleasure in all their simple joys,
remembering her own child-life, and the happy summer days.

That's it! Hope you like the story~
INFO:root:Stream cancelled by server. Exiting gracefully.
INFO:root:Finished requesting.
```

**NOTE**: You can tweak `buffer_size=1024` and `step_sec=0.01` in the `stream_print` function from the client to speed up text rendering in order to check the completion behavior of the client, including how it handles response stream cancellation from the server.

For more information about cancellation, check: https://grpc.io/docs/guides/cancellation/.

Also, you can tweak the server to sleep for 3 seconds after each story text chunk response in order to slow down the response sending. Then, tweak `buffer_size=1024` in the `stream_print` function from the client in order to speed up text rendering. In this case, the client will wait for the response message from the server in a blocking style.
