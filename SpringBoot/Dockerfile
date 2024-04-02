# Use the official Maven image to create a build artifact
# This is a multi-stage build. In the first stage, we build the application
FROM maven:3.9.6-eclipse-temurin-17-alpine as build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Use OpenJDK for running the application
FROM openjdk:17-jdk-slim
WORKDIR /app
# Copy the JAR file from the previous stage
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
