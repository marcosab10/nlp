# Arquivo para facilitar a ativação do ambiente no Git Bash
export PATH="$(pwd)/venv/Scripts:$PATH"
alias python="$(pwd)/venv/Scripts/python.exe"
alias pip="$(pwd)/venv/Scripts/pip.exe"

# Informações do ambiente ativado
echo "Ambiente virtual Python ativado!"
echo "Python: $(python -c 'import sys; print(sys.executable)')"
