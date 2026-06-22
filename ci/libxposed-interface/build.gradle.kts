plugins {
    id("com.android.library") version "8.2.1"
    id("maven-publish")
}

android {
    compileSdk = 34
    namespace = "io.github.libxposed.service"
    defaultConfig {
        minSdk = 27
    }
}

afterEvaluate {
    publishing {
        publications {
            create<MavenPublication>("release") {
                from(components["release"])
                groupId = "io.github.libxposed"
                artifactId = "interface"
                version = "100"
            }
        }
    }
}
