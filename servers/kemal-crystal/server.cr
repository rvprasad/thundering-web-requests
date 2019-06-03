require "kemal"

def get_randoms(nums)
  rand = Random.new
  (1..nums).map { "%06d" % rand.rand(0...1000000) }
end

get "/random" do |env|
  ret = ""
  elapsed_time = Time.measure do
    nums = env.params.query.fetch("num", "10").to_i()
    ret = "[" + get_randoms(nums).join(",") + "]"
  end
  puts "%.3fms" % (elapsed_time.total_nanoseconds / 1e6)
  ret
end

Kemal.config.logging = false
Kemal.config.port = 1234
puts "Serving at 0.0.0.0:1234"
Kemal.run
