use std::collections::HashMap;

pub struct LetterNode {
    pub freq: i32,
    pub children: HashMap<char, Box<LetterNode>>,
}

impl LetterNode {
    #[inline]
    fn new() -> Self {
        LetterNode {
            freq: 0,
            children: HashMap::new(),
        }
    }
}

struct Solution;
impl Solution {
    pub fn sum_prefix_scores(words: Vec<String>) -> Vec<i32> {
        let mut root = LetterNode::new();

        // build trie
        for word in &words {
            let mut curr = &mut root;
            for c in word.chars() {
                curr = curr
                    .children
                    .entry(c)
                    .or_insert(Box::new(LetterNode::new()));
                curr.freq += 1;
            }
        }

        // calculate scores
        let mut scores = vec![0; words.len()];
        for (i, word) in words.iter().enumerate() {
            let mut curr = &root;
            for c in word.chars() {
                curr = curr.children.get(&c).unwrap().as_ref();
                scores[i] += curr.freq;
            }
        }

        scores
    }
}
fn main() {
    println!(
        "{:?}",
        Solution::sum_prefix_scores(
            vec!["abc", "ab", "bc", "b"]
                .iter()
                .map(|s| s.to_string())
                .collect()
        )
    );
}
