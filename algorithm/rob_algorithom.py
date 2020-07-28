class Solution:
    """
    题目：你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，
    影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
    给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。
    """
    def rob(self, nums):
        """
        [2,7,9,3,1]
        a_sum = 2+9+1
        b_sum = 7 + 3
        [2,7,0, 1, 9,3,1]
        dp[i]= max(dp[i-1], nums[i] + dp[i-2])
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        a_sum = nums.pop(0)
        b_sum = nums.pop(1)
        for num in nums:
            b_sum, a_sum = max(a_sum+num, b_sum), b_sum
            
             

        