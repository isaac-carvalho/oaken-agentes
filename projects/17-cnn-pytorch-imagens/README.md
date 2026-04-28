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

# treino real (baixa CIFAR-10 ~170MB + pesos ResNet18 ~45MB)
python train.py --epochs 3 --batch 128

# smoke test offline (dataset sintético + sem pesos pré-treinados)
python train.py --no-download --no-pretrained --epochs 1

# inferência
python predict.py samples/cao.jpg
```

## Output de exemplo

Smoke test ponta a ponta (treino sintético sem internet + inferência):

```bash
$ python train.py --no-download --no-pretrained --epochs 1 --batch 64
[modo] dataset SINTÉTICO (smoke test)
epoch 1 loss=2.4551 val_acc=0.094
Modelo salvo em out/model.pt

$ python predict.py /tmp/test.png
  truck        0.222
  horse        0.216
  deer         0.193
```

A acurácia 9.4% é esperada (random no sintético = 10% para 10 classes), mas o **pipeline opera ponta a ponta**: treino → save TorchScript (45MB) → load → inferência com top-3.

Em uso real (CIFAR-10 + ResNet18 transfer), val_acc passa de 70% em 3 epochs num laptop.

## Entregáveis para portfólio
- Pipeline DL completo: treino → validação → export
- Curvas de loss/accuracy salvas em `out/`
- Modelo TorchScript portátil
