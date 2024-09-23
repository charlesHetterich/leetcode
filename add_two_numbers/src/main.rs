struct Solution;

// Definition for singly-linked list.
#[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { val, next: None }
    }
}
impl Solution {
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        let mut l1 = l1;
        let mut l2 = l2;

        let mut carry = 0;
        let mut a: Option<Box<ListNode>> = None;
        let mut c = &mut a;
        while l1.is_some() || l2.is_some() {
            // add carry value
            let mut sum = carry;

            // add current nodes
            if let Some(node) = &l1 {
                sum += node.val;
            }
            if let Some(node) = &l2 {
                sum += node.val;
            }

            // calculate  next node and carry
            carry = sum / 10;
            let remainder = sum % 10;

            // create and add next node
            let mut node = Box::new(ListNode::new(remainder));
            *c = Some(node);

            // move to next node
            c = &mut c.as_mut().unwrap().next;
            // l1 = l1.unwrap().next;
            // l2 = l2.unwrap().next;

            l1 = l1.and_then(|node| node.next);
            l2 = l2.and_then(|node| node.next);
        }

        if carry > 0 {
            *c = Some(Box::new(ListNode::new(carry)));
        }

        return a;
    }
}
fn main() {
    println!("{:?}", Option::Some(Box::new(ListNode::new(1))));

    let mut l1 = Some(Box::new(ListNode::new(2)));
    {
        let mut current = l1.as_mut().unwrap();
        current.next = Some(Box::new(ListNode::new(4)));
        current = current.next.as_mut().unwrap();
        current.next = Some(Box::new(ListNode::new(3)));
    }

    // Create second linked list: 5 -> 6 -> 4
    let mut l2 = Some(Box::new(ListNode::new(5)));
    {
        let mut current = l2.as_mut().unwrap();
        current.next = Some(Box::new(ListNode::new(6)));
        current = current.next.as_mut().unwrap();
        current.next = Some(Box::new(ListNode::new(4)));
        current = current.next.as_mut().unwrap();
        current.next = Some(Box::new(ListNode::new(1)));
    }

    println!("{:?}", Solution::add_two_numbers(l1, l2));
}
