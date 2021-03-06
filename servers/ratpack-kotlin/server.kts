// kscript server.kts

@file:CompilerOpts("-jvm-target 1.8")
@file:DependsOn("io.ratpack:ratpack-core:1.6.1")
@file:DependsOn("com.google.code.gson:gson:2.8.5")
@file:DependsOn("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.3.40")
@file:KotlinOpts("-J-Xmx1024M")

import com.google.gson.Gson
import ratpack.exec.Blocking
import ratpack.server.RatpackServer
import ratpack.server.ServerConfig
import java.net.InetAddress
import java.util.Random

val host = "0.0.0.0"
val port = 1234
RatpackServer.start { serverSpec ->
  val configBuilder = ServerConfig.embedded()
    .port(1234)
    .address(InetAddress.getByName(host))
  serverSpec.serverConfig(configBuilder)
    .handlers { chain ->
      chain.get("random") { ctx ->
        Blocking.get { ->
          val start = System.nanoTime()
          val num = ctx.getRequest().getQueryParams().get("num")?.toInt() ?: 10
          val randoms =  Random().ints(num.toLong(), 0, 1000000)
            .mapToObj { "%1$06d".format(it) }.toArray()
          val ret = Gson().toJson(randoms)
          val duration = System.nanoTime() - start
          println("%5.3fms".format(duration / 1e6))
          ret
        } .then { x -> ctx.render(x) }
      }
    }
}

println("Serving at $host:$port")
