set datafile missing "NA"
set datafile separator ","
set ylabel font ",14"
set xlabel font ",14"
set grid x
set grid y

set terminal png size 960, 800 fontscale 1.2

set output "images/wc-client-2MBps-median.png"
set key on top left horizontal
set ylabel "Median requests per second as observed on client-side"
set xlabel "Number of concurrent requests per client"
plot "data/wc-client-perf.txt" index 0 every 3::0 using 1:6 title "actix-rust" with linespoints, \
    "data/wc-client-perf.txt" index 1 every 3::0 using 1:6 title "go" with linespoints, \
    "data/wc-client-perf.txt" index 2 every 3::0 using 1:6 title "nodejs-express-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 3 every 3::0 using 1:6 title "nodejs-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 4 every 3::0 using 1:6 title "ktor-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 5 every 3::0 using 1:6 title "micronaut-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 6 every 3::0 using 1:6 title "ratpack-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 7 every 3::0 using 1:6 title "vertx-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 8 every 3::0 using 1:6 title "phoenix-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 9 every 3::0 using 1:6 title "trot-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 10 every 3::0 using 1:6 title "flask+uwsgi-python3" with linespoints, \
    "data/wc-client-perf.txt" index 11 every 3::0 using 1:6 title "tornado-python3" with linespoints, \
    "data/wc-client-perf.txt" index 12 every 3::0 using 1:6 title "cowboy-erlang" with linespoints

set output "images/wc-client-6MBps-median.png"
set key on top left horizontal
set ylabel "Median requests per second as observed on client-side"
set xlabel "Number of concurrent requests per client"
plot "data/wc-client-perf.txt" index 0 every 3::1 using 1:6 title "actix-rust" with linespoints, \
    "data/wc-client-perf.txt" index 1 every 3::1 using 1:6 title "go" with linespoints, \
    "data/wc-client-perf.txt" index 2 every 3::1 using 1:6 title "nodejs-express-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 3 every 3::1 using 1:6 title "nodejs-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 4 every 3::1 using 1:6 title "ktor-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 5 every 3::1 using 1:6 title "micronaut-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 6 every 3::1 using 1:6 title "ratpack-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 7 every 3::1 using 1:6 title "vertx-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 8 every 3::1 using 1:6 title "phoenix-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 9 every 3::1 using 1:6 title "trot-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 10 every 3::1 using 1:6 title "flask+uwsgi-python3" with linespoints, \
    "data/wc-client-perf.txt" index 11 every 3::1 using 1:6 title "tornado-python3" with linespoints, \
    "data/wc-client-perf.txt" index 12 every 3::1 using 1:6 title "cowboy-erlang" with linespoints

set output "images/wc-client-10MBps-median.png"
set key on top left horizontal
set ylabel "Median requests per second as observed on client-side"
set xlabel "Number of concurrent requests per client"
plot "data/wc-client-perf.txt" index 0 every 3::2 using 1:6 title "actix-rust" with linespoints, \
    "data/wc-client-perf.txt" index 1 every 3::2 using 1:6 title "go" with linespoints, \
    "data/wc-client-perf.txt" index 2 every 3::2 using 1:6 title "nodejs-express-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 3 every 3::2 using 1:6 title "nodejs-javascript" with linespoints, \
    "data/wc-client-perf.txt" index 4 every 3::2 using 1:6 title "ktor-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 5 every 3::2 using 1:6 title "micronaut-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 6 every 3::2 using 1:6 title "ratpack-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 7 every 3::2 using 1:6 title "vertx-kotlin" with linespoints, \
    "data/wc-client-perf.txt" index 8 every 3::2 using 1:6 title "phoenix-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 9 every 3::2 using 1:6 title "trot-elixir" with linespoints, \
    "data/wc-client-perf.txt" index 10 every 3::2 using 1:6 title "flask+uwsgi-python3" with linespoints, \
    "data/wc-client-perf.txt" index 11 every 3::2 using 1:6 title "tornado-python3" with linespoints, \
    "data/wc-client-perf.txt" index 12 every 3::2 using 1:6 title "cowboy-erlang" with linespoints
