import pdb
import ast

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

class Result:
    # breakoutData mandatory fields
    # buyBreakout, sellBreakout, buyStoploss, sellStoploss, buyTarget, sellTarget, quantity
    # quantity can be 1 or anything based on the strategy
    def get(self, minutesData, breakoutData, type = "single"):
        calls = []
        callIndices = []

        if type == "single":
            for idx, minute in enumerate(minutesData):
                if float(minute[HIGH]) >= breakoutData['buyBreakout']:
                    calls.append({ 'type': 'buy', 'index': idx })
                    break
                elif float(minute[LOW]) <= breakoutData['sellBreakout']:
                    calls.append({ 'type': 'sell', 'index': idx })
                    break
        elif type == "reverse":
            for idx, minute in enumerate(minutesData):
                if float(minute[LOW]) <= breakoutData['buyBreakout']:
                    calls.append({ 'type': 'buy', 'index': idx })
                    break
                elif float(minute[HIGH]) >= breakoutData['sellBreakout']:
                    calls.append({ 'type': 'sell', 'index': idx })
                    break

        if len(calls) == 0:
            return None

        if type == "single" or type == "reverse":
            return self.__singleSided(calls, minutesData, breakoutData)
        else:
            return self.__twoSided(calls, minutesData, breakoutData)

    def summary(data):
        # passing the profit loss data to calculate a summary to see, if the strategy is worth it
        # arg should contain date, callType, resultType, resultPoint, quantity
        # return accuracy percentage, number of months, number of profitable months
        # number of loss months, max drawdown, max continous profit
        # average profit per day, min profit per day, max profit per day
        # average loss per day, min loss per day, max loss per day
        # average loss profit per month, average loss per month
        # expected average profit per month
        # expected average loss per month
        # expected average profit and loss per year
        return None

    # Private functions

    def __singleSided(self, calls, minutesData, breakoutData):
        singleCall = calls[0]
        if singleCall['type'] == "buy":
            return self.__buyCall(singleCall, minutesData, breakoutData)
        else:
            return self.__sellCall(singleCall, minutesData, breakoutData)

    def __twoSided(self, calls, minutesData, breakoutData):
        pdb.set_trace()
        return None

    def __buyCall(self, singleCall, minutesData, breakoutData):
        afterTriggerMinutesData = minutesData[singleCall['index']:]
        resultPoints = 0
        resultType = None
        for minute in afterTriggerMinutesData:
            if float(minute[LOW]) <= float(breakoutData['buyStoploss']):
                resultType = 'stoploss'
                resultPoints = float(breakoutData['buyStoploss']) - float(breakoutData['buyBreakout'])
                break
            elif float(minute[HIGH]) >= float(breakoutData['buyTarget']):
                resultType = 'target'
                resultPoints = float(breakoutData['buyTarget']) - float(breakoutData['buyBreakout'])
                break
            else:
                resultType = 'eod'
                resultPoints = float(minute[CLOSE]) - float(breakoutData['buyBreakout'])
        return { 'callSide': singleCall['type'], 'resultType': resultType, 'resultPoint': resultPoints }

    def __sellCall(self, singleCall, minutesData, breakoutData):
        afterTriggerMinutesData = minutesData[singleCall['index']:]
        resultPoints = 0
        resultType = None
        for minute in afterTriggerMinutesData:
            if float(minute[HIGH]) >= float(breakoutData['sellStoploss']):
                resultType = 'stoploss'
                resultPoints = float(breakoutData['sellBreakout']) - float(breakoutData['sellStoploss'])
                break
            elif float(minute[LOW]) <= float(breakoutData['sellTarget']):
                resultType = 'target'
                resultPoints = float(breakoutData['sellBreakout']) - float(breakoutData['sellTarget'])
                break
            else:
                resultType = 'eod'
                resultPoints = float(breakoutData['sellBreakout']) - float(minute[CLOSE])
        return { 'callSide': singleCall['type'], 'resultType': resultType, 'resultPoint': resultPoints }
