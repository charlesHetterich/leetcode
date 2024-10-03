mod problems;

fn main() {
    let s = String::from("aaabbb");
    let result = problems::LS::Solution::length_of_longest_substring(s);
    println!("Result: {}", result);
}
