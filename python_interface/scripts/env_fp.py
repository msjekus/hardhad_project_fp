from dotenv import load_dotenv
import os
load_dotenv()
from web3 import Web3

rpc_url = os.getenv("RPC_URL")
adr_a = Web3.to_checksum_address(os.getenv("ACCOUNT_ADDRESS"))
adr_c=Web3.to_checksum_address(os.getenv("COURSE_ADDRESS"))
private_key=os.getenv("PRIVATE_KEY")
adr_r=Web3.to_checksum_address(os.getenv("REFUND_ADDRESS"))

