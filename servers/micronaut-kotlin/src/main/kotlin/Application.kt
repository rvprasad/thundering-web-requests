package micronaut.kotlin

import com.google.gson.Gson
import io.micronaut.runtime.Micronaut
import io.micronaut.http.annotation.Controller
import io.micronaut.http.annotation.Get
import io.micronaut.validation.Validated
import java.util.Random

@Controller("/")
@Validated
class Application {

  @Get("/random{?num}")
  fun random(num: String?): String {
    val start = System.nanoTime()
    val tmp1 = num?.toIntOrNull() ?: 10
    val randoms = Random().ints(tmp1.toLong(), 0, 1000000)
      .mapToObj { "%1$06d".format(it) }.toArray()
    val ret = Gson().toJson(randoms)
    val duration = System.nanoTime() - start
    println("%5.3fms".format(duration / 1e6))
    return ret
  }

  companion object {

    @JvmStatic
    fun main(args: Array<String>) {
        Micronaut.build()
                .packages("micronaut.kotlin")
                .mainClass(Application::class.java)
                .start()
    }
  }
}
