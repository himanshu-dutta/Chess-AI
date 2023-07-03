FROM --platform=arm64 ubuntu:latest

RUN apt update && apt upgrade -y
RUN apt install --no-install-recommends gcc g++ python3.10 python3-dev python3-pip openjdk-11-jre-headless -y


WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x /app/scripts/deploy.sh
CMD [ "./scripts/deploy.sh" ]
