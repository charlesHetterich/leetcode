# Leetcode Problem: https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: Optional[ListNode]
        :type n: int
        :rtype: Optional[ListNode]
        """
        if not head:
            return None

        # find n'th last node
        i = 0
        curr = head
        nth_back_parent = None
        nth_back = None
        while curr:
            if i >= n - 1:
                if nth_back == None:
                    nth_back = head
                else:
                    nth_back_parent = nth_back
                    nth_back = nth_back.next
            curr = curr.next
            i += 1

        # remove n'th back from linked list
        if nth_back:
            if nth_back_parent:
                nth_back_parent.next = nth_back.next
            else:
                head = nth_back.next
            del nth_back
        return head
