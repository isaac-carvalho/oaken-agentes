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

## Entregáveis para portfólio
- RAG multimodal real (não só texto)
- Indexação e busca cross-modal
- Use case: catálogo de produtos buscável por foto
