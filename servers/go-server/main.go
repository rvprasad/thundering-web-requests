package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"time"
)

func randomHandler(writer http.ResponseWriter, req *http.Request) {
	start := time.Now()
	num := 10
	req.ParseForm()
	if tmp1, exists := req.Form["num"]; exists {
		if tmp2, err := strconv.Atoi(tmp1[0]); err == nil {
			num = tmp2
		}
	}
	nums := make([]string, num)
	for i := 0; i < num; i++ {
		nums[i] = fmt.Sprintf("\"%06d\"", rand.Int()%1000000)
	}
	fmt.Fprintf(writer, "[%s]", strings.Join(nums, ","))
	elapsedTime := time.Now().Sub(start)

	fmt.Printf("%.3fms\n", float32(elapsedTime.Nanoseconds())/1e6)
}

func main() {
	http.HandleFunc("/random", randomHandler)
	fmt.Printf("Serving at 0.0.0.0:1234")
	log.Fatal(http.ListenAndServe("0.0.0.0:1234", nil))
}
