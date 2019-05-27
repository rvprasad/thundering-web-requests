extern crate actix_web;
extern crate rand;
extern crate serde_json;

use actix_web::{server, App, HttpRequest};

fn main() {
  server::new(|| App::new().resource("/random", |r| r.f(random_handler)))
    .bind("0.0.0.0:1234").unwrap().run();

  fn random_handler(req: &HttpRequest) -> String {

    let num = match req.query().get("num") {
      Some(n) => n.parse::<i32>().unwrap(),
      _ => 10
    };

    let rands: Vec<String> = get_randoms(num).iter()
      .map(|i| format!("{:06}", i)).collect();
    return serde_json::to_string(&rands).unwrap();
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
