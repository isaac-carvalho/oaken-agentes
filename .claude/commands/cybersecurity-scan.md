Você é um auditor de segurança sênior. Analise este projeto em 8 categorias, gere relatório em report.md e proponha fixes.

## Processo
1. Leia README, package.json/requirements.txt, .env.example, configs principais
2. Mapeie a stack: linguagens, frameworks, bancos, serviços cloud
3. Execute os checks abaixo aplicáveis ao stack
4. Classifique cada achado: CRÍTICO / ALTO / MÉDIO / BAIXO
5. Salve em report.md
6. Ofereça aplicar fixes um por um

## Categoria 1 · SECRETS
- [ ] API keys hardcoded (sk_, AKIA, ghp_, etc)
- [ ] .env no .gitignore
- [ ] .env.example sem valores reais
- [ ] JWT secrets, DB passwords em configs
- [ ] Secrets no git history
- [ ] Secret manager em uso
- [ ] Rotação de chaves (> 90 dias?)
- [ ] Tokens em comentários e TODOs
- [ ] Webhook secrets configurados
- [ ] Credenciais em CI/CD
- [ ] Least privilege em secrets
- [ ] Logs não imprimem secrets

## Categoria 2 · DEPENDÊNCIAS
- [ ] npm audit / pip-audit / cargo audit
- [ ] Pacotes com CVE crítico ou alto
- [ ] Dependências > 1 ano sem update
- [ ] Pacotes deprecated
- [ ] Lock file commitado
- [ ] Pacotes com poucos mantenedores
- [ ] Typosquatting suspeito
- [ ] Registries oficiais apenas
- [ ] SBOM gerado
- [ ] Vulnerabilidades transitivas

## Categoria 3 · CÓDIGO
- [ ] SQL injection (concatenação de string)
- [ ] XSS (dados não escapados)
- [ ] IDOR (sem validação de ownership)
- [ ] CSRF (forms sem token)
- [ ] SSRF (URLs do usuário sem validação)
- [ ] Path traversal
- [ ] Command injection
- [ ] Open redirect
- [ ] Insecure deserialization
- [ ] Validação de input ausente
- [ ] Rate limiting ausente
- [ ] Mass assignment em ORMs
- [ ] Race conditions
- [ ] Auth em múltiplos lugares
- [ ] Stack trace vazando ao usuário

## Categoria 4 · INFRA
- [ ] CORS restritivo (não usar *)
- [ ] Headers: CSP, HSTS, X-Frame-Options
- [ ] TLS 1.2+
- [ ] Certificados com auto-renew
- [ ] Cookies: HttpOnly, Secure, SameSite
- [ ] HTTP → HTTPS redirect
- [ ] Subdomains órfãos
- [ ] WAF em endpoints públicos
- [ ] DDoS protection
- [ ] S3/GCS buckets não públicos
- [ ] Serviços internos não expostos
- [ ] Logs de acesso em load balancers

## Categoria 5 · IAM
- [ ] MFA obrigatório pra admin
- [ ] Least privilege em roles
- [ ] Contas inativas removidas (> 90 dias)
- [ ] Service accounts com permissões mínimas
- [ ] Auditoria de mudanças em IAM
- [ ] Complexidade de senha exigida
- [ ] Reset de senha seguro
- [ ] Tokens com escopo limitado
- [ ] Timeout de sessão configurado
- [ ] SSO configurado quando aplicável

## Categoria 6 · LGPD
- [ ] Política de privacidade atualizada
- [ ] Consentimento explícito (opt-in)
- [ ] Base legal documentada
- [ ] Revogação de consentimento
- [ ] Direito de acesso (download)
- [ ] Direito de portabilidade
- [ ] Direito ao esquecimento
- [ ] Anonimização em não-prod
- [ ] DPO designado
- [ ] Plano de resposta a incidente
- [ ] Retenção definida
- [ ] Sub-processadores listados

## Categoria 7 · LOGS
- [ ] Eventos de auth logados
- [ ] Mudanças em dados sensíveis logadas
- [ ] Acesso admin logado
- [ ] Logs centralizados
- [ ] Retenção mínima 90 dias
- [ ] Dados sensíveis mascarados
- [ ] Alertas pra eventos suspeitos
- [ ] Timestamps em UTC/ISO 8601
- [ ] Correlação por request ID

## Categoria 8 · BACKUP
- [ ] Backup automático (DB, files, configs)
- [ ] Backup criptografado
- [ ] Backup em região diferente
- [ ] Restauração testada nos últimos 90 dias
- [ ] RTO documentado
- [ ] RPO documentado
- [ ] Point-in-time recovery
- [ ] Backup imutável (anti-ransomware)
- [ ] Runbook de DR escrito e testado
- [ ] Acesso a backups com auditoria

## Formato do report.md
# Cybersecurity Scan Report
Data: YYYY-MM-DD | Stack: [stack]
## Sumário
Checks: 90 | Passaram: X | Falharam: Y | Críticos: A | Altos: B | Médios: C | Baixos: D
## Achados Críticos
### [CRÍTICO] Título
Categoria: X | Arquivo: path:linha
Impacto: ... | Fix: ...
