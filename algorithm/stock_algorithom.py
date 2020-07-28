# -*- coding=utf-8 -*-
class Solution:
    """
    题目：给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
    如果你最多只允许完成一笔交易（即买入和卖出一支股票一次），
    设计一个算法来计算你所能获取的最大利润。
    注意：你不能在买入股票前卖出股票。
    """
    
    def maxProfit(self, prices):
        """
        """
        return self.onceTraverse(prices)

    def onceTraverse(self, prices): 
        """
        一次遍历: 计算历史最多价
        多次遍历：计算未来最高价
        """
        if not prices:
            return 0
        min_price = prices[0]
        max_profit = 0
        for price in prices:
            max_profit = max(max_profit, price-min_price)
            min_price = min(min_price, price)
        return max_profit
    
    def dynamic_method(self, prices):
        """
        dp[i]=max(dp[i−1], prices[i]−minprice)
        """
        n = len(prices)
        if n == 0: return 0 # 边界条件
        dp = [0] * n
        minprice = prices[0] 

        for i in range(1, n):
            minprice = min(minprice, prices[i])
            dp[i] = max(dp[i - 1], prices[i] - minprice)

        return dp[-1]
         


abc = Solution()
print(abc.maxProfit([7,6,3,4,1]))