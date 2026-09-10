"""App mínimo usado pela pipeline da aula. Sem dependências externas."""
import os


def saudacao(nome: str) -> str:
    return f"Olá, {nome}!"


def versao() -> str:
    # Na pipeline, APP_VERSION é preenchida a partir do commit (exercício 2).
    return os.environ.get("APP_VERSION", "dev")


if __name__ == "__main__":
    print(saudacao("TBX"), "versão:", versao())
