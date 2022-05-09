import agent
from etherscan_mock import EtherscanMock
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from web3_mock import EOA_ADDRESS, Web3Mock

w3 = Web3Mock()
etherscan = EtherscanMock()


class TestUnverifiedContractAgent:
    def test_calc_contract_address(self):
        contract_address = agent.calc_contract_address(w3, EOA_ADDRESS, 9)
        assert contract_address == "0x728ad672409DA288cA5B9AA85D1A55b803bA97D7", "should be the same contract address"

    def test_detect_unverified_contract_with_unverified_contract(self):
        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'from': EOA_ADDRESS,
                'nonce': 9,
            },
            'block': {
                'number': 0
            },
            'traces': [{'type': 'create',
                        'action': {
                            'from': EOA_ADDRESS,
                            'value': 1,
                        }
                        }
                       ],
            'receipt': {
                'logs': []}
        })

        findings = agent.detect_unverified_contract_creation(w3, etherscan, tx_event)
        assert len(findings) == 1, "should have 1 finding"
        finding = next((x for x in findings if x.alert_id == 'UNVERIFIED-CODE-CONTRACT-CREATION'), None)
        assert finding.severity == FindingSeverity.Medium
        assert finding.type == FindingType.Suspicious
        assert finding.description == f'{EOA_ADDRESS} created contract 0x728ad672409DA288cA5B9AA85D1A55b803bA97D7'

#todo - negative cases