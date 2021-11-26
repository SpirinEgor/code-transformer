import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    java
    application
    id("com.github.johnrengelman.shadow") version "7.0.0"
}

repositories {
    mavenLocal()
    maven {
        url = uri("https://repo.maven.apache.org/maven2/")
    }
}

dependencies {
    implementation("com.github.javaparser:javaparser-core:3.0.0-alpha.4")
    implementation("args4j:args4j:2.33")
    implementation("com.google.code.gson:gson:2.8.6")
}

group = "java-method-extractor"
version = "1.0.0-SNAPSHOT"
description = "Java method extractor to collect all methods over the corpus with Java source files."
java.sourceCompatibility = JavaVersion.VERSION_1_8

tasks.withType<JavaCompile>() {
    options.encoding = "UTF-8"
}

application {
    mainClass.set("JavaMethodExtractor")
}

tasks.withType<ShadowJar> {
    archiveFileName.set("${project.name}.jar")
}

