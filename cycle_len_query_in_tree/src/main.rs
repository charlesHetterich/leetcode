use std::collections::HashMap;

//Right... this could be a lot simpler (no need to track history) if we only move the value thats larger
struct Solution;
impl Solution {
    fn move_node_up(mut v: i32) -> i32 {
        // this can be replaced by `>>` operator (ex: v >>= 1 [right-shift bits by 1])
        if v % 2 == 1 {
            v -= 1;
        }
        v /= 2;
        v
    }

    pub fn cycle_length_queries(_: i32, queries: Vec<Vec<i32>>) -> Vec<i32> {
        queries
            .iter()
            .map(|q| {
                let (mut a, mut b) = (q[0], q[1]);
                let (mut a_hist, mut b_hist) = (HashMap::new(), HashMap::new());
                a_hist.insert(a, 0);
                b_hist.insert(b, 0);

                // let mut hit = false;
                let mut len = 1;
                loop {
                    // move 'a' node up
                    if !b_hist.contains_key(&a) {
                        if a != 1 {
                            a = Solution::move_node_up(a);
                            a_hist.insert(a, a_hist.len());
                            len += 1;
                        }
                    } else {
                        len -= b_hist.len() - b_hist[&a] - 1;
                        break;
                    }

                    // move 'b' node up
                    if !a_hist.contains_key(&b) {
                        if b != 1 {
                            b = Solution::move_node_up(b);
                            b_hist.insert(b, b_hist.len());
                            len += 1;
                        }
                    } else {
                        len -= a_hist.len() - a_hist[&b] - 1;
                        break;
                    }
                }

                len as i32
            })
            .collect()
    }
}
fn main() {
    let mut k = 20;
    while k > 1 {
        println!("{k}");
        k >>= 1
    }
    println!("{k}");

    let n = 3;
    let queries = vec![vec![5, 3], vec![4, 7], vec![2, 3]];
    println!("{:?}", Solution::cycle_length_queries(n, queries));
}
