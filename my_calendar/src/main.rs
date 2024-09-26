use std::cmp::Ordering;

struct MyCalendar {
    bookings: Vec<(i32, i32)>,
}

impl MyCalendar {
    fn new() -> Self {
        MyCalendar { bookings: vec![] }
    }

    fn book(&mut self, start: i32, end: i32) -> bool {
        match self.bookings.binary_search_by(|&(s, e)| {
            if end <= s {
                Ordering::Greater
            } else if start >= e {
                Ordering::Less
            } else {
                Ordering::Equal
            }
        }) {
            // If there's a conflict
            Ok(_) => false,
            // If no conflict, insert in sorted order
            Err(pos) => {
                self.bookings.insert(pos, (start, end));
                true
            }
        }
    }
}

fn main() {
    let bookings = vec![(5, 10), (2, 5), (1, 3), (1, 2)];
    let mut obj = MyCalendar::new();

    let mut booked = vec![];
    for (start, end) in bookings {
        booked.push(obj.book(start, end));
    }

    println!("{:?}", booked);
}
