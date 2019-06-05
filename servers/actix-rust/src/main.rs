#[macro_use]
extern crate actix_web;

extern crate rand;
extern crate serde_json;
extern crate serde_urlencoded;

use actix_web::{App, HttpRequest, HttpResponse, HttpServer, Result};
use actix_web::http::StatusCode;
use std::collections::HashMap;
use std::io;
use std::time::Instant;


#[get("/random")]
fn random_handler(req: HttpRequest) -> Result<HttpResponse> {
  let start = Instant::now();

  let num = req.uri().query().map_or(10, |q| {
      let pairs = serde_urlencoded::from_str::<HashMap<String, String>>(q)
        .unwrap();
      pairs.get("num").map_or(10, |n| n.parse::<i32>().unwrap())
  });
  let rands: Vec<String> = get_randoms(num).iter()
    .map(|i| format!("{:06}", i)).collect();
  let ret = Ok(HttpResponse::build(StatusCode::OK)
    .content_type("text/plain")
    .body(serde_json::to_string(&rands).unwrap()));

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

fn main() -> io::Result<()> {
  let sys = actix_rt::System::new("server");
  let address = "0.0.0.0:1234";
  HttpServer::new(|| {
      App::new().service(random_handler)
  })
  .bind(address)?.start();

  println!("Serving at {}", address);
  sys.run()
}
