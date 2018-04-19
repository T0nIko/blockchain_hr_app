import web3

from solc import compile_files


def init_singletons():
    compiled_sol = compile_files(['review.sol'])

    contract_interface = compiled_sol['review.sol:Reviews']

    w3 = web3.Web3(web3.providers.eth_tester.EthereumTesterProvider())  # TODO: somehow configure private chain & geth
    w3.eth.enable_unaudited_features()

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    return w3, contract, contract_interface


W3, CONTRACT, CONTRACT_INTERFACE = init_singletons()


def post_review(reviewer, target, data, is_positive):
    deploy_txn = CONTRACT.constructor(
        reviewer.address,
        target.address,
        data,
        is_positive
    ).transact()
    txn_receipt = W3.eth.getTransactionReceipt(deploy_txn)
    contract_address = txn_receipt['contractAddress']

    return contract_address


def get_contract_instance(contract_address):
    return W3.eth.contract(
        abi=CONTRACT_INTERFACE['abi'],
        address=contract_address,
        ContractFactoryClass=web3.contract.ConciseContract
    )


def contract_instance_wrapper(contract_address):
    instance = get_contract_instance(contract_address)

    return [
        instance.get_review_sender(),
        instance.get_review_target(),
        instance.get_review_text(),
        instance.get_review_is_positive()
    ]
