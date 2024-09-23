struct Solution;

impl Solution {
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        let mut nums = nums;
        let mut s_nums = nums.clone();
        s_nums.sort();

        let mut s = 0;
        let mut e = s_nums.len() - 1;

        while s_nums[s] + s_nums[e] != target {
            if s_nums[s] + s_nums[e] > target {
                e -= 1;
            } else {
                s += 1;
            }
        }

        let a = s_nums[s];
        let b = s_nums[e];

        if a != b {
            vec![
                nums.iter().position(|&x| x == a).unwrap() as i32,
                nums.iter().position(|&x| x == b).unwrap() as i32,
            ]
        } else {
            s = nums.iter().position(|&x| x == a).unwrap();
            nums.remove(s);
            e = nums.iter().position(|&x| x == b).unwrap() + 1;

            vec![s as i32, e as i32]
        }
    }
}

fn main() {
    let nums = vec![11, 7, 2, 15];
    let target = 9;
    println!("{:?}", Solution::two_sum(nums, target));
    // Solution::two_sum(nums, target);
}
