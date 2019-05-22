const http = require('http')
const url = require('url')

const hostname = '0.0.0.0'
const port = 1234

function getRandomNumbers (num) {
  const ret = []
  for (let i = 0; i < num; i = i + 1) {
    ret.push(Math.floor(Math.random() * 1e6))
  }
  return ret
}

var reqCount = 0

function getReqCount () {
  reqCount = reqCount + 1
  return reqCount
}

const server = http.createServer((req, res) => {
  const reqId = getReqCount()
  console.time(reqId)

  const parsedURL = url.parse(req.url, true)
  if (req.method === 'GET' && parsedURL.pathname === '/random') {
    const params = parsedURL.query
    const num = params.num ? params.num : 10
    const buf = JSON.stringify(getRandomNumbers(num))
    res.statusCode = 200
    res.setHeader('Content-Type', 'text/plain')
    res.setHeader('Content-Length', Buffer.byteLength(buf))
    res.end(buf)
  } else {
    res.statusCode = 501
    res.end()
  }

  console.timeEnd(reqId)
})

server.listen(port, hostname)
console.log(`Server running at http://${hostname}:${port}/`)
