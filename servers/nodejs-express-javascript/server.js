const http = require('http')
const express = require('express')

const hostname = '0.0.0.0'
const port = 1234

function getRandomNumbers(num) {
  const ret = []
  for (let i = 0; i < num; i = i + 1) {
    ret.push(Math.floor(Math.random() * 999999).toString().padStart(6, 0))
  }
  return ret
}

var reqCount = 0
const app = express()

app.get('/random', (req, res) => {
  const reqId = ++reqCount
  console.time(reqId)
  const num = req.query.num ? req.query.num : 10
  const buf = JSON.stringify(getRandomNumbers(num))
  res.type('text/plain')
  res.end(buf)
  console.timeEnd(reqId)
})

http.createServer(app).listen(port, hostname)
console.log(`Server running at http://${hostname}:${port}/`)
