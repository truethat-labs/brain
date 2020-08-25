import pdb
import math
import numpy as np


class Gann:
    def squareOfNine(self, price):
        sqrt = math.sqrt(price)
        alphasup1, alphasup2, alphares1, alphares2 = (math.floor(
            sqrt) - 1), math.floor(sqrt), math.ceil(sqrt), (math.ceil(sqrt) + 1)
        center = alphasup1 ** 2

        # increment 8 times
        level1_01 = (math.sqrt(center) + 0.125) ** 2
        level1_02 = (math.sqrt(center) + 0.25) ** 2
        level1_03 = (math.sqrt(center) + 0.375) ** 2
        level1_04 = (math.sqrt(center) + 0.5) ** 2
        level1_05 = (math.sqrt(center) + 0.625) ** 2
        level1_06 = (math.sqrt(center) + 0.75) ** 2
        level1_07 = (math.sqrt(center) + 0.875) ** 2
        level1_08 = (math.sqrt(center) + 1) ** 2

        level1s = [level1_01, level1_02, level1_03, level1_04,
                   level1_05, level1_06, level1_07, level1_08]

        level2_01 = (alphasup2 + 0.125) ** 2
        level2_02 = (alphasup2 + 0.25) ** 2
        level2_03 = (alphasup2 + 0.375) ** 2
        level2_04 = (alphasup2 + 0.5) ** 2
        level2_05 = (alphasup2 + 0.625) ** 2
        level2_06 = (alphasup2 + 0.75) ** 2
        level2_07 = (alphasup2 + 0.875) ** 2
        level2_08 = (alphasup2 + 1) ** 2

        level2s = [level2_01, level2_02, level2_03, level2_04,
                   level2_05, level2_06, level2_07, level2_08]

        level3_01 = (alphares1 + 0.125) ** 2
        level3_02 = (alphares1 + 0.25) ** 2
        level3_03 = (alphares1 + 0.375) ** 2
        level3_04 = (alphares1 + 0.5) ** 2
        level3_05 = (alphares1 + 0.625) ** 2
        level3_06 = (alphares1 + 0.75) ** 2
        level3_07 = (alphares1 + 0.875) ** 2
        level3_08 = (alphares1 + 1) ** 2

        level3s = [level3_01, level3_02, level3_03, level3_04,
                   level3_05, level3_06, level3_07, level3_08]

        allvals = np.array([level1s, level2s, level3s]).flatten()

        lower_idx = 0
        for idx, val in enumerate(allvals):
            if val < price:
                lower_idx = idx

        sell_below = math.floor(allvals[lower_idx] * 5) / 5.0
        sell_target = math.floor(allvals[lower_idx - 1] * 5) / 5.0
        sell_target_l2 = math.floor(allvals[lower_idx - 2] * 5) / 5.0
        sell_target_l3 = math.floor(allvals[lower_idx - 3] * 5) / 5.0
        sell_target_l4 = math.floor(allvals[lower_idx - 4] * 5) / 5.0

        buy_above = math.floor(allvals[lower_idx + 1] * 5) / 5.0
        buy_target = math.floor(allvals[lower_idx + 2] * 5) / 5.0
        buy_target_l2 = math.floor(allvals[lower_idx + 3] * 5) / 5.0
        buy_target_l3 = math.floor(allvals[lower_idx + 4] * 5) / 5.0
        buy_target_l4 = math.floor(allvals[lower_idx + 5] * 5) / 5.0

        return {
            'buy_above': [buy_above, buy_target, buy_target_l2, buy_target_l3, buy_target_l4],
            'sell_below': [sell_below, sell_target, sell_target_l2, sell_target_l3, sell_target_l4]
        }
