// kscript client.kts 127.0.0.1 1234 /random?num=10 100

@file:CompilerOpts("-jvm-target 1.8")
@file:DependsOn("io.vertx:vertx-web-client:3.7.1")
@file:DependsOn("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.3.40")
@file:KotlinOpts("-J-Xmx1024M")

import io.vertx.core.Vertx
import io.vertx.core.buffer.Buffer
import io.vertx.ext.web.client.HttpRequest
import io.vertx.ext.web.client.WebClient
import java.util.concurrent.CountDownLatch
import java.util.concurrent.atomic.AtomicInteger

val url = args[0]
val nums = args[1].toInt()
val client = WebClient.create(Vertx.vertx())
val succs = AtomicInteger()
val fails = AtomicInteger()
val latch = CountDownLatch(nums)
(1..nums).asIterable().toList().parallelStream().forEach { x ->
  val start = System.nanoTime()
  client.getAbs(url).send { ar ->
    val duration: Long = System.nanoTime() - start
    var verdict = "OK"
    if (ar.succeeded()) {
      succs.incrementAndGet()
    } else {
      verdict = "ERR"
      fails.incrementAndGet()
    }
    println("%5.3fms %s".format(duration / 1e6, verdict))
    latch.countDown()
  }
}

latch.await()
println("Success: ${succs.get()}")
println("Failure: ${fails.get()}")
System.exit(0)
