# 移動停損
def trailingStop(self, dataclose, tmpHigh, stopLoss):
    TrailingStop = tmpHigh - stopLoss
    if dataclose > tmpHigh:
        tmpHigh = dataclose
        TrailingStop = tmpHigh - stopLoss
    elif dataclose <= TrailingStop:
        print("跌出範圍啦 ><!! 趕快給你賣出來止損!")
        self.order = self.sell()


# MA 做多買進
def MA_1(self, crossover_MA):
    if crossover_MA > 0:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# MA 做多賣出
def MA_2(self, crossover_MA):
    if crossover_MA < 0:
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()


# MA 做空買進
def MA_3(self, crossover_MA):
    if crossover_MA < 0:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# MA 做空賣出
def MA_4(self, crossover_MA):
    if crossover_MA > 0:
        # 賣出邏輯
        # 若快線向下超越慢線，就創造一賣單，並顯示其賣單的價格
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()


# RSI 做多買進
def RSI_1(self, rsi):
    if rsi > 50:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# RSI 做多賣出
def RSI_2(self, rsi):
    if rsi < 30 or rsi > 80:
        # 賣出邏輯
        # 若快線向下超越慢線，就創造一賣單，並顯示其賣單的價格
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()


# RSI 做空買進
def RSI_3(self, rsi):
    if rsi < 50:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# RSI 做空賣出
def RSI_4(self, rsi):
    if rsi < 20 or rsi > 70:
        # 賣出邏輯
        # 若快線向下超越慢線，就創造一賣單，並顯示其賣單的價格
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()


# KD 做多買進
def KD_1(self, crossover_KD):
    if crossover_KD > 0:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# KD 做多賣出
def KD_2(self, crossover_KD):
    if crossover_KD < 0:
        # 賣出邏輯
        # 若快線向下超越慢線，就創造一賣單，並顯示其賣單的價格
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()


# KD 做空買進
def KD_3(self, crossover_KD):
    if crossover_KD < 0:
        self.log("Buy Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.buy()


# KD 做空賣出
def KD_4(self, crossover_KD):
    if crossover_KD > 0:
        # 賣出邏輯
        # 若快線向下超越慢線，就創造一賣單，並顯示其賣單的價格
        self.log("Sell Create {}".format(self.dataclose[0]))
        # 產生一個訂單(order)
        self.order = self.sell()
