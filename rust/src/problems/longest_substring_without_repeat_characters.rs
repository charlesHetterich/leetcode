use std::collections::HashSet;

pub struct Solution;
impl Solution {
    pub fn length_of_longest_substring(s: String) -> i32 {
        let mut best_len = 0;
        let mut section_start: usize = 0;
        let mut char_set = HashSet::new();
        let chars: Vec<char> = s.chars().collect();
        for (i, c) in chars.iter().enumerate() {
            // step forward start pos until substring is valid
            while char_set.contains(&c) {
                char_set.remove(&chars[section_start]);
                section_start += 1;
            }

            // 1. insert new char
            // 2. see if currently @ best len
            char_set.insert(c);
            let section_len = i - section_start + 1;
            if section_len > best_len {
                best_len = section_len;
            }
        }

        best_len as i32
    }
}
