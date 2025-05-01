mod problems;

fn main() {
    let p = 6;
    let arr = vec![3, 1, 4, 2];
    let result =
        problems::MSD::Solution::min_subarray(arr, p);
    println!("Result: {}", result);
}
