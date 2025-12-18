check-kubectl:
	kubectl version --client

check-kind:
	kind version

create-cluster:
	kind create cluster --name dncc --config kind-config.yaml

list-clusters:
	kind get clusters

load-nginx:
	docker pull nginx:1.27
	kind load docker-image --name dncc nginx:1.27

check-contexts:
	kubectl config get-contexts

switch-context:
	kubectl config use-context kind-dncc

delete-cluster:
	kind delete cluster --name dncc
