import json
import os

root = "./"

def get_private_key() -> str:
    for dirpath, _, filename in os.walk(root + 'organizations/peerOrganizations/org1.example.com/msp/keystore/'):
        return open(dirpath + filename[0]).read()

def get_public_key() -> str:
    for dirpath, _, filename in os.walk(root + 'organizations/peerOrganizations/org1.example.com/msp/signcerts/'):
        return open(dirpath + filename[0]).read()

def get_ccp():
    return open(root + "organizations/peerOrganizations/org1.example.com/connection-org1.json").read()

print(
json.dumps({
    "credentials": {
        "certificate": get_public_key(),
        "privateKey": get_private_key()
    },
    "mspId": "Org1MSP",
    "type": "X.509",
    "version": 1
})
)

print(get_ccp())
