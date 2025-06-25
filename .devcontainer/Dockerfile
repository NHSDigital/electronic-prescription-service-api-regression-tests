FROM mcr.microsoft.com/devcontainers/base:ubuntu

ARG TARGETARCH
ENV TARGETARCH=${TARGETARCH}

# Add amd64 architecture if on arm64
RUN if [ "$TARGETARCH" == "arm64" ] || [ "$TARGETARCH" == "aarch64" ]; then dpkg --add-architecture amd64; fi

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y dist-upgrade \
    && apt-get -y install --no-install-recommends htop vim curl git build-essential \
    libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev libbz2-dev \
    zlib1g-dev unixodbc unixodbc-dev libsecret-1-0 libsecret-1-dev libsqlite3-dev \
    openjdk-8-jdk jq apt-transport-https ca-certificates gnupg-agent \
    software-properties-common bash-completion python3-pip make libbz2-dev \
    libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev liblzma-dev netcat-traditional

# Install ASDF
RUN if [ "$TARGETARCH" = "arm64" ] || [ "$TARGETARCH" == "aarch64" ]; then \
        wget -O /tmp/asdf.tar.gz https://github.com/asdf-vm/asdf/releases/download/v0.16.4/asdf-v0.16.4-linux-arm64.tar.gz; \
    else \
        wget -O /tmp/asdf.tar.gz https://github.com/asdf-vm/asdf/releases/download/v0.16.4/asdf-v0.16.4-linux-amd64.tar.gz; \
    fi && \
    tar -xvzf /tmp/asdf.tar.gz; \
    mv asdf /usr/bin
    
USER vscode

ENV PATH="/home/vscode/.asdf/shims/:$PATH"
RUN \
    echo 'PATH="/home/vscode/.asdf/shims/:$PATH"' >> ~/.bashrc; \
    echo '. <(asdf completion bash)' >> ~/.bashrc;

# Install ASDF plugins
RUN asdf plugin add python; \
    asdf plugin add poetry https://github.com/asdf-community/asdf-poetry.git; \
    asdf plugin add shellcheck https://github.com/luizm/asdf-shellcheck.git; \
    asdf plugin add nodejs; \
    asdf plugin add actionlint; \
    asdf plugin add allure

WORKDIR /workspaces/electronic-prescription-service-api-regression-tests
ADD .tool-versions /workspaces/electronic-prescription-service-api-regression-tests/.tool-versions
ADD .tool-versions /home/vscode/.tool-versions

RUN asdf install; \
    asdf reshim python; \
    asdf reshim poetry; \
    asdf reshim nodejs;
