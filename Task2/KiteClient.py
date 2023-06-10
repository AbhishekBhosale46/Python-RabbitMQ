from kiteconnect import KiteConnect
import pandas as pd

kite = KiteConnect(api_key="r7hc14ebmbr16tv9")
kite.set_access_token("QVbOmi5MpiZr2jtbKNxjVgrNq0Gm6aJF")

# print(kite.profile())

# profile = kite.profile()
 
# response_message = {
#     'name': profile['user_name'],
#     'userid': profile['user_id']
# }

# print(kite.margins()['equity']['net'])

# print(kite.margins()['equity']['available']['cash'])

# print(kite.ltp('BSE:INFY'))

jsonData = kite.holdings()[0]
df = pd.DataFrame.from_dict(jsonData, orient='index').T
print(df)

