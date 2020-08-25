import pdb
import math


class Stoploss:
    def orbStoploss(self, buyBreakout, sellBreakout, target, stoploss):
        return {
            'buySl': (math.ceil((buyBreakout * (stoploss/100))*10))/10.0,
            'sellSl': (math.ceil((sellBreakout * (stoploss/100))*10))/10.0,
            'buyTarget': (math.floor((buyBreakout * (target/100))*10))/10.0,
            'sellTarget': (math.floor((sellBreakout * (target/100))*10))/10.0
        }

    def orbNrStoploss(self, buyBreakout, sellBreakout, rangeDiff, capital, targetPercent):
        targetPercent = targetPercent/100
        qty = math.floor(((capital*0.01)/(rangeDiff)))
        return {
            'buySl': math.ceil((rangeDiff)*10)/10.0,
            'sellSl': math.ceil((rangeDiff)*10)/10.0,
            'buyTarget': math.floor((buyBreakout * targetPercent)*10)/10.0,
            'sellTarget': math.floor((sellBreakout * targetPercent)*10)/10.0,
            'qty': qty
        }
