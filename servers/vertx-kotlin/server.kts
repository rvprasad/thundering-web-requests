// kscript server.kts

@file:CompilerOpts("-jvm-target 1.8")
@file:DependsOn("io.vertx:vertx-web:3.7.0")
@file:DependsOn("com.google.code.gson:gson:2.8.5")
@file:DependsOn("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.3.31")
@file:KotlinOpts("-J-Xmx1024M")

import com.google.gson.Gson
import io.vertx.core.Vertx
import io.vertx.core.http.HttpServerOptions
import io.vertx.ext.web.Router
import java.net.InetAddress
import java.util.Random

val host = "0.0.0.0"
val port = 1234
val vertx = Vertx.vertx()
val server = vertx.createHttpServer(HttpServerOptions().setHost(host))
val router = Router.router(vertx)

router.get("/random").handler { ctx ->
  val start = System.nanoTime()
  val num = ctx.request().params().get("num")?.toInt() ?: 10
  val randoms =  Random().ints(num.toLong(), 0, 1000000)
    .mapToObj { "%1$06d".format(it) }.toArray()
  ctx.response().end(Gson().toJson(randoms))
  val duration = System.nanoTime() - start
  println("%5.3fms".format(duration / 1e6))
}

server.requestHandler(router).listen(port)
println("Serving at $host:$port")
