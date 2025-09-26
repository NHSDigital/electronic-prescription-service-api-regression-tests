FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install dependencies
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

USER vscode

# Install ASDF properly via Git clone
RUN git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.16.4

# Set up ASDF environment variables and PATH
ENV ASDF_DIR=/home/vscode/.asdf
ENV PATH="/home/vscode/.asdf/bin:/home/vscode/.asdf/shims:$PATH"

# Set up shell integration
RUN echo 'export ASDF_DIR="$HOME/.asdf"' >> ~/.bashrc && \
    echo 'export PATH="$ASDF_DIR/bin:$ASDF_DIR/shims:$PATH"' >> ~/.bashrc && \
    echo '. "$ASDF_DIR/asdf.sh"' >> ~/.bashrc && \
    echo '. "$ASDF_DIR/completions/asdf.bash"' >> ~/.bashrc

# Install ASDF plugins (with proper environment setup)
RUN export ASDF_DIR=/home/vscode/.asdf && \
    . $ASDF_DIR/asdf.sh && \
    asdf plugin add python && \
    asdf plugin add poetry https://github.com/asdf-community/asdf-poetry.git && \
    asdf plugin add shellcheck https://github.com/luizm/asdf-shellcheck.git && \
    asdf plugin add nodejs && \
    asdf plugin add actionlint && \
    asdf plugin add allure

WORKDIR /workspaces/electronic-prescription-service-api-regression-tests
COPY .tool-versions /workspaces/electronic-prescription-service-api-regression-tests/.tool-versions
COPY .tool-versions /home/vscode/.tool-versions

# Install tools specified in .tool-versions (with proper environment setup)
RUN export ASDF_DIR=/home/vscode/.asdf && \
    . $ASDF_DIR/asdf.sh && \
    asdf install && \
    asdf reshim python && \
    asdf reshim poetry && \
    asdf reshim nodejs
