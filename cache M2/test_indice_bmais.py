import os
import random
import tempfile
import unittest

from cache import Cache
from indice_bmais import ArvoreBMais
from pager_indice import PagerIndice


class PagerMonitorado(PagerIndice):
    def __init__(self, caminho):
        super().__init__(caminho)
        self.leituras = []

    def le(self, page_id):
        self.leituras.append(page_id)
        return super().le(page_id)


class TestIndiceBMais(unittest.TestCase):
    def verificar_estrutura(self, arvore, esperado):
        folhas, niveis = [], set()

        def visitar(page_id, nivel, raiz=False):
            no = arvore._carregar_no(page_id)
            self.assertEqual(no.chaves, sorted(set(no.chaves)))
            self.assertLess(len(no.chaves), arvore.ordem)
            if no.folha:
                folhas.append(no)
                niveis.add(nivel)
                self.assertEqual(len(no.referencias), len(no.chaves))
                if not raiz:
                    self.assertGreaterEqual(len(no.chaves), arvore.ordem // 2)
                return no.chaves
            self.assertEqual(no.referencias, [])
            self.assertEqual(len(no.filhos), len(no.chaves) + 1)
            self.assertGreaterEqual(len(no.filhos), 2 if raiz else (arvore.ordem + 1) // 2)
            grupos = [visitar(filho, nivel + 1) for filho in no.filhos]
            self.assertEqual(no.chaves, [grupo[0] for grupo in grupos[1:]])
            for esquerda, direita in zip(grupos, grupos[1:]):
                self.assertLess(esquerda[-1], direita[0])
            return [chave for grupo in grupos for chave in grupo]

        self.assertEqual(visitar(arvore.raiz, 0, True), sorted(esperado))
        self.assertEqual(len(niveis), 1)
        for i, folha in enumerate(folhas):
            seguinte = folhas[i + 1].page_id if i + 1 < len(folhas) else 0
            self.assertEqual(folha.proxima, seguinte)
        for chave, referencia in esperado.items():
            self.assertEqual(arvore.buscar(chave), referencia)
        self.assertTrue(all(n == 0 for n in arvore.cache.fixada.values()))

    def test_divisoes_e_persistencia(self):
        with tempfile.TemporaryDirectory() as pasta:
            for ordem in (3, 4, 5, 8, None):
                for sequencia in (list(range(400)), list(reversed(range(400))),
                                  random.Random(42).sample(range(400), 400)):
                    with self.subTest(ordem=ordem, primeira=sequencia[0]):
                        caminho = os.path.join(pasta, 'indice.db')
                        pager = PagerIndice(caminho)
                        try:
                            arvore = ArvoreBMais(Cache(pager, 1), ordem)
                            esperado = {}
                            for chave in sequencia:
                                referencia = (chave // 20, chave % 20)
                                arvore.inserir(chave, *referencia)
                                esperado[chave] = referencia
                            quantidade = arvore.proxima_pagina
                            arvore.inserir(100, 999, 2)
                            esperado[100] = (999, 2)
                            self.assertEqual(arvore.proxima_pagina, quantidade)
                            for chave in (-(1 << 63), (1 << 63) - 1):
                                arvore.inserir(chave, 0, 0)
                                esperado[chave] = (0, 0)
                            self.verificar_estrutura(arvore, esperado)
                            self.assertIsNone(arvore.buscar(500))
                            arvore.descarrega()
                        finally:
                            pager.fecha()
                        pager = PagerIndice(caminho)
                        try:
                            arvore = ArvoreBMais(Cache(pager, 2))
                            self.verificar_estrutura(arvore, esperado)
                            arvore.inserir(500, 30, 1)
                            esperado[500] = (30, 1)
                            self.verificar_estrutura(arvore, esperado)
                            arvore.descarrega()
                        finally:
                            pager.fecha()
                        os.remove(caminho)

    def test_busca_sem_varrer_tabela(self):
        with tempfile.TemporaryDirectory() as pasta:
            dados = PagerMonitorado(os.path.join(pasta, 'dados.db'))
            indice = PagerIndice(os.path.join(pasta, 'indice.db'))
            try:
                # 50 páginas de tabela. Só a página 25 deve ser lida na busca.
                for page_id in range(50):
                    dados.escreve(page_id, bytes(4096))
                dados.escreve_registro_unico(25, 1, 'Ana')
                dados.sync()
                arvore = ArvoreBMais(Cache(indice, 1), 4)
                arvore.inserir(20, 25, 1)
                arvore.inserir(30, 25, 2)
                cache_dados = Cache(dados, 2)
                self.assertEqual(arvore.buscar_registro(20, cache_dados), b'Ana\x00\x00\x00\x00\x00')
                self.assertEqual(dados.leituras, [25])
                self.assertIsNone(arvore.buscar_registro(99, cache_dados))
                self.assertEqual(dados.leituras, [25])
                self.assertEqual(arvore.buscar_registro(30, cache_dados), bytes(8))
                self.assertEqual(dados.leituras, [25])  # Segunda busca usa o cache.
                arvore.inserir(40, 25, 510)  # Slots válidos: 0 a 509.
                with self.assertRaises(ValueError):
                    arvore.buscar_registro(40, cache_dados)
                arvore.inserir(50, 100, 0)
                with self.assertRaises(ValueError):
                    arvore.buscar_registro(50, cache_dados)
                self.assertTrue(all(n == 0 for n in cache_dados.fixada.values()))
                arvore.descarrega()
            finally:
                dados.fecha()
                indice.fecha()

    def test_validacao_e_arquivo_existente(self):
        with tempfile.TemporaryDirectory() as pasta:
            pager = PagerIndice(os.path.join(pasta, 'indice.db'))
            try:
                cache = Cache(pager, 2)
                arvore = ArvoreBMais(cache, 4)
                self.assertIsNone(arvore.buscar(0))
                for chave, pagina, slot in [(True, 0, 0), ('abc', 0, 0),
                                            (1 << 63, 0, 0), (1, -1, 0),
                                            (1, 0, -1), (1, 0, 1 << 64)]:
                    with self.assertRaises(ValueError):
                        arvore.inserir(chave, pagina, slot)
                for ordem in (2, True, arvore.max_ordem + 1, 5):
                    with self.assertRaises(ValueError):
                        ArvoreBMais(cache, ordem)
                arvore.descarrega()
                pager.escreve(10, b'\xff\x00ABC')
                self.assertEqual(pager.le(10), b'\xff\x00ABC' + bytes(4091))
                with self.assertRaises(ValueError):
                    pager.escreve(10, bytes(4097))
            finally:
                pager.fecha()
            pager = PagerIndice(os.path.join(pasta, 'outro.db'))
            try:
                pager.escreve(0, b'DADOS EXISTENTES')
                with self.assertRaises(ValueError):
                    ArvoreBMais(Cache(pager, 1))
                self.assertTrue(pager.le(0).startswith(b'DADOS EXISTENTES'))
            finally:
                pager.fecha()


if __name__ == '__main__':
    unittest.main()
