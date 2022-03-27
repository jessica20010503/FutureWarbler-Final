import backtrader as bt
# 載入指定檔案路徑相關的模組
import os
from pathlib import Path
import datetime
from pandas import Period
import strategy_Function
# backtrader 裡的策略要用物件去撰寫，之後再去繼承
# 注意 bt.Strategy 的 S 是大寫，若寫錯會執行錯誤喔!!


class TestStrategy(bt.Strategy):
    # 定義時間點的參數(原先的策略)
    # 定義 MA 快線以及慢線的長度 、 RSI 及 KD 的參數
    params = (
        # MA
        ('MA_period_fast', 5),
        ('MA_period_slow', 15),
        # RSI
        #('RSI_period', 12),
        # KD
        #('K_period', 14),
        #('D_period', 3),
        # 移動停損點數，這邊先寫死，之後需接使用者填入的
        ('Trailing_stop', 20)
    )

    def __init__(self):
        # 初始化收盤價
        # [0] 代表指定為系統在回測中最新的一個資料
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        # 建立 order 變數，因原先只有在買單條件成立時，該變數才被建立，但在前面要判斷是否有持單時就無法使用該變數，故要先初始化該變數
        self.order = None
        # 初始化 MA 、 RSI 、KD 指標 (backtrader 內有很多內建的指標 (indicators)!!!)
        # MA
        self.ma1 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.MA_period_fast)
        self.ma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.MA_period_slow)
        self.crossover_MA = bt.indicators.CrossOver(self.ma1, self.ma2)
        """
        # RSI
        self.rsi = bt.indicators.RSI(
            self.datas[0], period=self.params.RSI_period)
        # KD
        self.k = bt.indicators.StochasticSlow(
            self.datas[0], period=self.params.K_period)
        self.d = bt.indicators.StochasticSlow(
            self.datas[0], period=self.params.D_period)
        #self.crossover_KD = bt.indicators.CrossOver(self.k, self.d)
        """

    # 得到訂單的成交價
    # 只要轉換 order 的狀態，就會觸發 notify 的事件

    def notify_order(self, order):
        # 如果只是轉換成 submitted 或 Accepted，就直接 return，不再去執行下方的動作，因這兩者只是訂單送出和接受，不會有訂單增加和減少的事情發生
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 判斷訂單狀單，如果是完成，就顯示被執行了，並顯示其成交的價格
        if order.status in [order.Completed]:
            # 記錄訂單完成後的交易時間點
            # 判斷是買單還是賣單，並且記錄它在 買 / 賣 的成交價是多少
            if order.isbuy():
                self.log("Buy Executed {}".format(order.executed.price))
            elif order.issell():
                self.log("Sell Executed {}".format(order.executed.price))
            # 紀錄成交的時間有多長，用 len(self) 可讓我們知道目前執行到第幾個 bar
            self.bar_executed = len(self)

        # 訂單有可能會因保證金不足等原因被券商拒絕，狀態就會是取消、保證金不足等以下三種狀態
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # 如果是以上的狀態就顯示訊息
            self.log("Order Canceled/Margin/Rejected")

        # 如果單被 執行 或 取消時，就要再把 self.order 變回 None
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("交易收益：毛利 %.2f 淨利：%.2f" % (trade.pnl, trade.pnlcomm))

    # 策略的主要邏輯，每次在買賣邏輯都會經過此段程式碼
    def next(self):
        # [0] 是因為上面的 .close 並非是一個數字，而是一個物件，要在這個物件呼叫數值就必須用 [0]
        self.log("Close {}".format(self.dataclose[0]))
        # 如果 self.order 還是 None，就會回傳 False，這邊希望他回傳 False 時，能進入下方的買賣判斷
        # 如果 self.order 內有物件就會滿足此條件，就會去做 return 的動作，就不會再去做下方的買賣判斷
        # 這邊主要是要判斷說單有沒有重複
        # 如果 return 的話，就不會再執行下方的程式碼了!!
        if self.order:
            return

        # 利用 self 裡的 position 來判斷是否已持有資產，若是無持有的資產就做買入的判斷，反之，若已有持有的資產，就做賣出的判斷
        # 買入賣出邏輯(SMA): 向上突破就買入，向下跌破就賣出

        crossover_MA = self.crossover_MA
        #crossover_KD = self.crossover_KD
        #rsi = self.rsi
        if not self.position:
            # 這邊需從使用者所選的判斷使用哪個策略邏輯，這裡先將他寫死，之後在做判斷
            # 以下為做多的 MA 買進
            strategy_Function.MA_1(self=self, crossover_MA=crossover_MA)
        else:
            # 這邊需從使用者所選的判斷使用哪個策略邏輯，這裡先將他寫死，之後在做判斷
            # 停損停利，這邊也需從使用者所選的判斷使用哪個策略邏輯，這裡先將他寫死，之後在做判斷
            # 以下為移動停損，停損點數這邊先在參數的地方寫死
            stopLoss = self.params.Trailing_stop
            tmpHigh = cerebro.broker.getvalue()
            TrailingStop = tmpHigh - stopLoss
            highPrice = self.datahigh
            if highPrice > tmpHigh:
                tmpHigh = highPrice
                TrailingStop = tmpHigh - stopLoss
            elif highPrice <= TrailingStop:
                print("跌出範圍啦 ><!! 趕快給你賣出來止損!")
                self.order = self.sell()
            # 若前面停損條件沒符合，就看策略的部分
            else:
                # 以下為做多的 MA 賣出
                strategy_Function.MA_2(self=self, crossover_MA=crossover_MA)

    # 定義 log 函數: 接受一個文字訊息，並將其印出

    def log(self, txt):
        # 想要多顯示其它的資訊，便在以下設置
        # dt : 最新市場訊息裡的 datetime
        dt = self.datas[0].datetime.date(0)
        #印出時間(換成日期的) & 收盤價訊息(txt)
        print("{} {}".format(dt.isoformat(), txt))

    # 顯示每次優化參數的結果是多少，這邊要列印出當時的參數值及其跑出來的資產價格是多少
    """
    def stop(self):
        print(self.params.maperiod, self.broker.getvalue())
    """


