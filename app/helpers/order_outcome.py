import pdb
import ast

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5


class OrderOutcome:

    def get(self, minutesData, breakoutData):
        call = None
        callIndex = None

        for idx, minute in enumerate(minutesData):
            if float(minute[HIGH]) >= breakoutData['buyBreakout']:
                call = 'buy'
                callIndex = idx
                break
            elif float(minute[LOW]) <= breakoutData['sellBreakout']:
                call = 'sell'
                callIndex = idx
                break

        if call is None:
            return None

        profit_loss = 0
        if call == 'buy':
            for minuteData in minutesData[callIndex:]:
                if breakoutData['buyStoploss'] >= float(minuteData[LOW]):
                    profitLoss = breakoutData['buyStoploss'] - \
                        breakoutData['buyBreakout']
                    print("buy stoploss_hit:", round(profitLoss, 2))
                    break

                elif breakoutData['buyTarget'] <= float(minuteData[HIGH]):
                    profitLoss = breakoutData['buyTarget'] - \
                        breakoutData['buyBreakout']
                    print("eod_profit:", round(profitLoss, 2))
                    break

                else:
                    lastValue = float(minutesData[-1][CLOSE])
                    if lastValue > breakoutData['buyBreakout']:
                        profitLoss = lastValue - breakoutData['buyBreakout']
                        print("eod_profit:", round(profitLoss, 2))
                    elif lastValue < breakoutData['buyBreakout']:
                        profitLoss = lastValue - breakoutData['buyBreakout']
                        print("eod_los:", round(profitLoss, 2))
                    elif lastValue == breakoutData['buyBreakout']:
                        profitLoss = 0
                        print("eod:", profitLoss)

        elif call == 'sell':
            for minuteData in minutesData[callIndex:]:
                if breakoutData['sellStoploss'] <= float(minuteData[HIGH]):
                    profitLoss = breakoutData['sellBreakout'] - breakoutData['sellStoploss']
                    print("sell stoploss_hit:", round(profitLoss, 2))
                    break

                elif breakoutData['sellTarget'] >= float(minuteData[LOW]):
                    profitLoss = breakoutData['sellBreakout'] - breakoutData['sellTarget']
                    print("eod_profit:", round(profitLoss, 2))
                    break

                else:
                    lastValue = float(minutesData[-1][CLOSE])
                    if lastValue < breakoutData['sellBreakout']:
                        profitLoss = breakoutData['sellBreakout'] - lastValue
                        print("eod_profit:", round(profitLoss, 2))
                    elif lastValue > breakoutData['sellBreakout']:
                        profitLoss = breakoutData['sellBreakout'] - lastValue
                        print("eod_los:", round(profitLoss, 2))
                    elif lastValue == breakoutData['sellBreakout']:
                        profitLoss = 0
                        print("eod:", round(profitLoss, 2))

        if call == "buy":
            plPercentage = (profitLoss / breakoutData['buyBreakout']) * 100
        elif call == "sell":
            plPercentage = (profitLoss / breakoutData['sellBreakout']) * 100

        return {
            'call_type': call,
            'profit_loss': round(profitLoss, 2),
            'pl_percentage': round(plPercentage, 2)
        }