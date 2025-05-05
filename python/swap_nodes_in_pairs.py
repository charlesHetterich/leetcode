# Leetcode Problem: https://leetcode.com/problems/swap-nodes-in-pairs/description/


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def swapPairs(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        i = 0
        prev = None
        curr = head
        while curr:
            # step forward
            prev = curr
            curr = curr.next

            # swap on every other step
            if curr and i % 2 == 0:
                tmp = prev.val
                prev.val = curr.val
                curr.val = tmp
            i += 1
        return head
