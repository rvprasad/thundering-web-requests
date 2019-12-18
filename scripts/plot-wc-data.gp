set datafile missing "NA"
set datafile separator ","
set ylabel font ",14"
set xlabel font ",14"
set grid x
set grid y

set terminal png size 600,600 fontscale 1.1

set ylabel "Minimum time per request as observed on client-side (ms)"
set xlabel "Number of concurrent requests per client"

set output "images/wc-actix-rust-2MBps.png"
plot "data/wc-data.csv" index 0 every 3::0 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 1 every 3::0 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 2 every 3::0 using 3:11 title "vertx-kolin-client" with linespoints

set output "images/wc-actix-rust-6MBps.png"
plot "data/wc-data.csv" index 0 every 3::1 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 1 every 3::1 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 2 every 3::1 using 3:11 title "vertx-kolin-client" with linespoints

set output "images/wc-actix-rust-10MBps.png"
plot "data/wc-data.csv" index 0 every 3::2 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 1 every 3::2 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 2 every 3::2 using 3:11 title "vertx-kolin-client" with linespoints

set output "images/wc-go-server-2MBps.png"
plot "data/wc-data.csv" index 3 every 3::0 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 4 every 3::0 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 5 every 3::0 using 3:11 title "vertx-kolin-client" with linespoints

set output "images/wc-go-server-6MBps.png"
plot "data/wc-data.csv" index 3 every 3::1 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 4 every 3::1 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 5 every 3::1 using 3:11 title "vertx-kolin-client" with linespoints

set output "images/wc-go-server-10MBps.png"
plot "data/wc-data.csv" index 3 every 3::2 using 3:11 title "go-client" with linespoints, \
    "data/wc-data.csv" index 4 every 3::2 using 3:11 title "httpoison-elixir-client" with linespoints, \
    "data/wc-data.csv" index 5 every 3::2 using 3:11 title "vertx-kolin-client" with linespoints
