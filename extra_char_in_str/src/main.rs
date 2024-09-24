use std::collections::HashSet;

struct Solution {}
impl Solution {
    fn get_ex_char(i: usize, s: &String, d_set: &HashSet<&str>, ex_chars: &mut Vec<i32>) -> i32 {
        if i >= s.len() {
            return 0;
        }
        if ex_chars[i] != -1 {
            return ex_chars[i];
        }

        let mut result = 1 + Solution::get_ex_char(i + 1, s, d_set, ex_chars);
        for j in i..s.len() {
            if d_set.contains(&s[i..j + 1]) {
                result = result.min(Solution::get_ex_char(j + 1, s, d_set, ex_chars));
            }
        }

        ex_chars[i] = result;
        result
    }

    pub fn min_extra_char(s: String, dictionary: Vec<String>) -> i32 {
        let dict_set: HashSet<&str> = dictionary.iter().map(|s| s.as_str()).collect();

        let mut ex_chars = vec![-1; s.len() + 1];
        Solution::get_ex_char(0, &s, &dict_set, &mut ex_chars)
    }
}

fn main() {
    println!(
        "{:?}",
        Solution::min_extra_char(
            "dwmodizxvvbosxxw".to_string(),
            vec![
                "ox", "lb", "diz", "gu", "v", "ksv", "o", "nuq", "r", "txhe", "e", "wmo", "cehy",
                "tskz", "ds", "kzbu"
            ]
            .iter()
            .map(|s| s.to_string())
            .collect()
        )
    );
}
