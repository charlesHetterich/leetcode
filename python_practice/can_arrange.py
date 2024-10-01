class Solution:
    def canArrange(self, arr: list[int], k: int) -> bool:
        # count # of items for each remainder of `k`
        remainder_counts = {}
        for x in arr:
            rem = x % k
            remainder_counts[rem] = remainder_counts.get(rem, 0) + 1

        # for each remainder, see if it has all available pairs
        for key, val in remainder_counts.items():
            if key == 0: # edge case for remainder of 0 should be self paired (can't have remainder k)
                if remainder_counts[key] % 2 != 0:
                    return False
                continue

            # items with remainder `key` can only be paired with items with
            # remainder `complement`. So we should expect their counts to be the same
            complement = k - key
            if remainder_counts.get(complement, 0) != remainder_counts[key]:
                return False
        return True