if __name__ == '__main__':
    # backtrader 一開始需初始化 cerebo，這個值是用來幫助資料做回測的
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000000)
    # 加入券商手續費
    cerebro.broker.setcommission(commission=0.001)
    # 將前面設置好的 TestStrategy 策略加入 backtrader
    # 使用一定比例的帳戶餘額去買進
    cerebro.addsizer(bt.sizers.PercentSizer, percents=30)
    cerebro.addstrategy(TestStrategy)
    """
    # 優化參數，這邊指的是均線長度這個參數，給定一範圍，去找得出結果能是最好的值
    # range(a,b) 指的是要優化的參數的範圍
    cerebro.optstrategy(TestStrategy,
                        maperiod=range(10, 31))
    """
    # 初始化檔案路徑
    data_path = Path(os.getcwd()) / \
        'Data/MXF1-Minute-Trade(小台指分鐘-2016-1-1至2021--12-22).csv'
    # 餵資料源(這邊 YahooFinance 本身在 backtrader 裡已有對應的寫法)
    # dataname 是一重要參數，該部分主要是設定資料要餵進去的位置
    data = bt.feeds.GenericCSVData(dataname=data_path,
                                   fromdate=datetime.datetime(2016, 1, 4),
                                   todate=datetime.datetime(2017, 2, 18),
                                   nullvalue=0.0,

                                   dtformat=('%Y/%m/%d'),
                                   tmformat=('%H:%M:%S'),
                                   date=0,
                                   time=1,
                                   high=3,
                                   low=4,
                                   open=2,
                                   close=5,
                                   volume=6,
                                   openinterest=-1)
    cerebro.adddata(data)
    # cerebro 初始值裡會有一個值叫 broker，是券商的資料，這邊是要取得券商初始化的資產
    # 前面的 {} 表示 .format 裡的東西會去取代這個 {}
    print("Start Portfolio {}".format(cerebro.broker.getvalue()))
    start_value = cerebro.broker.getvalue()
    # 當執行 cerebro 這個方法時，cerebro 就會去迭代所有資料，並且計算我們策略回測出來的績效
    # 加入績效分析
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SR')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='RS')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
    results = cerebro.run()
    start = results[0]
    end_value = cerebro.broker.getvalue()
    # 看最後資產的總價值是多少
    print("Final Portfolio {}".format(cerebro.broker.getvalue()))
    print('收益:{:,.2f}'.format(end_value-start_value))
    print('年利潤:', start.analyzers.AnnualReturn.get_analysis())
    print('最大策略虧損:', start.analyzers.DW.get_analysis()["max"]["drawdown"])
    print('夏普指數:', start.analyzers.SR.get_analysis()["sharperatio"])
    print('總收益率:', start.analyzers.RS.get_analysis()["rtot"])
    #print('贏交易分析:', start.analyzers.TradeAnalyzer.get_analysis()['won'])
    #print('輸交易分析:', start.analyzers.TradeAnalyzer.get_analysis()['lost'])
    # 賺賠比 = 平均賺 / 平均賠
    print('賺賠比:{:,.2f}'.format(start.analyzers.TradeAnalyzer.get_analysis()[
          'won']['pnl']['average'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['average'])))
    # 獲利因子 = 賺得和 / |賠的和|
    print('獲利因子:{:,.2f}'.format(start.analyzers.TradeAnalyzer.get_analysis()[
          'won']['pnl']['total'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['total'])))
    print('總交易次數:', start.analyzers.TradeAnalyzer.get_analysis()
          ['total']['total'])
    print('盈利次數:', start.analyzers.TradeAnalyzer.get_analysis()
          ['won']['total'])
    print('虧損次數:', start.analyzers.TradeAnalyzer.get_analysis()
          ['lost']['total'])
    print('勝率: {:,.2f}'.format(start.analyzers.TradeAnalyzer.get_analysis()
          ['won']['total'] / start.analyzers.TradeAnalyzer.get_analysis()
          ['total']['total']))
    # SNQ 1.6~1.9凑合用，2.0~2.4普通，2.5~2.9好，3.0~5.0杰出，5.1~6.0一流，7.0以上极好，SNQ=（平均获利/标准差）*年交易次数的平方根
    print("SQN:{}".format(start.analyzers.SQN.get_analysis()["sqn"]))
    # 在 cerebro 把所有回測結果 run 完後，就能使用內建的繪圖功能來製作圖表(損益圖，內還會有資產、買點賣點等損益的情況)
    cerebro.plot()
