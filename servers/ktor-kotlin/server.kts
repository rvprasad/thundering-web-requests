// kscript server.kts

@file:CompilerOpts("-jvm-target 1.8")
@file:DependsOn("io.ktor:ktor-server-netty:1.2.2")
@file:DependsOn("com.google.code.gson:gson:2.8.5")
@file:DependsOn("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.3.40")
@file:KotlinOpts("-J-Xmx1024M")

import com.google.gson.Gson
import io.ktor.application.call
import io.ktor.http.ContentType
import io.ktor.response.respondText
import io.ktor.routing.get
import io.ktor.routing.routing
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import java.util.Random

val host = "0.0.0.0"
val port = 1234
embeddedServer(Netty, port, host) {
  routing {
    get("/random") {
      val start = System.nanoTime()
      val num = call.request.queryParameters["num"]?.toInt() ?: 10
      val randoms =  Random().ints(num.toLong(), 0, 1000000)
        .mapToObj { "%1$06d".format(it) }.toArray()
      val gson = Gson()
      call.respondText(gson.toJson(randoms), ContentType.Text.Plain)
      val duration = System.nanoTime() - start
      println("%5.3fms".format(duration / 1e6))
    }
  }
}.start()

println("Serving at $host:$port")
