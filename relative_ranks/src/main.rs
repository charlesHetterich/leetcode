struct Solution;
impl Solution {
    pub fn find_relative_ranks(score: Vec<i32>) -> Vec<String> {
        let mut indices = (0..score.len()).collect::<Vec<usize>>();
        indices.sort_unstable_by(|&a, &b| score[b].cmp(&score[a]));

        let mut res = vec![String::new(); score.len()];
        for (i, &idx) in indices.iter().enumerate() {
            res[idx] = match i {
                0 => "Gold Medal".to_string(),
                1 => "Silver Medal".to_string(),
                2 => "Bronze Medal".to_string(),
                _ => (i + 1).to_string(),
            };
        }

        res
    }
}
fn main() {
    let scores = vec![3, 4, 5, 2, 1];
    println!("{:?}", Solution::find_relative_ranks(scores));
}
