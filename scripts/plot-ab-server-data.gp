set datafile missing "NA"
set datafile separator ","
set ylabel font ",14"
set xlabel font ",14"
set grid x
set grid y
do for [i=1:15] {
    set style line i linewidth 2
}

set terminal png size 960, 960 fontscale 1.2

set logscale y

set output "images/ab-server-2MBps-median.png"
set key on bottom right horizontal
set xlabel "Number of concurrent requests per client node"
set ylabel "Median requests per second as observed on server-side" offset 2
plot "data/ab-server-perf.txt" index 0 every 3::0 using 1:9 title "actix-rust" with linespoints, \
    "data/ab-server-perf.txt" index 1 every 3::0 using 1:9 title "go" with linespoints, \
    "data/ab-server-perf.txt" index 2 every 3::0 using 1:9 title "nodejs-express-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 3 every 3::0 using 1:9 title "nodejs-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 4 every 3::0 using 1:9 title "ktor-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 5 every 3::0 using 1:9 title "micronaut-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 6 every 3::0 using 1:9 title "ratpack-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 7 every 3::0 using 1:9 title "vertx-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 8 every 3::0 using 1:9 title "phoenix-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 9 every 3::0 using 1:9 title "trot-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 10 every 3::0 using 1:9 title "flask+uwsgi-python3" with linespoints, \
    "data/ab-server-perf.txt" index 11 every 3::0 using 1:9 title "tornado-python3" with linespoints, \
    "data/ab-server-perf.txt" index 12 every 3::0 using 1:9 title "cowboy-erlang" with linespoints

set output "images/ab-server-6MBps-median.png"
set key on bottom right horizontal
set xlabel "Number of concurrent requests per client node"
set ylabel "Median requests per second as observed on server-side" offset 2
plot "data/ab-server-perf.txt" index 0 every 3::1 using 1:9 title "actix-rust" with linespoints, \
    "data/ab-server-perf.txt" index 1 every 3::1 using 1:9 title "go" with linespoints, \
    "data/ab-server-perf.txt" index 2 every 3::1 using 1:9 title "nodejs-express-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 3 every 3::1 using 1:9 title "nodejs-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 4 every 3::1 using 1:9 title "ktor-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 5 every 3::1 using 1:9 title "micronaut-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 6 every 3::1 using 1:9 title "ratpack-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 7 every 3::1 using 1:9 title "vertx-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 8 every 3::1 using 1:9 title "phoenix-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 9 every 3::1 using 1:9 title "trot-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 10 every 3::1 using 1:9 title "flask+uwsgi-python3" with linespoints, \
    "data/ab-server-perf.txt" index 11 every 3::1 using 1:9 title "tornado-python3" with linespoints, \
    "data/ab-server-perf.txt" index 12 every 3::1 using 1:9 title "cowboy-erlang" with linespoints

set output "images/ab-server-10MBps-median.png"
set key on bottom right horizontal
set xlabel "Number of concurrent requests per client node"
set ylabel "Median requests per second as observed on server-side" offset 2
plot "data/ab-server-perf.txt" index 0 every 3::2 using 1:9 title "actix-rust" with linespoints, \
    "data/ab-server-perf.txt" index 1 every 3::2 using 1:9 title "go" with linespoints, \
    "data/ab-server-perf.txt" index 2 every 3::2 using 1:9 title "nodejs-express-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 3 every 3::2 using 1:9 title "nodejs-javascript" with linespoints, \
    "data/ab-server-perf.txt" index 4 every 3::2 using 1:9 title "ktor-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 5 every 3::2 using 1:9 title "micronaut-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 6 every 3::2 using 1:9 title "ratpack-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 7 every 3::2 using 1:9 title "vertx-kotlin" with linespoints, \
    "data/ab-server-perf.txt" index 8 every 3::2 using 1:9 title "phoenix-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 9 every 3::2 using 1:9 title "trot-elixir" with linespoints, \
    "data/ab-server-perf.txt" index 10 every 3::2 using 1:9 title "flask+uwsgi-python3" with linespoints, \
    "data/ab-server-perf.txt" index 11 every 3::2 using 1:9 title "tornado-python3" with linespoints, \
    "data/ab-server-perf.txt" index 12 every 3::2 using 1:9 title "cowboy-erlang" with linespoints
