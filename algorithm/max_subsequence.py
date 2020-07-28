# -*- coding=utf-8 -*-
class Solution:
    """
    题目:给定一个整数数组 nums ，
    找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
    """
    def maxSubArray(self, nums):
        """
        """
        self.dynamic_method(nums)

    def dynamic_method(self, nums):
        """
        dp[i] = max(dp[i-1], max_sum)
        """
        if not nums:
            return 0
        num_sum = 0
        max_sum = nums[0]
        for num in nums:
            num_sum = max(num_sum+num, num)
            max_sum = max(max_sum, num_sum)
        return max_sum

if __name__ == "__main__":
    print(Solution().maxSubArray([-1]))