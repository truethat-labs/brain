import pdb
import json
from app.helpers.result import Result

result = Result()

############################################
# Testing:
# Buy breakout target reached
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/buy_breakout_target.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "buy" and response['resultType'] == 'target' and response['resultPoint'] > 0:
    print('PASSED: Buy breakout target reached')
else:
    print('FAILED: Buy breakout target reached')

############################################

############################################
# Testing:
# Buy breakout stoploss reached
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/buy_breakout_sl.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "buy" and response['resultType'] == 'stoploss' and response['resultPoint'] < 0:
    print('PASSED: Buy breakout stoploss reached')
else:
    print('FAILED: Buy breakout stoploss reached')

############################################

############################################
# Testing:
# Buy breakout EOD profit
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/buy_breakout_eod_profit.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "buy" and response['resultType'] == 'eod' and response['resultPoint'] > 0:
    print('PASSED: Buy breakout EOD profit')
else:
    print('FAILED: Buy breakout EOD profit')

############################################

############################################
# Testing:
# Buy breakout EOD loss
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/buy_breakout_eod_loss.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "buy" and response['resultType'] == 'eod' and response['resultPoint'] < 0:
    print('PASSED: Buy breakout EOD loss')
else:
    print('FAILED: Buy breakout EOD loss')

############################################

############################################
# Testing:
# Buy breakout EOD CTC
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/buy_breakout_eod_ctc.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "buy" and response['resultType'] == 'eod' and response['resultPoint'] == 0.0:
    print('PASSED: Buy breakout EOD CTC')
else:
    print('FAILED: Buy breakout EOD CTC')

############################################

############################################
# Testing:
# Sell breakout target reached
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/sell_breakout_target.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "sell" and response['resultType'] == 'target' and response['resultPoint'] > 0.0:
    print('PASSED: Sell breakout target reached')
else:
    print('FAILED: Sell breakout target reached')

############################################

############################################
# Testing:
# Sell breakout stoploss reached
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/sell_breakout_sl.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "sell" and response['resultType'] == 'stoploss' and response['resultPoint'] < 0.0:
    print('PASSED: Sell breakout stoploss reached')
else:
    print('FAILED: Sell breakout stoploss reached')

############################################

############################################
# Testing:
# Sell breakout EOD profit
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/sell_breakout_eod_profit.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "sell" and response['resultType'] == 'eod' and response['resultPoint'] > 0.0:
    print('PASSED: Sell breakout EOD profit')
else:
    print('FAILED: Sell breakout EOD profit')

############################################

############################################
# Testing:
# Sell breakout EOD loss
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/sell_breakout_eod_loss.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "sell" and response['resultType'] == 'eod' and response['resultPoint'] < 0.0:
    print('PASSED: Sell breakout EOD loss')
else:
    print('FAILED: Sell breakout EOD loss')

############################################

############################################
# Testing:
# Sell breakout EOD CTC
with open('tests/data/breakouts_reverse.json') as f:
    breakouts = json.load(f)

with open('tests/data/minutes_reverse/sell_breakout_eod_ctc.json') as f:
    minutes = json.load(f)

response = result.get(minutes, breakouts, "reverse")

if response['callSide'] == "sell" and response['resultType'] == 'eod' and response['resultPoint'] == 0.0:
    print('PASSED: Sell breakout EOD CTC')
else:
    print('FAILED: Sell breakout EOD CTC')

############################################
