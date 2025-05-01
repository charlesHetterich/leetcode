use std::collections::HashMap;

struct PathNode {
    val: i32,
    rem: i32,
    pub children: HashMap<char, Box<PathNode>>,
}

pub struct Solution {}
impl Solution {
    pub fn min_subarray(nums: Vec<i32>, p: i32) -> i32 {
        let mut rem = 0;
        let mut counts = HashMap::new();
        for n in nums {
            rem = (rem + n) % p;
            counts
                .entry(n)
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }

        // breadth-first search ?

        print!("{:?}", counts);
        0
    }
}
