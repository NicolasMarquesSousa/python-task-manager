"""Gerenciador de tarefas com persistência local em JSON."""

import json
from pathlib import Path


class GerenciadorTarefas:
    def __init__(self, arquivo: Path) -> None:
        self.arquivo = arquivo
        self.tarefas = self._carregar()

    def _carregar(self) -> list[dict]:
        if not self.arquivo.exists():
            return []
        try:
            return json.loads(self.arquivo.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def _salvar(self) -> None:
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        self.arquivo.write_text(
            json.dumps(self.tarefas, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def adicionar(self, descricao: str) -> dict:
        descricao = descricao.strip()
        if not descricao:
            raise ValueError("A descrição não pode ficar vazia.")

        tarefa = {
            "id": max((item["id"] for item in self.tarefas), default=0) + 1,
            "descricao": descricao,
            "concluida": False,
        }
        self.tarefas.append(tarefa)
        self._salvar()
        return tarefa

    def listar(self) -> list[dict]:
        return list(self.tarefas)

    def concluir(self, tarefa_id: int) -> bool:
        for tarefa in self.tarefas:
            if tarefa["id"] == tarefa_id:
                tarefa["concluida"] = True
                self._salvar()
                return True
        return False

    def remover(self, tarefa_id: int) -> bool:
        quantidade_anterior = len(self.tarefas)
        self.tarefas = [tarefa for tarefa in self.tarefas if tarefa["id"] != tarefa_id]
        if len(self.tarefas) == quantidade_anterior:
            return False
        self._salvar()
        return True


def exibir_tarefas(gerenciador: GerenciadorTarefas) -> None:
    tarefas = gerenciador.listar()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for tarefa in tarefas:
        estado = "x" if tarefa["concluida"] else " "
        print(f"{tarefa['id']:>3} [{estado}] {tarefa['descricao']}")


def ler_id() -> int | None:
    try:
        return int(input("ID da tarefa: "))
    except ValueError:
        print("Digite um número inteiro.")
        return None


def main() -> None:
    gerenciador = GerenciadorTarefas(Path(__file__).with_name("tarefas.json"))
    opcoes = {
        "1": "Listar tarefas",
        "2": "Adicionar tarefa",
        "3": "Concluir tarefa",
        "4": "Remover tarefa",
        "0": "Sair",
    }

    while True:
        print("\nGerenciador de tarefas")
        for codigo, descricao in opcoes.items():
            print(f"{codigo} - {descricao}")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print("Até mais!")
            break
        if escolha == "1":
            exibir_tarefas(gerenciador)
        elif escolha == "2":
            try:
                tarefa = gerenciador.adicionar(input("Descrição: "))
                print(f"Tarefa {tarefa['id']} adicionada.")
            except ValueError as erro:
                print(erro)
        elif escolha in {"3", "4"}:
            tarefa_id = ler_id()
            if tarefa_id is None:
                continue
            sucesso = (
                gerenciador.concluir(tarefa_id)
                if escolha == "3"
                else gerenciador.remover(tarefa_id)
            )
            print("Operação concluída." if sucesso else "Tarefa não encontrada.")
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
