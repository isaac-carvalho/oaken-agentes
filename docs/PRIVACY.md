# Política de Privacidade — Oaken Agentes (Portfolio)

> Versão: 1.0 · Última atualização: 2026-05-02
> Este documento é um **template educacional** alinhado à LGPD (Lei 13.709/2018). Adapte antes de usar em produto real e consulte advogado especializado.

## 1. Quem é o controlador

**Responsável:** recuperarcontato4-prog (autor do portfolio)
**Contato DPO:** _a definir antes de uso comercial_
**Repositório:** https://github.com/recuperarcontato4-prog/oaken-agentes

Este portfolio reúne 21 projetos práticos de IA e agentes. **Não coleta dados pessoais de visitantes do site estático** (`index.html`). As coletas só ocorrem se você executar localmente os projetos com APIs LLM ou usar o `lgpd-compliance-toolkit` (projeto 12).

## 2. Quais dados são tratados

| Contexto | Dados | Base legal LGPD |
|---------|-------|-----------------|
| Visita ao `index.html` | Nenhum (HTML estático) | N/A |
| Execução do projeto 12 (`/anonimizar`) | Texto submetido (efêmero, não persistido) | Execução de contrato (art. 7º, V) |
| Execução do projeto 12 (`/consentimento`) | `titular`, `finalidade`, `aceito` | Consentimento (art. 7º, I) |
| Auditoria (`audit_chain.log`) | Hash SHA-256 + timestamp UTC + evento | Cumprimento de obrigação legal (art. 7º, II) |

**Dados sensíveis** (saúde, biometria, religião, opinião política): **não tratados**.

## 3. Direitos do titular (LGPD art. 18)

| Direito | Como exercer |
|---------|--------------|
| Confirmação da existência do tratamento | `GET /titular/{id}` |
| Acesso aos dados | `GET /titular/{id}/dados` |
| Correção | `POST /consentimento` (sobrescreve) |
| Anonimização / bloqueio / eliminação | `DELETE /titular/{id}` |
| Portabilidade | `GET /titular/{id}/export` (JSON) |
| Revogação do consentimento | `POST /consentimento` com `aceito: false` |

## 4. Retenção

- **Consentimentos**: indefinidamente até revogação (timestamp registrado).
- **Audit log**: append-only com hash chain; pode ser truncado após **5 anos** (limite legal mínimo para obrigações fiscais brasileiras).
- **Texto anonimizado**: não persistido (resposta efêmera).

## 5. Compartilhamento com terceiros

- **APIs LLM** (OpenAI, Anthropic, Google): chamadas só ocorrem se o usuário configurar `*_API_KEY`. Cada provedor tem sua própria política — recomendamos revisar antes de enviar dados.
- **AWS Bedrock** (projeto 11): mesmo princípio.
- **Langfuse** (projeto 20): só ativo com credenciais explícitas.

Nenhum dado é vendido. Nenhum dado é compartilhado para fins de marketing.

## 6. Segurança

Medidas implementadas no portfolio:
- `.env` nunca commitado (no `.gitignore`)
- Guardrails de PII redaction (projeto 10)
- Audit chain SHA-256 (projeto 12)
- Security headers + rate limiting nas APIs FastAPI
- IAM least privilege no Terraform (projeto 11)
- K8s `securityContext` non-root + readOnlyRootFilesystem (projeto 21)

## 7. Incidente de segurança

Em caso de incidente envolvendo dados pessoais (LGPD art. 48):
1. Notificar a ANPD em até **2 dias úteis**
2. Notificar titulares afetados
3. Registrar no audit log do toolkit (projeto 12)

Plano de resposta: definir antes de uso comercial (template em `docs/INCIDENT.md`).

## 8. Sub-processadores

Lista atualizada quando aplicável:
- OpenAI · Estados Unidos · LLM
- Anthropic · Estados Unidos · LLM
- Google (Gemini) · Estados Unidos · LLM
- AWS · multi-região · cloud (Lambda, Bedrock, S3)
- HuggingFace · Estados Unidos · modelos open-source

Transferência internacional ocorre nessas chamadas — base legal: **garantias contratuais** ou **consentimento específico** (LGPD art. 33).

## 9. Mudanças nesta política

Histórico em `git log docs/PRIVACY.md`. Atualizações relevantes serão sinalizadas no README do repositório.

## 10. Reclamações

Em caso de descumprimento, o titular pode reclamar à ANPD (https://www.gov.br/anpd).
