import time
from web3 import Web3
from web3.exceptions import TransactionNotFound

RPC_URL = "https://rpc.ankr.com/taiko"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def analyze_block(block_number):
    start_time = time.time() 

    block = w3.eth.get_block(block_number, full_transactions=True)
    
    # Base Fee (for blocks after EIP-1559)
    base_fee = block.baseFeePerGas if hasattr(block, 'baseFeePerGas') else 0
    total_revenue = 0
    
    for tx in block.transactions:
        try:
            receipt = w3.eth.get_transaction_receipt(tx.hash)
            
            # Gas price (EIP-1559 after and before)
            if hasattr(tx, 'maxFeePerGas'):
                # After EIP-1559 
                effective_gas_price = receipt.effectiveGasPrice
            else:
                # Before EIP-1559
                effective_gas_price = tx.gasPrice
            
            revenue = receipt.gasUsed * (effective_gas_price - base_fee)
            total_revenue += revenue
        
        except TransactionNotFound:
            continue

    total_revenue_ether = w3.from_wei(total_revenue, 'ether')
    
    print(f"Block Number: {block_number}")
    print(f"Total Transactions: {len(block.transactions)}")
    print(f"Total revenue (gasPrice - baseFee) * gasUsed: {total_revenue_ether:.18f} ETH")

    end_time = time.time()  
    execution_time = end_time - start_time  
    print(f"\nExecution time: {execution_time:.2f} seconds")  

if __name__ == "__main__":
    BLOCK_NUMBER = 487373 
    analyze_block(BLOCK_NUMBER)
