# Kubernetes Test Network 

This project re-establishes the Hyperledger [test-network](../test-network) as a _cloud native_ application.

### Objectives:

- Provide a simple, _one click_ activity for running the Fabric test network.
- Provide a reference guide for deploying _production-style_ networks on Kubernetes.
- Provide a _cloud ready_ platform for developing chaincode, Gateway, and blockchain apps.
- Provide a Kube supplement to the Fabric [CA Operations and Deployment](https://hyperledger-fabric-ca.readthedocs.io/en/latest/deployguide/ca-deploy.html) guides.
- Support a transition to [Chaincode as a Service](https://hyperledger-fabric.readthedocs.io/en/latest/cc_service.html).
- Support a transition from the Internal, Docker daemon to [External Chaincode](https://hyperledger-fabric.readthedocs.io/en/latest/cc_launcher.html) builders.
- Run on any Kube.

_Fabric, Ahoy!_ 


## Prerequisites 

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://www.docker.com)
- K8s: [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) or [Rancher / k3s](https://rancherdesktop.io)
- [jq](https://stedolan.github.io/jq/)
- [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html) (`brew install gettext` on OSX)


## Quickstart

Create a KIND Kubernetes:
```shell
./network kind
```
For environments running [Rancher k3s](docs/KUBERNETES.md#rancher-desktop-and-k3s): 
```shell
export TEST_NETWORK_CLUSTER_RUNTIME=k3s

./network cluster-init 
```

Launch the network, create a channel, and deploy the [basic-asset-transfer](../asset-transfer-basic) smart contract: 
```shell
./network up
./network channel create

./network chaincode deploy asset-transfer-basic basic_1.0 $PWD/../asset-transfer-basic/chaincode-java
```

Invoke and query chaincode:
```shell
./network chaincode invoke asset-transfer-basic '{"Args":["CreateAsset","1","blue","35","tom","1000"]}' 
./network chaincode query  asset-transfer-basic '{"Args":["ReadAsset","1"]}'
```

Access the blockchain with a [REST API](https://github.com/hyperledger/fabric-samples/tree/main/asset-transfer-basic/rest-api-typescript): 
```shell
./network rest-easy
```

Tear down the test network: 
```shell
./network down 
```

Tear down the cluster: 
```shell
./network unkind
```


## [Detailed Guides](docs/README.md)

- [Working with Kubernetes](docs/KUBERNETES.md)
- [Certificate Authorities](docs/CA.md)
- [Launching the Test Network](docs/TEST_NETWORK.md)
- [Working with Channels](docs/CHANNELS.md)
- [Working with Chaincode](docs/CHAINCODE.md)
- [Working with Applications](docs/APPLICATIONS.md)


### DNS Resolution on OSX

Fabric's OSX binaries have been statically linked with the golang `go` DNS resolver.  In some environments, this 
causes a brief but [noticeable delay](https://github.com/hyperledger/fabric/issues/3372) when issuing peer commands 
against the test network.

Workarounds to improve DNS resolution time on OSX: 

- Add manual DNS overrides for virtual hosts by adding to /etc/hosts:
```
127.0.0.1 org0-ca.vcap.me
127.0.0.1 org1-ca.vcap.me
127.0.0.1 org2-ca.vcap.me
127.0.0.1 org0-orderer1.vcap.me
127.0.0.1 org0-orderer2.vcap.me
127.0.0.1 org0-orderer3.vcap.me
127.0.0.1 org1-peer1.vcap.me
127.0.0.1 org1-peer2.vcap.me
127.0.0.1 org2-peer1.vcap.me
127.0.0.1 org2-peer2.vcap.me
```

- Reduce the system resolver timeout from the default 5s by adding to /etc/resolv.conf:
```shell
options: timeout 2
```

- Compile the [fabric binaries](https://github.com/hyperledger/fabric) on a Mac and copy `build/bin/*` outputs to 
  `test-network-k8s/bin`.  Mac native builds are linked against the `netdns=cgo` DNS resolver, and are not
  subject to the timeouts associated with the Golang DNS resolver.