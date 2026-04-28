# 17 — CNN PyTorch para Classificação de Imagens

> **Carreira Alura:** Engenharia de Agentes — Nível 2 (*Deep Learning*)

Treina uma CNN com **transfer learning** (ResNet18 pré-treinada na ImageNet) para classificar imagens em classes customizadas. Inclui data augmentation, early stopping e exporta o modelo em **TorchScript**.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Modelo | `torch`, `torchvision` (ResNet18) |
| Dataset | CIFAR-10 (download automático) ou pasta customizada |

## Como rodar

```bash
pip install -r requirements.txt
python train.py --epochs 3 --dataset cifar10
python predict.py samples/cao.jpg
```

## Entregáveis para portfólio
- Pipeline DL completo: treino → validação → export
- Curvas de loss/accuracy salvas em `out/`
- Modelo TorchScript portátil
