# -*- coding=utf-8 -*-
class Solution:
    """
    题目：假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
    每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
    注意：给定 n 是一个正整数
    符合数学规律：斐波那契数列
    """
    def climbStairs(self, n: int):
        return self.get_climb_methods(n)
   
    def Recursion(self, n: int) -> int:
        if n in [0, 1]:
            return 1
        else:
            return self.climbStairs(n-1) + self.climbStairs(n-2)
    
    def Addition(self, n: int) -> int:
        dp = {}
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]
    
    climb_methods = []

    def get_climb_methods(self, n: int, lines=None) -> int:
        if lines is None:
            lines = []
        sum_lines = int(sum(lines))
        for num in [1,2]: 
            if sum_lines + num == n:
                lines.append(num)
                self.climb_methods.append(lines[:])
                lines.pop()
            elif sum_lines + num < n:
                lines.append(num)
                self.get_climb_methods(n, lines)
                lines.pop()
        return self.climb_methods
        
        
if __name__ == "__main__":
    print(Solution().climbStairs(5))