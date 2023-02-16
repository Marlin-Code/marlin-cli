#!/bin/bash
install_pyenv() {
  # Set PYENV_ROOT if not set
  if [ -z "$PYENV_ROOT" ]; then
    export PYENV_ROOT="${HOME}/.pyenv"
  fi
  # Check if pyenv is already installed
  if [ -d "${PYENV_ROOT}" ]; then
    echo "Pyenv already installed. Skipping..."
  else
    curl https://pyenv.run | bash
    exec $SHELL
  fi
  if ! command -v pyenv 1>/dev/null; then
    { echo
      echo "You have not added 'pyenv' to the load path."
      echo "Follow these instructions and rerun the install script"
      echo
    } >&2

    { # Without args, `init` commands print installation help
      "${PYENV_ROOT}/bin/pyenv" init || true
      "${PYENV_ROOT}/bin/pyenv" virtualenv-init || true
      exit 1
    } >&2
  fi
}

install_poetry() {
  if [ -d "${HOME}/Library/Application Support/pypoetry" ]; then
    echo "Poetry already installed. Skipping..."
  else
    curl -sSL https://install.python-poetry.org | python
    echo "Add 'export PATH="\$HOME/.local/bin:\$PATH"' to your shell config and restart"
  fi
}
index_main() {
    install_pyenv
    install_poetry    
}

index_main