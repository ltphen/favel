# FROM adoptopenjdk/openjdk11:jre-11.0.6_10-alpine
# RUN apk add --no-cache curl tar bash procps
# RUN apk update && apk add git && apk add maven
# RUN git clone "https://github.com/ltphen/COPAAL"


# FROM maven:3.6.0-jdk-11-slim AS maven
# RUN mkdir copaal
# COPY --from=alpine . /copaal
# WORKDIR /copaal/COPAAL/service
# RUN mvn clean install
# EXPOSE 3333
# ENTRYPOINT ["java","-jar","/copaal/COPAAL/service/target/corraborative-2.2.2.jar"]


FROM adoptopenjdk/openjdk11:jre-11.0.6_10-alpine
VOLUME /tmp
ARG JAR_FILE
COPY *.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app.jar"]
