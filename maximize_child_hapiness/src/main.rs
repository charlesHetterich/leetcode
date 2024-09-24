// use std::cmp::Reverse;

struct Solution;
impl Solution {
    pub fn maximum_happiness_sum(happiness: Vec<i32>, k: i32) -> i64 {
        let mut happiness = happiness;
        happiness.sort_by(|a, b| b.cmp(a));

        let mut sum: i64 = 0;
        for i in 0..k as usize {
            sum += (happiness[i] - i as i32).max(0) as i64;
        }
        sum
    }
}

fn main() {
    let scores = vec![2, 1, 3];
    println!("{:?}", Solution::maximum_happiness_sum(scores, 2));
}
