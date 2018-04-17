import web3

from solc import compile_files


compiled_sol = compile_files(['review.sol'])

contract_interface = compiled_sol['review.sol:Reviews']

w3 = web3.Web3(web3.providers.eth_tester.EthereumTesterProvider())

contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

deploy_txn = contract.constructor(
    '0xCf5609B003B2776699eEA1233F7C82D5695cC9AA',
    '0xCf5609B003B2776699eEA1233F7C82D5695cC9AA',
    'test_data'
).transact()
txn_receipt = w3.eth.getTransactionReceipt(deploy_txn)
contract_address = txn_receipt['contractAddress']

contract_instance = w3.eth.contract(abi=contract_interface['abi'], address=contract_address, ContractFactoryClass=web3.contract.ConciseContract)


if __name__ == '__main__':
    print(contract_instance.get_review_text())