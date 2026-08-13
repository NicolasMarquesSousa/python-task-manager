import tempfile
import unittest
from pathlib import Path

from gerenciador import GerenciadorTarefas


class GerenciadorTarefasTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "tarefas.json"
        self.gerenciador = GerenciadorTarefas(self.arquivo)

    def tearDown(self) -> None:
        self.pasta.cleanup()

    def test_adiciona_e_persiste_tarefa(self) -> None:
        tarefa = self.gerenciador.adicionar("Estudar Python")
        recarregado = GerenciadorTarefas(self.arquivo)

        self.assertEqual(tarefa["id"], 1)
        self.assertEqual(recarregado.listar(), [tarefa])

    def test_conclui_tarefa(self) -> None:
        tarefa = self.gerenciador.adicionar("Praticar funções")

        self.assertTrue(self.gerenciador.concluir(tarefa["id"]))
        self.assertTrue(self.gerenciador.listar()[0]["concluida"])

    def test_remove_tarefa(self) -> None:
        tarefa = self.gerenciador.adicionar("Revisar exercícios")

        self.assertTrue(self.gerenciador.remover(tarefa["id"]))
        self.assertEqual(self.gerenciador.listar(), [])

    def test_rejeita_descricao_vazia(self) -> None:
        with self.assertRaises(ValueError):
            self.gerenciador.adicionar("   ")


if __name__ == "__main__":
    unittest.main()
