import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    java
    application
    id("com.github.johnrengelman.shadow") version "7.0.0"
}

repositories {
    maven {
        url = uri("https://repo.maven.apache.org/maven2/")
    }
}

dependencies {
    implementation("com.github.javaparser:javaparser-core-serialization:3.15.17")
    implementation("javax.json:javax.json-api:1.1")
    implementation("org.glassfish:javax.json:1.1")
    implementation("com.google.code.gson:gson:2.8.0")
}

group = "java-parser"
version = "1.0-SNAPSHOT"
description = "Java Parser wrapper for CodeTransformer preprocessing."
java.sourceCompatibility = JavaVersion.VERSION_1_8

application {
    mainClass.set("ASTParser")
}

tasks.withType<ShadowJar> {
    archiveFileName.set("${project.name}.jar")
}
