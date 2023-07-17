ARG BUILDER_IMAGE=debian:bullseye
ARG BASE_IMAGE=node:18.13.0-bullseye
FROM $BUILDER_IMAGE AS ripes-builder

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -q \
    && apt-get install -qy --no-install-recommends \
    build-essential \
    cmake \
    gcc-riscv64-unknown-elf \
    git \
    libpthread-stubs0-dev \
    libqt5charts5-dev \
    libqt5svg5-dev \
    python3 \
    && apt-get -y autoremove \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

ARG GIT_SSL_NO_VERIFY=true
ENV LC_ALL=C.UTF-8 SHELL=/bin/bash

RUN git clone --recursive https://github.com/mortbopet/Ripes.git /tmp/ripes

COPY ./ripes-ecall.patch /tmp/ripes

RUN cd /tmp/ripes \
    && mkdir build-output \
    && git checkout 2a03b38ce63576698be5737eed14f809ba549a20 \
    && git submodule update \
    && git apply ripes-ecall.patch \
    && cmake -S /tmp/ripes -B /tmp/ripes/build-output -DCMAKE_BUILD_TYPE=Release . \
    && cmake --build /tmp/ripes/build-output --parallel $(nproc)

FROM $BASE_IMAGE

RUN apt-get update \
    && apt-get install -y \
        default-jre \
        libqt5charts5-dev \
        libqt5svg5-dev \
    && apt-get -y autoremove \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

ENV NODE_ENV build

USER node
WORKDIR /home/node

COPY --chown=node:node package*.json ./
RUN npm i

COPY --chown=node:node . .
RUN npm run build

ENV NODE_ENV production

WORKDIR /home/node

COPY --from=ripes-builder --chown=node:node /tmp/ripes/build-output/Ripes /home/node/lib/ripes
RUN chmod +x /home/node/lib/ripes
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-node

CMD ["node", "./dist/index.js"]
