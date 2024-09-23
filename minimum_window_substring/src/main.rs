use std::collections::{HashSet, VecDeque};

struct Window(usize, usize);

struct Solution;
impl Solution {
    pub fn min_window(s: String, t: String) -> String {
        // create hashmap & hashset tracking characters in t
        let mut t_set: HashSet<char> = t.chars().collect();
        let mut t_map = std::collections::HashMap::new();
        for c in t.chars() {
            *t_map.entry(c).or_insert(0) += 1;
        }

        // iterate through s, track current/best window
        let mut best: Option<Window> = None;
        let mut cur = Window(0, 0);
        let mut positions = VecDeque::new();
        let mut s_chars: Vec<char> = vec![];
        for (i, c) in s.chars().enumerate() {
            s_chars.push(c);
            if let Some(count) = t_map.get_mut(&c) {
                // move end position --> next char
                cur.1 = i;
                *count -= 1;

                // add to position queue if not first (started here)
                if i != 0 {
                    positions.push_back(i);
                }

                // remove char from t_set if count <= 0
                if *count <= 0 {
                    t_set.remove(&c);
                }
                // (only at start) if start pos isn't a relevant character move it up
                if !t_map.contains_key(&s_chars[cur.0]) {
                    cur.0 = positions.pop_front().unwrap();
                }

                // move start position --> as much as possible
                while t_map[&s_chars[cur.0]] < 0 {
                    *t_map.get_mut(&s_chars[cur.0]).unwrap() += 1;
                    cur.0 = positions.pop_front().unwrap();
                }

                // if t_set empty, update best window
                if t_set.is_empty() {
                    match best {
                        Some(Window(start, end)) => {
                            if cur.1 - cur.0 < end - start {
                                best = Some(Window(cur.0, cur.1));
                            }
                        }
                        None => best = Some(Window(cur.0, cur.1)),
                    }
                }
            }
        }

        // return best window
        if let Some(Window(start, end)) = best {
            println!("{} {}", start, end);
            s.chars().skip(start).take(end - start + 1).collect()
        } else {
            "".to_string()
        }
    }
}

fn main() {
    println!(
        "{:?}",
        // Solution::min_window("ADOBECODEBANC".to_string(), "ABC".to_string())
        Solution::min_window("BbBABaABbbb".to_string(), "aA".to_string())
    );
}
