import pdb
import json
import pandas as pd


symbols = pd.read_json("data/structured/good_price_symbols.json",
                       typ='series').keys()  # only Good price symbols
accuracyStock = pd.read_csv('data/structured/fno/accuracyStock.txt', header=None).values  # Very Good stock Symbols

onlyBuy = pd.read_csv('data/structured/fno/only_buy.txt',
                      header=None).values
onlySell = pd.read_csv('data/structured/fno/only_sell.txt',
                       header=None).values
reverseBuy = pd.read_csv('data/structured/fno/reverse_buy.txt',
                         header=None).values
reverseSell = pd.read_csv('data/structured/fno/reverse_sell.txt',
                          header=None).values

# Filter symbol only that usefull
data= {}
for symbol in symbols:
    if symbol in accuracyStock:
        if symbol in onlyBuy:
          data[symbol] = 'buy'
        elif symbol in onlySell:
          data[symbol] = 'sell'
        elif symbol in reverseBuy:
          data[symbol] = 'reverseBuy'
        elif symbol in reverseSell:
          data[symbol] = 'reverseSell'
        # json_data = json.dumps(data)
        with open('data/orb_nr_symbols.json', 'w') as outfile:
          json.dump(data, outfile, indent=2)
# pdb.set_trace()

