# 06 — RAG Multimodal com CLIP

> **Carreira Alura:** Especialista em IA — Nível 1 (*RAG avançado*)

Sistema RAG que aceita **texto OU imagem** como query, e busca em uma coleção mista de imagens e descrições textuais via embeddings CLIP.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Embeddings | `open-clip-torch` |
| Vector store | `chromadb` |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python ingest.py samples/
python search.py --texto "gato preto sentado"
python search.py --imagem samples/foto1.jpg
```

## Output de exemplo

Indexação + 2 queries cross-modal validadas:

```bash
$ python ingest.py samples
Indexadas 1 imagens e 2 textos.

$ python search.py --texto "tenis preto para corrida"
Query: texto 'tenis preto para corrida'
  [1.095] text  samples/exemplo1.txt  — Tênis esportivo preto com solado branco...
  [1.667] text  samples/exemplo2.txt  — Mochila preta tamanho médio...
  [1.872] image samples/imagem_azul_amarelo.png

$ python search.py --imagem samples/imagem_azul_amarelo.png
Query: imagem samples/imagem_azul_amarelo.png
  [0.000] image samples/imagem_azul_amarelo.png   ← match exato (distância 0)
  [1.796] text  samples/exemplo1.txt
  [1.859] text  samples/exemplo2.txt
```

### Backends: OpenCLIP (default) e fallback offline

Por padrão tenta carregar `open-clip ViT-B/32 laion2b_s34b_b79k` — modelo real, ~150MB, baixado do HuggingFace na primeira execução. Se houver falha de rede ou HF estiver inacessível (ex: ambientes air-gapped, sandboxes), o `ClipIndex` automaticamente cai num **`_HashBackend`** (hashing 512d sobre tokens de texto / pixels de imagem) — pior em qualidade semântica, mas garante o pipeline operacional.

> Em uso real (com internet), o modelo CLIP retorna similaridades muito mais precisas (texto "tênis" próximo de imagem de tênis, etc).

## Entregáveis para portfólio
- RAG multimodal real (não só texto)
- Indexação e busca cross-modal
- Use case: catálogo de produtos buscável por foto
