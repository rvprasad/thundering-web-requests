package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"
)

func makeRequest(url string, results chan string) {
	start := time.Now()
	verdict := "OK"
	if _, err := http.Get(url); err != nil {
		fmt.Println(err)
		verdict = "ERR"
	}
	elapsedTime := time.Now().Sub(start)

	results <- verdict
	fmt.Printf("%.3fms %s\n", float32(elapsedTime.Nanoseconds())/1e6,
		verdict)
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

func main() {
	url := os.Args[1]
	num := getNum(os.Args)

	results := make(chan string)
	for i := 0; i < num; i++ {
		go makeRequest(url, results)
	}

	numSucc, numFail := 0, 0
	for num > 0 {
		if <-results == "OK" {
			numSucc++
		} else {
			numFail++
		}
		num--
	}

	fmt.Printf("Success: %d\n", numSucc)
	fmt.Printf("Failure: %d\n", numFail)
}
