# Leetcode Problem: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
#
# Going to try a BFS method


# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


def isnumeric(c):
    return c in "0123456789-"


class Codec:

    def append_node(self, agg, node):
        val = str(node.val) if node else "_"
        return agg + val + ","

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        # agg = f"{root.val if root else "_"},"
        agg = self.append_node("", root)

        stack = [root] if root else []
        while stack:
            node = stack.pop(0)
            agg = self.append_node(agg, node.left)
            agg = self.append_node(agg, node.right)
            # agg += f"{node.left.val if node.left else "_"},{node.right.val if node.right else "_"},"
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return agg

    def get_node(self, data):
        """
        Gets a node given the value at the front of data. Returns a tuple of the node & its value's length in the string
        """
        if data[0] == "_":
            return None, 1
        agg, pos = "", 0
        # if data[0] == "-":
        #     agg = "-"
        #     pos = 1

        while isnumeric(data[pos]):
            agg += data[pos]
            pos += 1

        return TreeNode(int(agg)), pos

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        # root = TreeNode(int(data[0])) if data[0] != "_" else None
        root, cut_len = self.get_node(data)

        stack = [root]
        while stack:
            node = stack.pop(0)
            if not node:
                continue

            data = data[cut_len + 1 :]
            node.left, cut_len = self.get_node(data)
            data = data[cut_len + 1 :]
            node.right, cut_len = self.get_node(data)
            stack.extend([node.left, node.right])

        return root


# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
