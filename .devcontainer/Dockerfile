FROM ubuntu:22.04

# Create vscode user with sudo capabilities
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode \
    && apt-get update \
    && apt-get install -y sudo \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# provide DOCKER_GID via build args if you need to force group id to match host
ARG DOCKER_GID
ARG TARGETARCH
ENV TARGETARCH=${TARGETARCH}

ARG ASDF_VERSION
COPY .tool-versions.asdf /tmp/.tool-versions.asdf

RUN if [ "$TARGETARCH" = "arm64" ] || [ "$TARGETARCH" = "aarch64" ]; then dpkg --add-architecture arm64; fi

# Anticipate and resolve potential permission issues with apt
RUN mkdir -p /tmp && chmod 1777 /tmp

# Install system dependencies
RUN apt-get update \
  && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y dist-upgrade \
  && apt-get -y install --no-install-recommends htop vim curl git build-essential \
  libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev libbz2-dev \
  zlib1g-dev unixodbc unixodbc-dev libsecret-1-0 libsecret-1-dev libsqlite3-dev \
  openjdk-8-jdk jq apt-transport-https ca-certificates gnupg-agent \
  software-properties-common bash-completion python3-pip make \
  libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev liblzma-dev netcat-traditional libyaml-dev unzip

# Install ASDF
RUN ASDF_VERSION=$(awk '!/^#/ && NF {print $1; exit}' /tmp/.tool-versions.asdf) && \
  if [ "$TARGETARCH" = "arm64" ] || [ "$TARGETARCH" == "aarch64" ]; then \
  wget -O /tmp/asdf.tar.gz "https://github.com/asdf-vm/asdf/releases/download/v${ASDF_VERSION}/asdf-v${ASDF_VERSION}-linux-arm64.tar.gz"; \
  else \
  wget -O /tmp/asdf.tar.gz "https://github.com/asdf-vm/asdf/releases/download/v${ASDF_VERSION}/asdf-v${ASDF_VERSION}-linux-amd64.tar.gz"; \
  fi && \
  tar -xzf /tmp/asdf.tar.gz -C /tmp && \
  mkdir -p /usr/bin && \
  mv /tmp/asdf /usr/bin/asdf && \
  chmod +x /usr/bin/asdf && \
  rm -rf /tmp/asdf.tar.gz 

# specify DOCKER_GID to force container docker group id to match host
RUN if [ -n "${DOCKER_GID}" ]; then \
  if ! getent group docker; then \
  groupadd -g ${DOCKER_GID} docker; \
  else \
  groupmod -g ${DOCKER_GID} docker; \
  fi && \
  usermod -aG docker vscode; \
  fi

USER vscode

ENV PATH="/home/vscode/.asdf/shims/:$PATH"
RUN \
  echo 'PATH="/home/vscode/.asdf/shims/:$PATH"' >> ~/.bashrc; \
  echo '. <(asdf completion bash)' >> ~/.bashrc;

ENV PATH="$PATH:/workspaces/electronic-prescription-service-api-regression-tests/node_modules/.bin"

# Install ASDF plugins for regression testing tools
RUN asdf plugin add python && \
  asdf plugin add poetry https://github.com/asdf-community/asdf-poetry.git && \
  asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git && \
  asdf plugin add shellcheck https://github.com/luizm/asdf-shellcheck.git && \
  asdf plugin add actionlint && \
  asdf plugin add allure

WORKDIR /workspaces/electronic-prescription-service-api-regression-tests
ADD .tool-versions /workspaces/electronic-prescription-service-api-regression-tests/.tool-versions
ADD .tool-versions /home/vscode/.tool-versions

# install python before poetry to ensure correct python version is used
RUN asdf install python && \
  asdf install && \
  asdf reshim python && \
  asdf reshim poetry && \
  asdf reshim nodejs
