package main

import "fmt"
import "math/rand"
import "strings"
import "sort"
import "strconv"
import "time"

func worker(stats1 *float64, stats2 *float64, num int, done chan bool) {
	var writer strings.Builder
	start1 := time.Now()

	nums := make([]string, num)
	for i := 0; i < num; i++ {
		nums[i] = fmt.Sprintf("%06d", rand.Int()%1000000)
	}
	*stats1 = float64(time.Now().Sub(start1).Nanoseconds()) / 1e6

	start2 := time.Now()
	fmt.Fprintf(&writer, "%s", strings.Join(nums, ","))

	*stats2 = float64(time.Now().Sub(start2).Nanoseconds()) / 1e6
	done <- true
}

func helper1(num int, step int) (float64, float64) {
	N := step * 3
	stats1 := make([]float64, N)
	stats2 := make([]float64, N)

	for j := 0; j < 3; j++ {
		done := make(chan bool, step)
		for k := 0; k < step; k++ {
			go worker(&stats1[j*step+k], &stats2[j*step+k], num, done)
		}
		for k := 0; k < step; k++ {
			<-done
		}
	}
	sort.Float64s(stats1)
	sort.Float64s(stats2)
	i1 := N / 2
	return (stats1[i1-1] + stats1[i1]) / 2, (stats2[i1-1] + stats2[i1]) / 2
}

func helper(num int) {
	steps := []int{1, 50, 100, 200, 300, 400, 500, 600, 700, 800}
	stats := make([]string, len(steps)*2)
	for i, step := range steps {
		stats1 := make([]float64, 7)
		stats2 := make([]float64, 7)
		for j := 0; j < 7; j++ {
			tmp1, tmp2 := helper1(num, step)
			stats1[j] = tmp1
			stats2[j] = tmp2
		}
		sort.Float64s(stats1)
		sort.Float64s(stats2)
		stats[i*2] = strconv.FormatFloat(stats1[4], 'f', 3, 64)
		stats[i*2+1] = strconv.FormatFloat(stats2[4], 'f', 3, 64)
	}

	fmt.Printf("%d,%s\n", num, strings.Join(stats, ","))
}

func main() {
	nums := []int{20, 40, 60, 80, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500}
	for _, i := range nums {
		helper(i)
	}
}
