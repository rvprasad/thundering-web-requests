package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime/pprof"
	"strconv"
	"time"
)

func main() {
	f, err := os.Create("cpuprofile")
	if err != nil {
		log.Fatal(err)
	}
	pprof.StartCPUProfile(f)
	defer pprof.StopCPUProfile()

	url := os.Args[1]
	num := 10
	if len(os.Args) > 2 {
		tmp1, err := strconv.Atoi(os.Args[2])
		if err == nil {
			num = tmp1
		}
	}

	results := make(chan string)
	for i := 0; i < num; i++ {
		go func(url string) {
			start := time.Now()
			_, err := http.Get(url)
			elapsedTime := time.Now().Sub(start)

			verdict := "OK"
			if err != nil {
				fmt.Println(err)
				verdict = "ERR"
			}

			results <- verdict
			fmt.Printf("%.3fms %s\n", float32(elapsedTime.Nanoseconds())/1e6,
				verdict)

		}(url)
	}

	numSucc := 0
	numFail := 0
	for num > 0 {
		verdict := <-results
		if verdict == "OK" {
			numSucc++
		} else {
			numFail++
		}
		num--
	}

	fmt.Printf("Success: %d\n", numSucc)
	fmt.Printf("Failure: %d\n", numFail)
}
