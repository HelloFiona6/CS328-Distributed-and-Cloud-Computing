setup:
	uv sync

gen-proto: setup
	uv run python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. assistant.proto
