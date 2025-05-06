# Leetcode Problem: https://leetcode.com/problems/longest-valid-parentheses/description/


class Solution(object):
    def __init__(self):
        self.best = ""
        self.agg = ""

    def scoped_substr(self, s):
        """
        Given a substring `s` of s[i] in `[(, )]`, return the substring that
        completes the scope, assuming an unincluded starting "("

        Assume len(s) >= 1. Returns `None` if scope cannot be completed
        """
        # invalid
        if len(s) == 0 or s == "(":
            return None
        # complete scope
        if s[0] == ")":
            return s[0]

        # Build sub-scoped strings & aggregate them
        # until we hit this scope's ")" or run out of string
        i = 0
        agg = ""
        while i < len(s) and s[i] == "(":
            substr = self.scoped_substr(s[i + 1 :])
            if not substr:  # Failed to complete sub-scope
                return None
            # aggregate subscoped string
            agg += "(" + substr
            i += len(substr) + 1

        if i < len(s):  # found this scope's ")"
            return agg + ")"
        else:  # Failed to complete this scope
            return None

    def longestValidParentheses(self, s):
        """
        :type s: str
        :rtype: int
        """
        self.best = ""
        i = 0
        self.agg = ""

        def reset():
            if len(self.agg) > len(self.best):
                self.best = self.agg
            self.agg = ""

        while i < len(s) - 1:
            if s[i] == ")":
                i += 1
                reset()
                continue
            else:
                rest = self.scoped_substr(s[i + 1 :])
                if rest:
                    self.agg += "(" + rest
                    i += len(rest) + 1
                else:
                    i += 1
                    reset()

        reset()
        return len(self.best)
