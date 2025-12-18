# gRPC - Bidirectional Streaming

A Bidirectional Streaming example for gRPC. In this example, the gRPC server offers a number-guessing service. The client will call the `GuessInt` procedure from the server to enter a real-time number-guessing gameplay session. Within the session, the client can continuously send guesses to the server in a streaming fashion, while the server will also stream the guessing results back to the client.

## Requirements

- Check `pyproject.toml` or `requirements.txt` for Python requirements in the `server/` folder. Set up with `uv sync` **inside that folder**.

> If you are not working with `uv`, then just run `python -m pip install -r requirements.txt`.

## Write a `.proto` File

Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there is the story-telling procedure defined. The request and response message for the remote procedure are also defined at the bottom of the file.

**Specifically, the RPC procedure specifies to use both a `stream` request and a `stream` response in its definition.**

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

**In the `GuessInt` precedure implementation, Python uses `yield` to generate responses once acquiring a guessing request.**

`asyncio` is used to enable faster and non-blocking I/O operations. Additional code is written to ensure graceful shutdown of the asynchronous I/O gRPC server.

Besides, a callback function is assigned to the RPC context so that the server can always log an ending note to the console whenever the client/server actively finishes the RPC call.

## Implement and Run the gRPC Client

Check the `client.py` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:

```bash
uv run python client.py
```

**In the client, Python retrieves a response stream by calling the remote procedure `GuessInt`. Then, `async for` is used to retrieve arrived response mesasges upon their arrival.**

Similar to the server, `asyncio` is used to enable faster and non-blocking I/O operations. To separate the request streaming and response streaming logic, async functions are implemented for the two individually. However, note that since this is a number guessing service, requests and responses will logically block each other.

The client code provides two modes for number guessing. The manual guessing mode supports interactively inputing an integer from the console to play with the server, while the auto-guessing mode will provide guesses by itself in order to demonstrate the real-time communication speed in this bidirectional streaming scenario.

## Execution & Result Analysis

### Manual Guessing

#### Breaking the Outputs

Using `guess = await manual_guess()`, the client starts an interactive guessing attempt. As soon as this starts, the **server** generates the true number and logs the number to its own console:

```text
INFO:root:Server started on port 50051
INFO:root:Received number guessing request.
INFO:root:True value is 92.
```

The **client** immediately receives a greeting message from the server and enters the blocking `input()` function:

```text
Guessing start! Try an integer between 1 and 100.
Guess:
```

Entering a guess, the client sends a guessing request message from the same request to the server. The **server** will compare the value and log the comparison result to its console:

```text
INFO:root:User guessed 12 < 92 (true value).
```

The response messagee will be streamed back to the client and appear at the client's console, along with a new `input()` round started:

```text
Your guess 12 < true value.
Guess:
```

The same operation happens multiple times until the **client** manages to find the true value:

```text
Guess: 92
Your guess 92 = true value. Congratulations!!!
```

The client will receive the announcing message from the server and the RPC call will be automatically ended by the server. On the **server**, everything will be logged to the console:

```text
INFO:root:User guessed 92 = 92 (true value).
INFO:root:Guessing service finished.
```

**NOTE**: Manual guessing supports input checking to verify that the input value must be an integer.

#### Complete Client Output

```text
Guessing start! Try an integer between 1 and 100.
Guess: 20
Your guess 20 < true value.
Guess: 70
Your guess 70 > true value.
Guess: xxx
ERROR:root:Invalid input xxx. Please enter a valid number.
Guess: 55
Your guess 55 = true value. Congratulations!!!
```

#### Complete Server Output

```text
INFO:root:Server started on port 50051
INFO:root:Received number guessing request.
INFO:root:True value is 55.
INFO:root:User guessed 20 < 55 (true value).
INFO:root:User guessed 70 > 55 (true value).
INFO:root:User guessed 55 = 55 (true value).
INFO:root:Guessing service finished.
```

### Auto-Guessing

Using `guess = await auto_guess()`, the client starts an automatic guessing attempt. The client uses the bisection method to quickly approach the true integer. Once the client starts, it automatically detects the guess evaluation from the server and provides a new guess. The outputs from the **client** are as follows:

```text
Guessing start! Try an integer between 1 and 100.
INFO:root:Init guess: go for 50
Your guess 50 < true value.
INFO:root:Guessing: 75
Your guess 75 > true value.
INFO:root:Guessing: 62
Your guess 62 < true value.
INFO:root:Guessing: 68
Your guess 68 < true value.
INFO:root:Guessing: 71
Your guess 71 = true value. Congratulations!!!
```

The outputs from the **server** are as follows:

```text
INFO:root:Server started on port 50051
INFO:root:Received number guessing request.
INFO:root:True value is 71.
INFO:root:User guessed 50 < 71 (true value).
INFO:root:User guessed 75 > 71 (true value).
INFO:root:User guessed 62 < 71 (true value).
INFO:root:User guessed 68 < 71 (true value).
INFO:root:User guessed 71 = 71 (true value).
INFO:root:Guessing service finished.
```

## Keyboard Interrupt

When `Ctrl+C` is pressed in the server console during a number-guessing gameplay, the **server** will be gracefully shutdown within 3 seconds:

```text
INFO:root:Received number guessing request.
INFO:root:True value is 80.
INFO:root:User guessed 50 < 80 (true value).
INFO:root:User guessed 32 < 80 (true value).
# Ctrl+C
INFO:root:Server gracefully shutting down...
INFO:root:Server gracefully shut down.
INFO:root:Guessing service finished.
```

When `Ctrl+C` is pressed in the client console during a number-guessing gameplay, the **client** will also gracefully exit:

```text
Guessing start! Try an integer between 1 and 100.
Guess: 32
Your guess 32 < true value.
Guess: 44
Your guess 44 < true value.
Guess:
# Ctrl+C
INFO:root:Stopped by keyboard input.
```

In the meantime, the **server** can capture this event and log an ending note:

```text
INFO:root:Received number guessing request.
INFO:root:True value is 63.
INFO:root:User guessed 32 < 63 (true value).
INFO:root:User guessed 44 < 63 (true value).
# Ctrl+C from the client
INFO:root:Guessing service finished.
```
