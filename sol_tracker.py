import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import asyncio
import aiohttp
import ssl
import certifi
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import json

# Create SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

class RateLimiter:
    def __init__(self, calls_per_second=10):
        self.calls_per_second = calls_per_second
        self.calls = []
        
    async def acquire(self):
        now = time.time()
        self.calls = [call for call in self.calls if now - call < 1.0]
        
        if len(self.calls) >= self.calls_per_second:
            await asyncio.sleep(1.0 - (now - self.calls[0]))
            
        self.calls.append(now)

async def get_wallet_tokens_async(session: aiohttp.ClientSession, wallet_address: str, rate_limiter: RateLimiter) -> List[Dict]:
    """
    Async function to fetch token balances for a given Solana wallet
    """
    try:
        await rate_limiter.acquire()
        
        url = "https://api.mainnet-beta.solana.com"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                wallet_address,
                {
                    "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
                },
                {
                    "encoding": "jsonParsed"
                }
            ]
        }
        
        async with session.post(url, json=payload, ssl=ssl_context) as response:
            data = await response.json()
            
            if "result" not in data:
                return []
                
            tokens = []
            token_tasks = []
            
            for item in data["result"]["value"]:
                info = item["account"]["data"]["parsed"]["info"]
                amount = float(info["tokenAmount"]["uiAmount"])
                if amount > 0:
                    token_address = info["mint"]
                    token_tasks.append(get_token_info_async(session, token_address, amount, rate_limiter))
            
            token_results = await asyncio.gather(*token_tasks, return_exceptions=True)
            
            for result in token_results:
                if isinstance(result, dict):
                    tokens.append({
                        "wallet": wallet_address[:8] + "...",
                        **result
                    })
            
            return tokens
            
    except Exception as e:
        st.error(f"Error fetching data for wallet {wallet_address[:8]}...: {str(e)}")
        return []

async def get_token_info_async(session: aiohttp.ClientSession, token_address: str, amount: float, rate_limiter: RateLimiter) -> Dict:
    """
    Async function to get token information including price
    """
    try:
        await rate_limiter.acquire()
        
        cache_key = f"token_info_{token_address}"
        if cache_key not in st.session_state:
            # For testing, return mock data since the API endpoint is placeholder
            token_info = {
                "symbol": f"TOKEN_{token_address[:4]}",
                "price": 1.0  # Mock price
            }
            st.session_state[cache_key] = token_info
        else:
            token_info = st.session_state[cache_key]
        
        return {
            "token": token_info.get("symbol", token_address[:8] + "..."),
            "amount": amount,
            "usd_value": amount * token_info.get("price", 0)
        }
    except Exception:
        return {
            "token": token_address[:8] + "...",
            "amount": amount,
            "usd_value": 0
        }

async def fetch_all_wallets(wallet_addresses: List[str]):
    """
    Fetch data for all wallets concurrently
    """
    rate_limiter = RateLimiter(calls_per_second=50)
    
    # Configure client session with SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [get_wallet_tokens_async(session, wallet, rate_limiter) 
                for wallet in wallet_addresses]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_tokens = []
        for result in results:
            if isinstance(result, list):
                all_tokens.extend(result)
        
        return all_tokens

def main():
    st.title("Solana Wallet Token Tracker")
    
    # Example wallet addresses, replace with your logic to get these
    wallet_addresses = st.text_area("Enter wallet addresses (one per line):", "").split("\n")
    
    if st.button("Fetch Token Data"):
        with st.spinner("Fetching data..."):
            # Run the async function in a blocking way for Streamlit
            all_tokens = asyncio.run(fetch_all_wallets(wallet_addresses))
        
        if all_tokens:
            df = pd.DataFrame(all_tokens)
            st.dataframe(df)
        else:
            st.write("No tokens found or an error occurred.")

if __name__ == "__main__":
    main()