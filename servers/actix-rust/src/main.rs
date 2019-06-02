extern crate actix_web;
extern crate rand;
extern crate serde_json;

use actix_web::{actix, server, App, HttpRequest};
use std::time::{Instant};

fn main() {
  let address = "0.0.0.0:1234";
  let sys = actix::System::new("server");
  server::new(|| App::new().resource("/random", |r| r.f(random_handler)))
    .bind(address).unwrap().start();
  println!("Serving at {}", address);
  sys.run();

  fn random_handler(req: &HttpRequest) -> String {
    let start = Instant::now();

    let num = match req.query().get("num") {
      Some(n) => n.parse::<i32>().unwrap(),
      _ => 10
    };

    let rands: Vec<String> = get_randoms(num).iter()
      .map(|i| format!("{:06}", i)).collect();
    let ret = serde_json::to_string(&rands).unwrap();
    let elapsed_time = Instant::now().duration_since(start).as_micros();
    println!("{:0.3}ms", (elapsed_time as f32) / 1000.0);
    return ret;
  }

  fn get_randoms(num: i32) -> Vec<i32> {
    use rand::Rng;

    let mut ret: Vec<i32> = vec![];
    for _ in 0..num {
      ret.push(rand::thread_rng().gen_range(0, 1000000));
    }
    return ret;
  }
}
