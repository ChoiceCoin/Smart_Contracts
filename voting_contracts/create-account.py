#!/usr/bin/env python
import base64
from typing import List, Any, Optional
import algosdk
from algosdk import mnemonic


sk, pk = algosdk.account.generate_account()
print(f"""
  creator_mnemonic: {mnemonic.from_private_key(sk)}
""")

sk, pk = algosdk.account.generate_account()
print(f"""
  user_mnemonic: {mnemonic.from_private_key(sk)}
""")