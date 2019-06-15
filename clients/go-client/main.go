package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"
)

type Result struct {
	verdict string
	time    float32
}

func makeRequest(url string, results chan Result) {
	start := time.Now()
	result := Result{verdict: "OK", time: 0}
	if _, err := http.Get(url); err != nil {
		fmt.Println(err)
		result.verdict = "ERR"
	}
	elapsedTime := time.Now().Sub(start)

	result.time = float32(elapsedTime.Nanoseconds()) / 1e6
	results <- result
}

func getNum(args []string) int {
	num := 10
	if len(args) > 2 {
		if tmp1, err := strconv.Atoi(args[2]); err == nil {
			num = tmp1
		}
	}

	return num
}

func waitOnResults(results chan Result, completion chan bool, num int) {
	numSucc, numFail := 0, 0
	for num > 0 {
		result := <-results
		fmt.Printf("%.3fms %s\n", result.time, result.verdict)
		if result.verdict == "OK" {
			numSucc++
		} else {
			numFail++
		}
		num--
	}

	fmt.Printf("Success: %d\n", numSucc)
	fmt.Printf("Failure: %d\n", numFail)
	completion <- true
}

func main() {
	url := os.Args[1]
	num := getNum(os.Args)

	results := make(chan Result)
	completion := make(chan bool)
	go waitOnResults(results, completion, num)

	for i := 0; i < num; i++ {
		go makeRequest(url, results)
	}

	<-completion
}
