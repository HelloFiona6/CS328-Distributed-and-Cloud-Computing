setup-python:
	uv sync

gen-proto: setup-python
	uv run python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. assistant.proto

get-alice-story:
	wget -O alice.txt https://python.pages.doc.ic.ac.uk/2020/assets/files/modules-files/alice.txt
