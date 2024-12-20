FROM openjdk:17-alpine

WORKDIR /app

COPY calc.java .

RUN javac calc.java

CMD ["java", "calc"]