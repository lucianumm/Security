# Enciclopédia de Segurança de Software, Infraestrutura, APIs e Sistemas de IA

> **Documento-base para desenvolvimento de uma Skill de Segurança**  
> **Versão:** 1.0.0  
> **Data de referência:** 04/11/2026  
> **Idioma:** Português do Brasil  
> **Abrangência:** engenharia de software full stack, APIs, autenticação, serviços, cloud, redes, containers, bancos de dados, CI/CD, aplicações móveis e sistemas com IA.  
> **Objetivo:** fornecer um catálogo de ataques, fraquezas, controles e verificações defensivas, apto a ser transformado em regras auditáveis por uma skill.

## Visão geral do inventário

| Métrica | Quantidade |
|---|---:|
| Entradas de ataques, técnicas e cenários de vulnerabilidade | **506** |
| Categorias de ameaças | **19** |
| Controles defensivos catalogados com ID | **136** |
| Fraquezas no ranking MITRE CWE Top 25 2025 | **25** |
| Referências técnicas e normativas com links | **43** |

**Nota sobre contagem:** entradas representam cenários e famílias de ameaça, não necessariamente técnicas únicas; certos ataques aparecem em mais de uma camada quando o contexto de defesa muda. O catálogo é propositalmente extensível.

### Guia de navegação

- **Seções 0 a 2:** conceitos, taxonomias, referenciais e camadas de proteção.
- **Seção 3:** autenticação, JWT, cookie `HttpOnly`, OAuth, MFA e sessões.
- **Seção 4:** 136 controles defensivos com identificadores.
- **Seção 5:** catálogo dos 506 cenários, organizado em 19 domínios.
- **Seções 6 a 10:** CWE Top 25, checklists, prioridade, stacks e testes.
- **Seção 11:** blueprint da futura skill, estrutura de diretórios e schema de findings.
- **Seções 12 a 15:** privacidade/LGPD, atualização, fontes e glossário.

## 0. Escopo, princípios e limitações

A segurança é um processo de gestão de riscos, e não uma propriedade conferida por um cabeçalho HTTP, um framework ou uma ferramenta. **Ataque** é uma ação adversarial; **vulnerabilidade** é uma fraqueza explorável; **ameaça** é uma possível causa de incidente; **exploit** é uma técnica de exploração; **controle** é uma medida preventiva, detectiva, responsiva ou corretiva; **risco** combina cenário, probabilidade e impacto. Uma ocorrência de ataque não prova, isoladamente, que o sistema possui uma vulnerabilidade explorável.

Não é possível reproduzir literalmente *todos os ataques conhecidos* em uma lista estática: existem múltiplas taxonomias, variantes, técnicas emergentes e CVEs publicados continuamente. Esta obra traz **um catálogo amplo de famílias relevantes**, com orientação defensiva e pontos de extensão para importar as bases MITRE ATT&CK, CWE, CAPEC, NVD/CVE e CISA KEV. Não equivale a um inventário completo de cada técnica, subtécnica, vulnerabilidade específica de produto ou campanha.

**Uso autorizado:** as verificações propostas destinam-se a repositórios, serviços e ambientes cuja avaliação foi expressamente autorizada. Testes intrusivos, exploração, fuzzing de alto volume, varredura de terceiros, tentativas reais de DoS/DDoS, engenharia social e manipulação de credenciais exigem escopo e autorização específicos. A skill deve preferir inspeção estática e testes não destrutivos.

**Regras fundamentais:** defesa em profundidade; menor privilégio; negar por padrão; validação no servidor; proteção de cada fronteira de confiança; separação de funções; identidade forte; auditabilidade; segurança no desenho; configurações seguras por padrão; automação de regressões; controle de mudanças; gestão contínua de risco e de incidentes.

### 0.1 Nomenclatura e identificadores

| Identificador | Descreve | Exemplo de aplicação |
|---|---|---|
| **CWE** | Fraqueza genérica de implementação/desenho | CWE-89, SQL Injection; CWE-862, autorização ausente |
| **CVE** | Vulnerabilidade específica de um produto/versão | Usar identificadores confirmados em boletins dos fornecedores |
| **CAPEC** | Padrões de ataque | Relacionar fraqueza, técnica e precondições |
| **MITRE ATT&CK** | Táticas, técnicas e subtécnicas de adversários | Mapeamento de detecção, ameaça e resposta |
| **OWASP Top 10** | Categorias priorizadas de riscos de aplicações | Planejamento de controles de AppSec |
| **OWASP ASVS** | Requisitos verificáveis de segurança | Checklist técnico com evidências |
| **OWASP WSTG** | Procedimentos estruturados de teste | Planejamento de validações em ambiente autorizado |
| **CVSS / EPSS / KEV** | Severidade técnica, probabilidade estimada de exploração e exploração confirmada | Priorizar correções considerando exposição e ativos |
| **STRIDE / LINDDUN** | Modelagem de ameaças e ameaças à privacidade | Análise de arquitetura e fluxos de dados |

**Atenção:** CVSS alto não significa exploração em andamento; KEV indica exploração observada no mundo real, e não uma classificação por gravidade. Uma CWE não é uma CVE.

## 1. Referenciais e versões adotados

1. **OWASP Top 10 Web 2025:** A01 Broken Access Control; A02 Security Misconfiguration; A03 Software Supply Chain Failures; A04 Cryptographic Failures; A05 Injection; A06 Insecure Design; A07 Authentication Failures; A08 Software or Data Integrity Failures; A09 Security Logging & Alerting Failures; A10 Mishandling of Exceptional Conditions.
2. **OWASP API Security Top 10 2023:** API1 BOLA; API2 Broken Authentication; API3 Broken Object Property Level Authorization; API4 Unrestricted Resource Consumption; API5 Broken Function Level Authorization; API6 Unrestricted Access to Sensitive Business Flows; API7 SSRF; API8 Security Misconfiguration; API9 Improper Inventory Management; API10 Unsafe Consumption of APIs.
3. **OWASP ASVS 5.0.0 (30/05/2025):** requisitos detalhados para desenho, desenvolvimento e verificação de aplicações/serviços. Usar identificadores oficiais da versão instalada, sem inventar números de controle.
4. **MITRE CWE Top 25 (2025):** priorização baseada em fraquezas recorrentes; não substitui análise específica do ambiente.
5. **MITRE ATT&CK Enterprise:** táticas e técnicas evolutivas, especialmente acesso inicial, persistência, elevação de privilégio, acesso a credenciais, movimento lateral, exfiltração e impacto.
6. **NIST CSF 2.0:** Governar, Identificar, Proteger, Detectar, Responder e Recuperar.
7. **NIST SP 800-218 (SSDF 1.1):** desenvolvimento seguro ao longo do SDLC.
8. **NIST SP 800-63-4 (2025):** identidade digital, autenticação e federação; observar o nível de garantia requerido por cenário.
9. **RFC 8725:** práticas atuais para JWT; **RFC 9700:** segurança de OAuth 2.0; considerar RFC 7636 (PKCE), RFC 9449 (DPoP), RFC 8705 (mTLS), RFC 7519 (JWT).
10. **OWASP MASVS/MASTG:** verificações de aplicações móveis.
11. **OWASP Kubernetes Top 10 2025:** controles do ecossistema Kubernetes.
12. **OWASP GenAI LLM Top 10 2026 e OWASP Agentic Applications Top 10 2026:** aplicações generativas, agentes, ferramentas e fluxos autônomos.
13. **OWASP Cheat Sheet Series / WSTG:** orientação prática para controles e testes.
14. **CISA Secure by Design / KEV, NVD, CERTs e boletins oficiais:** inteligência de vulnerabilidade e priorização operacional.

> Versões devem ser registradas no relatório gerado pela skill. Categorias OWASP 2025, API 2023 e GenAI 2026 não devem ser misturadas como se representassem uma única lista.

## 2. Arquitetura defensiva por camadas

| Camada | Proteções essenciais | Evidência que a skill deve procurar |
|---|---|---|
| Governança | Inventário, classificação, responsáveis, modelos de ameaça, política de exceções | Documentos versionados, owners, registro de decisões |
| Identidade | Passkeys/FIDO2, MFA, ciclo de vida de credenciais, controles contra abuso | Fluxos de login, MFA, recuperação, logs de autenticação |
| Sessão | Cookie seguro, expiração, rotação, revogação, CSRF, binding quando adequado | `Set-Cookie`, middleware, stores, invalidadores |
| Autorização | Negar por padrão, checagem por objeto/propriedade, isolamento entre tenants | Guards, políticas, filtros, testes cruzados |
| Aplicação | Validação, parametrização, output encoding contextual, CSP, sanitização | Sinks, templates, validadores, regras SAST |
| API | Contratos, quotas, autenticação, esquema, proteção de fluxos e terceiros | OpenAPI/GraphQL, gateways, testes negativos |
| Dados | Minimização, criptografia, RLS, isolamento, backup, retenção | Migrações, permissões, pipelines, políticas |
| Dependências | SBOM, versionamento, lockfile, assinaturas, SCA, procedência | CI/CD, integridade de artefatos, inventário |
| Execução | Hardening, isolamento, non-root, segmentação, egress, patch | IaC, Dockerfile, manifests, firewall, IAM |
| Perímetro | TLS, DDoS, WAF, CDN, rate limit, DNS, filtragem | Configuração de edge, redes, métricas |
| Observabilidade | Logs estruturados, correlação, métricas, alertas, retenção segura | SIEM, trilhas de auditoria, detecções |
| Resposta | Playbooks, revogação, contenção, evidências, recuperação e exercícios | Runbooks e testes de restauração |

## 3. Autenticação, identidade, cookies, JWT e sessões

### 3.1 Escolha entre sessões opacas e JWT

**Sessão opaca gerenciada no servidor:** cookie carrega um identificador aleatório de alta entropia; o estado e os privilégios são verificados no servidor. Vantagens: revogação imediata, controle central e menor risco de claims desatualizadas. Exige store resiliente e escalável.

**JWT assinado:** transporta claims verificáveis criptograficamente. É útil para interoperabilidade entre serviços ou domínios de confiança, mas **JWT não é obrigatoriamente superior a sessão opaca**; sua revogação e alteração de privilégios exigem desenho específico. JWT assinado geralmente **não cifra o conteúdo**: payloads podem ser decodificados. O acesso ao token deve ser protegido, mas não colocar segredos/PII desnecessária em claims.

**BFF (Backend-for-Frontend):** mantém tokens OAuth no servidor; o navegador usa cookie de sessão protegido. É uma opção relevante para aplicações web com identidade federada e APIs. Avaliar UX, domínios, CSRF e arquitetura antes de escolher.

### 3.2 Exemplo de cookie protegido (modelo, não configuração universal)

```http
Set-Cookie: __Host-session=<identificador-opaco>; Path=/; Secure; HttpOnly; SameSite=Lax
Cache-Control: no-store
```

- **`HttpOnly`**: impede acesso direto ao valor pelo `document.cookie`, mas não neutraliza XSS nem impede que scripts maliciosos executem ações autenticadas na sessão.
- **`Secure`**: impede envio do cookie sobre HTTP, ressalvadas peculiaridades locais; usar HTTPS com TLS configurado corretamente.
- **`SameSite=Strict` ou `Lax`**: reduz superfícies de CSRF, mas não substitui defesa CSRF em todos os modelos; `Strict` pode atrapalhar navegações legítimas. `SameSite=None` exige `Secure` e uma avaliação rigorosa.
- **`__Host-`**: exige `Secure`, `Path=/` e ausência de `Domain`; reduz riscos associados a subdomínios e sobrescrita de cookies.
- **`Path`/`Domain`**: controlar escopo; evitar ampla exposição a subdomínios que não tenham a mesma confiança.
- **`Max-Age`/`Expires`**: definir persistência conscientemente; cookies de sessão sem persistência têm comportamento dependente do navegador e restauração de sessão.
- **CSRF**: adotar token sincronizador ou *signed double-submit* vinculado à sessão, verificação de `Origin`/Fetch Metadata e ausência de alterações por `GET`. Para APIs com cookies, CORS restritivo não substitui anti-CSRF.

**Nunca** depender apenas de `HttpOnly`, `SameSite`, CORS ou WAF como única defesa. Tokens de acesso/refresh em `localStorage` ou `sessionStorage` ficam acessíveis a scripts do mesmo origin; para aplicações web sensíveis, preferir BFF/cookies protegidos e análise de ameaças. Cookies com sessão em memória também podem ser explorados indiretamente por XSS, por exemplo mediante requisições na sessão da vítima.

### 3.3 Política técnica para JWT (quando realmente usado)

1. Aceitar **somente algoritmos explicitamente permitidos** pela aplicação; rejeitar `alg=none` quando assinatura for exigida e bloquear confusão de algoritmo/chave.
2. Validar assinatura com biblioteca madura, chave apropriada, tipagem de token e política de chaves confiáveis. Não aceitar chaves arbitrárias apontadas por `jku`, `x5u`, `kid` ou payload.
3. Validar `iss`, `aud`, `sub`, `exp`, `nbf`, `iat` quando aplicáveis; checar tenant, finalidade, escopos e vínculo da identidade. Diferenciar **ID token**, **access token** e **refresh token**.
4. Gerar `jti` quando necessário para rastreamento/revogação. Usar tokens de acesso de curta duração conforme perfil de risco, sem duração universal arbitrária.
5. Refresh tokens: rotação por uso quando aplicável, detecção de reuse, revogação por dispositivo/família, armazenamento protegido e limpeza em logout.
6. Implementar invalidação em logout, recuperação de conta, troca de senha, comprometimento, revogação administrativa e alteração relevante de permissões; quando necessário, usar registro servidor de sessões/versão de autorização.
7. Proteger assinatura com armazenamento e rotação de chaves, `kid` controlado, JWKS legítimo, KMS/HSM conforme risco; não publicar secrets HS256.
8. Não registrar JWT ou secrets em logs, URLs, telemetria, exceções, páginas ou analytics. Proteger ambientes de build e testes.
9. Tratar token **bearer** como credencial: quem possui pode, em regra, usá-lo. Quando cabível, avaliar restrição ao emissor (DPoP/mTLS) e proteção contra replay.
10. Não usar conteúdo do JWT como prova autossuficiente da autorização de acesso a **um objeto específico**; verificação por recurso e tenant deve ocorrer no backend.
11. Diferenciar `401` (não autenticado/token inválido) e `403` (sem permissão), sem expor detalhes sensíveis.
12. Avaliar cache de chaves, disponibilidade do IdP, falhas de relógio e indisponibilidade de serviços de revogação. Definir comportamento seguro sob falha.

### 3.4 MFA, senhas, recuperação e ciclo de conta

- **Passkeys/WebAuthn/FIDO2:** autenticação resistente a phishing baseada em credenciais vinculadas a origem/RP ID; revisar registro, sincronização, recuperação, revogação e *step-up*.
- **MFA:** TOTP, chaves de segurança, autenticadores e fatores apropriados ao risco; SMS pode ser usado sob condições específicas, mas apresenta riscos de SIM swapping e phishing. Preferir fatores resistentes a phishing em contextos críticos.
- **Senhas:** hash adaptativo com `Argon2id` (preferencial, conforme OWASP), `scrypt`, `bcrypt` legado ou `PBKDF2` em contexto FIPS; sal individual; **não** usar SHA-256 puro, MD5 ou cifra reversível como armazenamento de senha. Configuração deve ser revista e calibrada operacionalmente.
- **Bloqueio/limitação progressiva:** limitar ataques sem permitir bloqueio abusivo massivo de usuários; combinar por IP, conta, dispositivo, rede e comportamento com proteção de privacidade.
- **Recuperação:** tokens aleatórios únicos, expiração curta, invalidação após uso, verificação da identidade e reautenticação para mudanças sensíveis; não revelar se e-mail está cadastrado.
- **Sessões:** rotacionar identificador após login/elevação de privilégio, expirar por inatividade e por tempo absoluto, permitir listar e revogar dispositivos, detectar anomalias e não reutilizar session IDs.
- **OAuth 2.0 / OpenID Connect:** authorization code com PKCE, `state` quando necessário, `nonce` conforme fluxo OIDC, redirect URI com correspondência estrita, validação de emissor/audience, proteção contra mix-up; evitar implicit grant e resource owner password credentials grant em novos sistemas. Considerar PAR/JAR e tokens restritos por remetente segundo risco.
- **SAML:** validar assinatura, audiência, destinatário, relógio, `InResponseTo`, identificadores únicos e prevenção contra XML signature wrapping; não confiar em metadados arbitrários.
- **Contas de serviço:** workload identity, credenciais efêmeras, menor privilégio, rotação, auditoria e ausência de contas compartilhadas.

## 4. Catálogo de controles e métodos defensivos

> Para cada controle, registrar **ID**, onde se aplica, ameaça mitigada, evidência, criticidade por contexto e como testar. Os itens abaixo são métodos, não produtos obrigatórios.

### 4.1 Governo de segurança e desenvolvimento

| ID | Controle | Aplicação e verificação |
|---|---|---|
| GOV-01 | Inventário de ativos e dados | Identificar aplicações, domínios, APIs, ambientes, repositórios, bases, proprietários e classificação da informação. |
| GOV-02 | Modelagem de ameaças STRIDE | Mapear ativos, fluxos, fronteiras de confiança, ameaças, controles e risco residual antes de funcionalidades críticas. |
| GOV-03 | Secure by Design / Secure by Default | Negar por padrão, eliminar privilégios excessivos e reduzir opções perigosas na configuração inicial. |
| GOV-04 | Critérios de aceite de segurança | Traduzir riscos em requisitos verificáveis ligados a tickets, ASVS e testes automatizados. |
| GOV-05 | Políticas de exceção e dívida técnica | Registrar exceção, prazo, owner, controles compensatórios e aceitação formal do risco. |
| GOV-06 | Revisão de arquitetura e código | Requerer revisão independente para autenticação, pagamentos, isolamento multi-tenant, criptografia e administração. |
| GOV-07 | Separação de deveres | Distanciar aprovação, desenvolvimento, deploy, administração de produção e acesso a dados sensíveis. |
| GOV-08 | Princípio de acesso mínimo | Permissões just-in-time, just-enough e revisões periódicas; evitar credenciais universais. |
| GOV-09 | Inventário de terceiros e fornecedores | Avaliar integrações, contratos, escopos de dados, exposição, SLA de patches e dependências críticas. |
| GOV-10 | Gestão de vulnerabilidades | Deduplicar findings, priorizar por exposição, criticidade, KEV/EPSS, impacto e contexto de negócio. |
| GOV-11 | Política de divulgação coordenada | Disponibilizar canal de reporte e triagem; `security.txt` quando aplicável. |
| GOV-12 | Exercícios tabletop e restauração | Ensaiar cenários de incidentes, indisponibilidade, ransomware e vazamentos. |

### 4.2 Identidade, autenticação e autorização

| ID | Controle | Aplicação e verificação |
|---|---|---|
| IAM-01 | Passkeys/WebAuthn | Validar origem/RP ID, assinatura, challenge, registro e revogação. |
| IAM-02 | MFA resistente a phishing | Privilegiar chaves FIDO2 para admin, acesso remoto e contas de alto risco. |
| IAM-03 | Hash de senha adaptativo | Argon2id/scrypt/PBKDF2/bcrypt conforme contexto, sal individual e configuração calibrada. |
| IAM-04 | Anti-enumeração de contas | Respostas e tempos equivalentes em login/recuperação, sem vazamento de registro. |
| IAM-05 | Rate limit e proteção contra brute force | Aplicar limites proporcionais a IP, usuário, dispositivo, tenant e operação. |
| IAM-06 | Sessão segura | ID aleatório, rotação, expiração por inatividade/absoluta e revogação. |
| IAM-07 | Cookie HttpOnly/Secure/SameSite | Escopo mínimo, prefixo `__Host-` quando possível, TLS e anti-CSRF. |
| IAM-08 | JWT seguro | Algoritmos permitidos, chave confiável, claims verificados, ciclo de vida, revogação. |
| IAM-09 | Refresh token rotation | Detectar reuse, revogar família, guardar credencial protegida no contexto correto. |
| IAM-10 | OAuth/OIDC robusto | Code+PKCE, exact redirect URI, validação de emissor, fluxo e tokens. |
| IAM-11 | Autorização por objeto | Verificar dono, tenant, papel e ação em cada recurso, não só na rota. |
| IAM-12 | Autorização por propriedade | Controlar leitura/alteração de atributos sensíveis e evitar mass assignment. |
| IAM-13 | RBAC/ABAC/ReBAC | Escolher modelo apropriado, centralizar políticas e testar combinações negativas. |
| IAM-14 | Isolamento multi-tenant | `tenant_id` de contexto autenticado, escopo no backend, RLS e testes cruzados. |
| IAM-15 | Menor privilégio de máquina | IAM para workload, roles estreitas, credenciais efêmeras, PAM/JIT. |
| IAM-16 | Reautenticação de operações críticas | Exigir step-up adequado para transferência, mudança de e-mail, segredos e permissões. |
| IAM-17 | Ciclo de vida de identidade | Provisionamento, revisão de acessos, desligamento, remoção de sessões e integração SCIM quando pertinente. |
| IAM-18 | Defesa contra sessão simultânea anômala | Monitorar mudanças bruscas de contexto, aplicar verificação contextual e informar usuário. |

### 4.3 Entrada, saída, navegação e navegador

| ID | Controle | Aplicação e verificação |
|---|---|---|
| APP-01 | Validação de esquema no servidor | Tipos, tamanho, formato, enumeração, semântica e limites de payload. |
| APP-02 | Consultas parametrizadas | Queries preparadas/bind parameters; jamais concatenar entrada do usuário em SQL. |
| APP-03 | Output encoding contextual | Escape em HTML, atributo, URL, JavaScript e CSS conforme o contexto de saída. |
| APP-04 | Sanitização de HTML | Sanitizador maduro e allowlist para conteúdo rico realmente permitido; preferir saída textual. |
| APP-05 | CSP forte | Usar nonces/hashes onde possível, `script-src` restritiva, `object-src 'none'`, `base-uri` e `frame-ancestors`. |
| APP-06 | Trusted Types | Reduzir sinks DOM XSS em navegadores compatíveis e aplicações de alto risco. |
| APP-07 | Anti-CSRF | Token sincronizador ou double-submit assinado, proteção de origem/Fetch Metadata. |
| APP-08 | TLS/HSTS | HTTPS e TLS atuais; HSTS após avaliar subdomínios e impactos operacionais. |
| APP-09 | Headers de segurança | `nosniff`, `Referrer-Policy`, `Permissions-Policy`, CSP e política de cache contextual. |
| APP-10 | Proteção contra clickjacking | `frame-ancestors`; `X-Frame-Options` apenas como compatibilidade. |
| APP-11 | CORS por origem confiável | Evitar `*` com credenciais; não refletir `Origin` sem validação, nem tratar CORS como autenticação. |
| APP-12 | SSRF allowlist/egress | Validar destino DNS/IP na conexão, restringir protocolos, redirects e acesso a metadados de cloud. |
| APP-13 | Proteção de arquivos e paths | IDs indiretos, canonicalização controlada, sandbox e restrição de diretórios permitidos. |
| APP-14 | Upload seguro | Tipo real, tamanho, extensão, antivírus quando pertinente, renomeação, armazenamento isolado. |
| APP-15 | Limites de decompression/processamento | Bloquear zip bombs, PDF/arquivo patológico, parsers recursivos, volume excessivo. |
| APP-16 | XML seguro | Desabilitar DTD/entities externas e recursos não requeridos; evitar XXE/XSLT inseguro. |
| APP-17 | Serialização segura | Não desserializar objetos executáveis de origem não confiável; limitar modelos e tipos. |
| APP-18 | ReDoS | Regex de complexidade controlada, limites de input, timeout e bibliotecas resilientes. |
| APP-19 | Evitar execução de shell | Usar APIs nativas; caso inevitável, argumentos separados, allowlist e sandbox. |
| APP-20 | Tratamento seguro de erros | Respostas genéricas, logging interno estruturado; sem stack traces públicos. |
| APP-21 | Limites transacionais e idempotência | Garantir atomicidade, bloqueios necessários e idempotency keys em efeitos financeiros. |
| APP-22 | Processamento de webhooks | Assinatura/HMAC, janela temporal, replay protection, controle de eventos e origem. |
| APP-23 | Proteção de cache | Chaves com tenant/usuário, respostas sensíveis `private/no-store`, controle de variantes. |
| APP-24 | Sanitização de CSV/fórmulas | Neutralizar células que possam ser interpretadas como fórmulas em planilhas. |
| APP-25 | Redirecionamentos permitidos | Destinos fixos ou allowlist; evitar open redirect e validação por prefixo frágil. |
| APP-26 | Normalização consistente | Evitar interpretações divergentes entre CDN, proxy, framework, parser e backend. |

### 4.4 APIs, serviços e integridade dos dados

| ID | Controle | Aplicação e verificação |
|---|---|---|
| API-01 | OpenAPI/JSON Schema | Contratos completos para parâmetros, corpos, respostas e versionamento. |
| API-02 | Inventário de endpoints | Catalogar ambientes, versões, APIs legadas, shadow APIs, owners e exposição. |
| API-03 | Gateway com defesa em profundidade | AuthN e quotas na borda **e** checagem real de autorização nos serviços. |
| API-04 | Quotas por custo | Controlar tempo, memória, chamadas externas, linhas, operações de DB e payload. |
| API-05 | Defesa de GraphQL | Limites de depth/complexity, aliases, batching, persistência de queries quando apropriado. |
| API-06 | Segurança gRPC | mTLS quando aplicável, identidade, limites de mensagens, autorização por método. |
| API-07 | Segurança de WebSocket | Checar `Origin`, autenticação, autorização por mensagem, tamanho e ciclo de conexão. |
| API-08 | Webhook trust | Verificação criptográfica, timestamp, deduplicação e segredos rotativos. |
| API-09 | Autorização de campo | Não confiar em atributos enviados por cliente; DTOs com allowlist de propriedades. |
| API-10 | Auditoria de mudanças | Registrar quem, o quê, quando, origem, antes/depois pertinente e integridade. |
| API-11 | Controle de replays | Nonce, timestamp, deduplicação, assinatura e transação conforme protocolo. |
| API-12 | Saída mínima | Reduzir DTOs, paginar, mascarar PII e evitar exposição de metadados internos. |
| API-13 | Contratos com terceiros | Validar respostas externas antes de inserir em banco, exibir ou usar como confiança. |
| API-14 | Consistência de validação | Revalidar após deserialização, filas, filas de eventos, caches e boundaries. |

### 4.5 Criptografia, dados e privacidade

| ID | Controle | Aplicação e verificação |
|---|---|---|
| DAT-01 | Criptografia em trânsito | TLS adequado nas conexões cliente, serviço, banco e message broker. |
| DAT-02 | Criptografia em repouso | Proteção de volumes, objetos, backups e campos de alto risco quando justificável. |
| DAT-03 | Algoritmos modernos | AEAD como AES-GCM/ChaCha20-Poly1305 quando aplicável; evitar modos inseguros. |
| DAT-04 | Gestão de chaves | KMS/HSM, segregação, rotação, revogação, versionamento e controle de acesso. |
| DAT-05 | Geração aleatória segura | CSPRNG para tokens, nonces, sessões e chaves; proibir IDs previsíveis como credenciais. |
| DAT-06 | Segredos fora do código | Secret manager, variáveis protegidas e scanning; cuidado com leaks por imagens e logs. |
| DAT-07 | Minimização dos dados | Coletar só o necessário; reter pelo prazo devido; mascarar em teste/observabilidade. |
| DAT-08 | Isolamento de tenants | Linhas/colunas/bancos/contas isolados conforme risco; RLS como defesa adicional. |
| DAT-09 | Backups resilientes | Criptografia, acesso mínimo, cópia imutável/offline e teste periódico de restauração. |
| DAT-10 | Retenção e descarte | Política de lifecycle, deleção verificável e classificação de dados. |
| DAT-11 | Prevenção de exportação indevida | Aprovação, quotas, alertas, DLP e auditoria de acesso maciço. |
| DAT-12 | Tokenização/pseudonimização | Reduzir exposição de identificadores, avaliar reversibilidade e segregação. |
| DAT-13 | Integridade e assinatura | Assinar artefatos/objetos quando necessário; comparar hash com origem confiável. |
| DAT-14 | Proteção de dados em logs | Redação de PII/segredos, retenção, acesso e proteção contra adulteração. |

### 4.6 Rede, DDoS, infraestrutura, cloud e execução

| ID | Controle | Aplicação e verificação |
|---|---|---|
| NET-01 | Proteção volumétrica DDoS | Provedor de mitigação L3/L4, capacidade upstream e procedimentos de escalonamento. |
| NET-02 | Proteção DDoS na aplicação | CDN/WAF, challenge adaptativo, cache, proteção do origin, limites por rota e custo. |
| NET-03 | Rate limiting distribuído | Limites corretos em multi-instância, Redis/gateway quando apropriado e chave de identidade confiável. |
| NET-04 | Circuit breaker e backpressure | Impedir cascatas de falhas e filas infinitas, definir timeouts e budgets. |
| NET-05 | Proteção de origin | Firewall/ACL para aceitar tráfego só do proxy legítimo; validar headers de IP de origem. |
| NET-06 | Segmentação de rede | Privado por padrão, portas mínimas, regras de entrada/saída e isolamento entre tiers. |
| NET-07 | Egress filtering | Restringir tráfego externo de workloads, SSRF e canais de exfiltração. |
| NET-08 | WAF / WAAP | Regras gerenciadas e customizadas, observabilidade e teste de falsos positivos. |
| NET-09 | IDS/IPS e NDR | Detecção de comportamento de rede anômalo; correlação com app e hosts. |
| NET-10 | DNS seguro | Controles de alteração, DNSSEC quando apropriado, inventário, CAA e monitoramento. |
| NET-11 | Proteção contra takeover | Remover DNS pendente e verificar posse de subdomínios e buckets vinculados. |
| NET-12 | Hardening do sistema | Patches, desativar serviços, usuários não privilegiados, firewall, segurança de SSH. |
| NET-13 | Gestão de certificados | Automação de renovação, validação de cadeia, validade e chaves privadas. |
| NET-14 | IAM de cloud mínimo | Evitar permissões globais, separar contas e regiões e fiscalizar federação/roles. |
| NET-15 | CSPM/IaC scanning | Detectar buckets públicos, security groups amplos, IAM, logging e criptografia. |
| NET-16 | Imagens/containers mínimos | Imagens oficiais e fixadas, atualização, scanning, usuário non-root e sistemas read-only. |
| NET-17 | Sandbox / isolamento | Seccomp, AppArmor/SELinux, namespaces, capacidades mínimas, limites de recursos. |
| NET-18 | Kubernetes RBAC e policies | Service accounts mínimas, admission policies, network policies, Pod Security, quotas. |
| NET-19 | Secrets em runtime | Não embutir em image layers nem expor via logs, endpoints de debug ou env dumps. |
| NET-20 | Metadata service hardening | AWS IMDSv2, restrição de acesso a metadados, egress e identities de escopo mínimo. |
| NET-21 | Proteção de infraestrutura como código | Revisão, planos aprovados, secrets protegidos, estados remotos criptografados. |
| NET-22 | Resiliência e contingência | Regiões/zones redundantes quando necessário, testes de failover e RTO/RPO definidos. |
| NET-23 | Endpoint/EDR | Proteção de estações, servidores e workloads, telemetria e contenção. |
| NET-24 | Zero Trust contextual | Autenticar e autorizar cada acesso relevante, limitar confiança em rede interna. |

### 4.7 Cadeia de suprimentos, CI/CD e testes

| ID | Controle | Aplicação e verificação |
|---|---|---|
| SDLC-01 | SAST | Detectar padrões de fluxo perigoso no código; validar findings manualmente. |
| SDLC-02 | SCA e SBOM | Inventariar dependências diretas/transitivas, licenças, versões e vulnerabilidades. |
| SDLC-03 | Secrets scanning | Examinar código, histórico, artefatos e pipelines, com revogação após vazamento. |
| SDLC-04 | DAST autorizado | Testes dinâmicos controlados em ambientes autorizados com taxa e escopo limitados. |
| SDLC-05 | Fuzzing de parsers | Entradas malformadas em ambiente isolado, com limites e monitoramento. |
| SDLC-06 | IaC e container scanning | Analisar Terraform, Kubernetes, Dockerfiles e imagens quanto a hardening e CVEs. |
| SDLC-07 | Lockfiles e versões fixas | Controlar resolução de dependências e builds reproduzíveis onde possível. |
| SDLC-08 | Proteção de branch e revisão | Aprovações, checks obrigatórios, Code Owners e política contra bypass. |
| SDLC-09 | OIDC para pipeline | Trocar segredos long-lived por identidades de workload e tokens de vida curta. |
| SDLC-10 | Assinatura/proveniência de build | Assinar artefatos, verificar attestation e cadeia de build segundo SLSA quando aplicável. |
| SDLC-11 | Isolamento de runners | Separar contexto não confiável, PRs externos e produção; não compartilhar secrets. |
| SDLC-12 | Governança de pacotes | Registry confiável, revisão de novos pacotes, nomes e integridade. |
| SDLC-13 | Releases progressivos | Canary/blue-green, health checks, rollback e teste de segurança pós-deploy. |
| SDLC-14 | Testes de autorização | Matriz usuário × tenant × recurso × ação com cenários negativos. |
| SDLC-15 | Testes regressivos de segurança | Cada achado corrigido deve gerar teste que falhe na versão vulnerável. |
| SDLC-16 | Artefatos de evidência | Repositório, commit, arquivo/linha, regra, impacto, reprodução não destrutiva e fix. |

### 4.8 Operação, detecção e resposta

| ID | Controle | Aplicação e verificação |
|---|---|---|
| OPS-01 | Logs estruturados | Identidade, resultado, recurso, correlation ID, timestamp confiável; sem segredos. |
| OPS-02 | Auditoria de segurança | Sucessos e falhas de autenticação, autorização, administração, exportações e segredos. |
| OPS-03 | Centralização e integridade | SIEM/log pipeline protegido, retenção adequada, restrições de acesso e imutabilidade conforme risco. |
| OPS-04 | Alertas acionáveis | Detectar credential stuffing, mudanças de papel, exfiltração, picos de erros e tráfego. |
| OPS-05 | Métricas RED/USE e SLO | Avaliar taxa, erros, latência, recursos e degradações atípicas. |
| OPS-06 | Playbooks de incidente | Contenção, triagem, preservação de evidências, comunicação, recuperação e lições aprendidas. |
| OPS-07 | Rotação e revogação emergencial | Capacidade comprovada de invalidar tokens, chaves, contas e integrações comprometidas. |
| OPS-08 | Threat hunting autorizado | Investigar hipóteses baseadas em ATT&CK e detecções, respeitando privacidade. |
| OPS-09 | Testes de backup/restore | Verificar integridade, tempo de recuperação e chaves de descriptografia. |
| OPS-10 | Monitoramento de KEV | Priorizar correções de falhas exploradas, especialmente serviços expostos. |
| OPS-11 | Observabilidade de anti-abuso | Detectar scraping, bots, enumeração, criação massiva de contas e fraudes. |
| OPS-12 | Segurança dos próprios logs | Prevenir log injection, saturação, vazamento e adulteração das trilhas. |

## 5. Catálogo de ataques e vulnerabilidades

**Como ler:** cada entrada descreve a **família de ataque**, a **fraqueza/precondição e o impacto**, e as **defesas/detecções**. A gravidade concreta depende de exposição, dados afetados, privilégios e controles existentes. Os exemplos são conceituais, voltados à prevenção, sem roteiros de exploração de alvos.

### 5.1 Identidade, autenticação e sessões

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Brute force online | Sem controle de tentativas, credenciais podem ser adivinhadas repetidamente. | MFA, limites por conta/rede, alertas, respostas uniformes e testes de limites. |
| Credential stuffing | Pares usuário/senha vazados são reutilizados em serviços diferentes. | MFA/passkeys, monitoramento de vazamentos, proteção anti-bot, detecção de logins anômalos. |
| Password spraying | Mesma senha comum testada contra múltiplas contas, evitando limiares por usuário. | Detecção agregada por origem/campanha, MFA e rate limits multidimensionais. |
| Ataque de dicionário offline | Base de hashes vazada pode permitir tentativa de senhas em massa. | Argon2id/scrypt com sal único, parâmetros robustos, pepper protegido quando adotado. |
| Rainbow tables | Hash rápido sem salt é passível de comparação com tabelas pré-computadas. | Salt aleatório e hash adaptativo adequado, sem SHA-256 puro. |
| Credential phishing | Usuário é induzido a divulgar senha/código em página fraudulenta. | Passkeys/FIDO2, conscientização, monitoramento de domínio, proteção de e-mail. |
| Adversary-in-the-middle de login | Proxy fraudulento intercepta sessão ou credencial de autenticação não resistente a phishing. | FIDO2/passkeys, validação de origem, detecção de token/rede anômalos, step-up. |
| MFA fatigue / push bombing | Requisições repetidas levam usuário a aprovar indevidamente. | Number matching, limitação de prompts, fatores resistentes a phishing e alertas. |
| SIM swap | Controle do número telefônico compromete recuperação ou MFA baseado em SMS. | Preferir passkeys/TOTP/chaves, controles adicionais para recuperação e mudanças. |
| OTP guessing/replay | Códigos com entropia ou validação inadequada são adivinhados ou reutilizados. | TTL curto, uso único, limite de tentativas e vinculação de transação. |
| Bypass de MFA | Rotas auxiliares, APIs ou fluxos legados dispensam o segundo fator. | Testar cobertura em todos os fluxos, negar sessão parcialmente autenticada. |
| Account enumeration | Login, cadastro e reset revelam contas válidas por mensagens ou tempo. | Respostas uniformes, limitar endpoints de descoberta e telemetria. |
| Reset token prediction | Token de recuperação previsível ou curto permite tomada de conta. | CSPRNG, uso único, expiração, armazenamento hash e validação no backend. |
| Reset token leakage | Links de recuperação aparecem em logs, Referer, analytics ou terceiros. | Remover tokens de telemetria, `Referrer-Policy`, `no-store`, fluxo adequado. |
| Account recovery abuse | Suporte ou fluxo de recuperação tem verificação de identidade fraca. | Verificações proporcionais ao risco, rastreamento, notificações e atrasos de segurança quando pertinentes. |
| Session hijacking | Cookie ou token é roubado e usado em outro contexto. | TLS, HttpOnly, XSS prevention, revogação, monitoramento de sessão. |
| Session fixation | Identificador conhecido pelo atacante persiste após autenticação. | Regenerar sessão no login e alterações de privilégio. |
| Session prediction | IDs sequenciais ou gerados por PRNG inadequado permitem adivinhação. | IDs de alta entropia com CSPRNG e testes estatísticos básicos. |
| Session replay | Token capturado continua válido indefinidamente ou sem restrições. | Expiração, revogação, rotação, detecção de reuse e sender constraint quando apropriado. |
| Sessão não invalidada no logout | Cookie some do browser, mas token segue válido no servidor. | Revogação efetiva e teste de reutilização pós-logout. |
| Autorização defasada no JWT | Privilégio foi revogado, porém claims antigos seguem aceitos. | Tokens curtos, políticas servidor, sessão/versionamento e invalidação de eventos. |
| JWT `alg=none` / confusão algorítmica | Validador confia em algoritmo não permitido ou confunde chaves. | Allowlist estrita, tipagem de token, biblioteca madura e testes negativos. |
| JWT `kid`/`jku`/`x5u` manipulation | Metadados não confiáveis controlam busca de chaves ou URL externa. | JWKS confiável fixado, validação de parâmetros, bloqueio de SSRF. |
| JWT audience/issuer confusion | Token destinado a outra aplicação ou emissor é aceito. | Validar `aud`, `iss`, finalidade e tipo do token no receptor. |
| Refresh token reuse | Refresh token antigo reaparece após rotação, indicando cópia. | Detecção e revogação de família/dispositivo, logs e resposta. |
| OAuth authorization code interception | Código é interceptado ou reusado em fluxo inadequado. | PKCE, HTTPS, redirect URI exata, código curto e uso único. |
| OAuth redirect URI manipulation | Redirect permissivo recebe códigos/tokens em destino controlado. | Match exato, destinos registrados, proibir open redirect no fluxo. |
| OAuth mix-up / token substitution | Cliente confunde provedores, destinatários ou classes de token. | `iss`, `state`, `nonce` onde aplicável, metadados de issuer e token validation. |
| OAuth scope escalation | Escopo não solicitado/consentido ou permissões excedentes são concedidos. | Scopes mínimos, consentimento e autorização servidor por recurso. |
| OAuth consent phishing | Aplicação maliciosa solicita consentimento amplo de conta legítima. | App governance, consentimento controlado, auditoria e revogação de grants. |
| SAML signature wrapping | Parser e validador selecionam elementos XML diferentes. | Validar o elemento efetivamente consumido, assinatura, issuer, audience e destination. |
| SAML replay | Assertion válida é reutilizada por falta de controle de ID/tempo. | `InResponseTo`, janela temporal, cache de assertions usadas e validação de destinatário. |
| Passkey account-linking confusion | Credencial é vinculada à conta errada devido a contexto incorreto. | Vincular challenge, RP ID, usuário, operação e estado autenticado. |
| API key leakage | Chave em Git, front-end, logs ou URL permite chamadas não autorizadas. | Vault, escopos, revogação, secrets scanning e limites de uso. |
| Shared admin credentials | Ausência de identidade individual impede revogação e atribuição. | Contas nominativas, PAM/JIT e auditoria. |

### 5.2 Autorização e separação de privilégios

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| IDOR (Insecure Direct Object Reference) | Identificador alterado dá acesso a objeto de outra pessoa. | Autorizar propriedade e tenant em todo acesso, não apenas validar ID. |
| BOLA (Broken Object Level Authorization) | API verifica login, mas não se usuário pode acessar cada objeto. | Verificação no backend, consultas contextualizadas e testes interusuários. |
| BFLA (Broken Function Level Authorization) | Usuário comum consegue invocar função administrativa. | Guards por operação, políticas centralizadas e testes de papéis. |
| BOPLA (Broken Object Property Level Authorization) | Campo sensível pode ser lido/modificado sem permissão. | DTOs de resposta/escrita com allowlist e política por atributo. |
| Horizontal privilege escalation | Uma conta alcança dados/ações de usuário de mesmo nível. | Políticas por objeto, subject e tenant; testes cruzados. |
| Vertical privilege escalation | Usuário de baixo privilégio executa funções administrativas. | RBAC/ABAC/ReBAC no servidor, deny-by-default e segregação. |
| Forced browsing | URL interna ou endpoint não exibido no menu é acessível diretamente. | Verificar permissão em cada rota; interface não é controle de segurança. |
| Tenant escape | Falta de filtro por `tenant_id` expõe dados de outros clientes. | Tenant derivado da sessão, escopo nas queries, RLS e testes multi-tenant. |
| Mass assignment | JSON recebido altera `role`, `isAdmin`, saldo, status ou proprietário. | Schemas explícitos de escrita, jamais espalhar corpo bruto para ORM. |
| Overposting / underposting | Campos inesperados ou omitidos alteram lógica/autorização. | Contratos de entrada estritos e autorização por campo. |
| Insecure default role | Cadastro recebe privilégios excessivos por configuração padrão. | Role mínimo, revisão de onboarding, teste de novos usuários. |
| RBAC rule conflict | Regra ampla sobrepõe restrição específica ou negação. | Avaliação determinística, deny precedence e testes de política. |
| Client-side role trust | Permissões são aceitas por parâmetro ou estado do frontend. | Decidir no servidor, assinar contexto apenas quando necessário e verificar fonte. |
| Admin endpoint exposure | API administrativa fica pública ou sem proteção adicional. | Separação, rede restrita, SSO/MFA, authorization e logs. |
| Multi-step authorization bypass | Fluxo confere permissão no início, mas não no passo final. | Autorizar cada operação final, revalidar estado e ownership. |
| TOCTOU (check/use race) | Permissão ou condição muda entre validação e uso. | Transações, locks, verificações atômicas e invariantes no banco. |
| Authorization caching flaw | Decisão cacheada é reutilizada entre usuários/tenants. | Cache key contendo principal, tenant, recurso, ação e versão de política. |
| RLS policy bypass | Papel com BYPASSRLS ou conexão privilegiada ignora política. | Conexões de aplicação sem superuser, testes do papel real e RLS rigoroso. |
| File ACL inheritance abuse | Arquivo herda permissão ampla e fica visível publicamente. | ACL explícita, least privilege e scanner de objetos públicos. |
| Insecure impersonation | Suporte assume identidade de cliente sem controle ou rastreio. | Aprovação contextual, tempo limitado, banner, auditoria e controles restritos. |
| Cross-tenant job/queue confusion | Worker processa job sob tenant errado por falta de contexto confiável. | Propagar identidade assinada/validada, isolamento e checagem no consumidor. |
| Confused deputy | Serviço com privilégios elevados atende pedido de ator não autorizado. | Autorizar ação em nome do principal, delegação restrita e auditável. |
| Broken access on exports | PDF/CSV/exportações ignoram filtros da interface. | Aplicar mesma autorização e scoping em jobs assíncronos. |
| Partial-object exposure | Endpoint retorna objeto inteiro e frontend esconde campos. | Serialização mínima e teste de payload de rede. |

### 5.3 Injeção, interpretação e execução de código

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| SQL Injection (SQLi) | Entrada concatenada em SQL muda a consulta e pode expor/alterar dados. | Prepared statements, bind parameters, roles restritas e teste SAST/DAST. |
| SQLi blind/time-based | Respostas sem dados ainda podem vazar informações via diferenças de comportamento/tempo. | Parametrização em todos os caminhos, erros neutros e monitoramento. |
| SQLi em ORM/raw query | Uso indevido de `raw`, interpolação de colunas ou ordenação dinâmica. | Query builders seguros, allowlist de identificadores e revisão de sinks. |
| NoSQL Injection | Operadores/objetos inesperados alteram filtros de busca/autenticação. | Validar tipos de JSON, não aceitar operadores arbitrários do usuário. |
| MongoDB operator injection | Objeto recebido é interpretado como operador de consulta. | DTO com tipos escalares e parâmetros seguros de driver. |
| GraphQL injection into backend | Resolver transforma argumentos em SQL, shell ou chamadas perigosas. | Validação dos resolvers e controles do sink final. |
| LDAP Injection | Entrada manipula filtros de diretório e regras de busca. | APIs de filtro com encoding apropriado e restrição de busca. |
| XPath/XQuery Injection | Parâmetro altera expressão de consulta XML. | Bind variables e validação de esquema/consulta. |
| OS Command Injection | Entrada chega a shell ou comando de sistema. | Evitar shell; usar APIs nativas, argumentos separados e sandbox. |
| Code Injection / eval | Conteúdo não confiável vira código interpretado. | Proibir `eval` em dados externos e usar formatos declarativos estritos. |
| Remote Code Execution (RCE) | Falha permite execução de instruções em contexto do servidor. | Patches, sandbox, menor privilégio, bloqueio de execução dinâmica e EDR. |
| Server-Side Template Injection (SSTI) | Dados controlados são interpretados como template com expressões. | Templates estáticos, autoescape e ausência de avaliação de templates arbitrários. |
| Expression Language injection | Linguagem de expressões recebe conteúdo não confiável. | Não executar expressões fornecidas pelo cliente; allowlists e isolamento. |
| Prototype Pollution (JavaScript) | Merge de objetos permite contaminar protótipos e lógica posterior. | Bloquear chaves especiais, objetos sem protótipo quando cabível, bibliotecas corrigidas. |
| Insecure deserialization | Objetos com tipos/gadgets perigosos são reconstruídos. | Formatos seguros, allowlist de tipos e proibir serialização executável. |
| PHP object injection | Dados serializados acionam métodos mágicos/gadgets perigosos. | Não usar `unserialize` em dados externos; validar tipos e remover gadgets. |
| Java deserialization gadgets | Deserializador aceita classes/objetos com efeitos colaterais. | ObjectInputFilter, tipos permitidos e formatos neutros. |
| YAML unsafe load | Parser instancia objetos ou executa construções indevidas. | Safe loader, schemas estritos e limites. |
| XML External Entity (XXE) | Processador XML resolve entidades externas, podendo ler arquivos ou fazer SSRF. | Desabilitar DTD/entities externas e recursos de rede. |
| XML/XSLT transformation injection | Transformação permite extensões, leitura ou execução indevida. | Restringir transformadores, esquemas e acesso externo. |
| Server-Side Includes Injection | Conteúdo interpretado como diretiva de SSI. | Não avaliar conteúdo de usuário como SSI; restringir configuração. |
| CRLF Injection | Quebras de linha são interpretadas em headers, logs ou protocolos. | APIs seguras, rejeição de caracteres de controle, encoding contextual. |
| HTTP Response Splitting | Cabeçalho controlado cria resposta HTTP manipulada. | Validar headers e não interpolar entrada em linhas de protocolo. |
| HTTP Header Injection | Host, Referer ou campos controlados alteram lógica downstream. | Validar campos de confiança, normalização e allowlists. |
| Log Injection / log forging | Texto malicioso cria entradas falsas ou quebra formato da trilha. | Logs JSON estruturados, escaping e limitação de tamanho. |
| Email header injection | Entrada com controles altera destinatários ou cabeçalhos SMTP. | APIs de e-mail, validação de endereços e rejeição de CRLF. |
| CSV/Formula Injection | Células exportadas executam fórmulas ao abrir planilha. | Neutralizar valores perigosos conforme software de destino. |
| Regex DoS (ReDoS) | Expressão com backtracking excessivo consome CPU. | RegEx linear/segura, limites de input e timeout. |
| HTTP Parameter Pollution (HPP) | Parâmetros duplicados são interpretados de formas distintas por camadas. | Política única de parsing e rejeição de duplicatas inesperadas. |
| JSON parser differential | Proxy e backend interpretam mesmo JSON com regras diferentes. | Canonicalização, parser uniforme e testes de ambiguidades. |
| Unicode normalization bypass | Formas Unicode distintas contornam validações ou ACL. | Normalização consistente, IDs canônicos e testes de caracteres equivalentes. |
| Path Traversal / `../` | Caminho controlado sai do diretório permitido e acessa arquivos indevidos. | Paths fixos/IDs, canonicalização, isolamento e permissões mínimas. |
| Local File Inclusion (LFI) | Parâmetro seleciona arquivo local fora da área autorizada. | Templates fixos, mapeamento por IDs e restrição de diretórios. |
| Remote File Inclusion (RFI) | Aplicação carrega recurso remoto como código ou conteúdo interpretado. | Proibir inclusão por URL e limitar origens. |
| ZIP Slip | Arquivo comprimido contém paths que escrevem fora do destino. | Normalizar cada entrada, restringir raiz e evitar symlink abuse. |
| Arbitrary File Upload | Upload de arquivo executável ou perigoso gera comprometimento. | Armazenamento fora de webroot, tipos validados, renomeação, sandbox/AV. |
| Polyglot file upload | Arquivo se apresenta como formato inocente e executável em outro parser. | Validar conteúdo real, transcoding e servir como download. |
| Archive / decompression bomb | Arquivo pequeno expande para consumo enorme de recursos. | Limitar tamanho expandido, arquivos, profundidade e CPU. |
| Image/PDF parser exploit | Parser vulnerável executa código ou esgota recursos ao processar arquivo. | Atualizações, isolamento, formatos seguros, limites e análise de mídia. |
| SSRF | Backend acessa URL controlada, alcançando redes internas ou serviços protegidos. | Allowlist, validação DNS/IP na conexão, egress, bloqueio de metadata. |
| Blind SSRF | Resposta não aparece ao atacante, mas chamada indevida ocorre. | Políticas de saída, logs de rede/DNS e validação de destino. |
| DNS Rebinding | Endereço aprovado muda para IP interno antes da conexão. | Resolver e conectar a IP validado, checagem pós-resolução e egress. |
| Open Redirect | Navegação legítima redireciona a destino fraudulento arbitrário. | URLs de destino fixas/allowlist e validação por origem completa. |

### 5.4 Web, navegador, HTTP, cache e origens

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Reflected XSS | Entrada aparece em resposta HTML sem encoding adequado. | Escape contextual, frameworks seguros, CSP e testes de sinks. |
| Stored XSS | Conteúdo persistido executa script para outros usuários. | Sanitização de conteúdo rico e saída codificada contextual. |
| DOM-based XSS | JavaScript usa dados não confiáveis em sinks DOM perigosos. | `textContent`, APIs seguras, Trusted Types e CSP. |
| Mutation XSS (mXSS) | DOM normalizado pelo navegador converte HTML aparentemente seguro em conteúdo ativo. | Sanitizador atualizado, contexto de saída controlado e testes por navegador. |
| CSS/Style injection | Valores CSS inseguros alteram aparência ou provocam vazamentos contextuais. | Restringir estilos a propriedades/valores permitidos. |
| HTML injection | Conteúdo externo manipula interface, formulários ou links sem necessariamente executar JS. | Escape HTML, sanitização e CSP. |
| DOM clobbering | IDs/names HTML interferem em variáveis e propriedades usadas por scripts. | Evitar busca global implícita, checar tipos e usar referências explícitas. |
| Clickjacking | Página é incorporada em frame para induzir cliques invisíveis ou desviados. | CSP `frame-ancestors`, confirmação de ações sensíveis. |
| Reverse tabnabbing | Nova aba acessa `window.opener` e redireciona aba de origem. | `rel="noopener noreferrer"` e padrões modernos de abertura. |
| CSRF | Browser envia cookies automaticamente em operação forjada de outro contexto. | Token anti-CSRF, Origin/Fetch Metadata, SameSite e métodos corretos. |
| Client-side CSRF | JS legítimo é convencido a produzir request malicioso no próprio origin. | Validar dados que compõem URL/ação, permitir destinos fixos. |
| CORS misconfiguration | API permite leitura por origem indevida, especialmente com credenciais. | Allowlist exata de origens, `Vary: Origin`, revisão de credentials. |
| CORS `null` origin trust | Origem nula é tratada como confiável indiscriminadamente. | Rejeitar origem nula fora de casos explicitamente justificados. |
| Subdomain takeover | DNS aponta para serviço externo desalocado que pode ser reivindicado. | Inventário, apagar registros órfãos e verificar posse de serviços. |
| Cookie tossing / cookie injection | Subdomínios conseguem plantar cookies em domínio pai. | `__Host-`, evitar Domain amplo, isolamento de subdomínios. |
| Session cookie theft via XSS | Script malicioso acessa cookie sem HttpOnly ou atua na sessão autenticada. | HttpOnly e mitigação de XSS; revalidação de ações críticas. |
| Mixed content | Recursos HTTP comprometem confidencialidade/integridade de página HTTPS. | HTTPS em toda a cadeia, CSP e HSTS conforme planejamento. |
| HTTPS stripping | Navegação é reduzida para conexão sem proteção. | HTTPS obrigatório, HSTS corretamente configurado. |
| TLS downgrade | Negociação permite versão/cifra obsoleta. | TLS moderno, configuração e monitoramento. |
| Certificate validation bypass | Cliente aceita certificado inválido ou não verifica hostname. | Validação rigorosa, trust store legítima e testes negativos. |
| Cache poisoning | Entrada controlada contamina versão cacheada servida a outros usuários. | Cache keys corretas, cabeçalhos canonizados e edge/backend consistentes. |
| Web cache deception | Endpoint privado é armazenado como conteúdo público. | Cache-Control apropriado e regras de cache conscientes da autenticação. |
| Host header poisoning | Host não validado altera links, redirects, reset de senha ou roteamento. | `Host`/proxy confiáveis, hostname canônico e configuração de forwarded headers. |
| HTTP request smuggling (CL.TE/TE.CL e variantes) | Frontend e backend divergem no framing das requisições, misturando tráfego. | Parsers alinhados, atualizações de proxies e testes controlados de protocolo. |
| HTTP/2 request desync | Conversão HTTP/2 para HTTP/1 gera interpretação divergente. | Normalização, proxy atualizado e revisão do downgrade. |
| HTTP/3 edge parser ambiguity | Implementações divergentes em borda e origem podem causar roteamento inseguro. | Patching, validação e testes de protocolos sob carga controlada. |
| Request routing ambiguity | Path ou header ambíguo seleciona backend não previsto. | Canonicalização e matching estritos, remoção de caminhos legados. |
| Browser storage exfiltration | Tokens em `localStorage` ou IndexedDB são acessados por scripts comprometidos. | Evitar tokens bearer persistentes acessíveis a JS quando houver opção mais segura. |
| Service Worker poisoning | Service worker malicioso persiste e intercepta recursos no escopo. | CSP, segurança da origem, escopo restrito e rotina de atualização/revogação. |
| Third-party script compromise | JS de fornecedor carrega na origem e recebe privilégios da página. | Reduzir terceiros, SRI quando viável, CSP, isolamento e monitoramento. |
| XS-Leaks | Diferenças em tempo, cache ou comportamento revelam informação cross-origin. | Isolamento de recursos, headers COOP/COEP/CORP conforme arquitetura, respostas uniformes. |
| Referrer data leakage | URLs com identificadores/token são enviadas em `Referer` a terceiros. | Não usar secrets em URL, política de referência restrita. |
| Browser extension compromise | Extensão com privilégios pode ler/modificar páginas ou dados do usuário. | Gestão de extensões, browser corporativo e minimizar dados expostos. |
| Client-side source map exposure | Mapas de fonte públicos revelam estruturas internas e ajudam reconhecimento. | Política de publicação e revisão de artefatos, sem segredos no bundle. |
| Error detail disclosure | Stack traces, dumps e frameworks expõem informações sensíveis. | Erro público mínimo, observabilidade interna com controle de acesso. |

### 5.5 APIs, GraphQL, gRPC, WebSockets e integrações

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| REST BOLA | API retorna qualquer recurso pelo ID sem ownership. | Contextualizar consultas, checar tenant e usuário a cada operação. |
| REST BFLA | Método proibido ao papel atual é alcançado por endpoint alternativo. | Política por rota/método e testes por função. |
| API excessive data exposure | Endpoint envia campos demais, mesmo se frontend não os exibe. | Modelos explícitos de resposta e minimização de dados. |
| API mass assignment | Campos arbitrários do corpo sobrepõem estado sensível. | Schema de escrita com whitelist e separação de DTO/entidade. |
| Excessive resource consumption | Paginação, export ou busca consome CPU, memória e banco sem limites. | Quotas por operação/custo, paginação máxima, budgets e circuit breaker. |
| Shadow API | Serviço não documentado escapa das políticas de segurança. | API discovery, inventário de gateway e remoção de versões não suportadas. |
| Deprecated API exposure | Versão antiga mantém falhas corrigidas nas versões novas. | Deprecar com prazo, bloquear rotas e aplicar patches em todas as versões ativas. |
| API schema bypass | Validação na documentação não é aplicada no runtime. | Middleware de schema testado e falha fechada. |
| Unsafe API consumption | Resposta de fornecedor externo é confiada como entrada validada. | Verificar assinatura quando disponível, validar schema e tratar como não confiável. |
| GraphQL deep query | Consulta profundamente aninhada exige trabalho desproporcional. | Depth, complexity e timeout por operação. |
| GraphQL alias/fragment abuse | Aliases/fragments multiplicam resoluções e podem contornar limites ingênuos. | Custo do plano executado, limites de alias e análise de AST. |
| GraphQL batching abuse | Múltiplas operações em uma requisição contornam limites por request. | Quotas por operação e por identidade, batching limitado. |
| GraphQL introspection exposure | Schema revela superfície de ataque sem necessidade operacional. | Política consciente de introspection; controle de auth e ambientes. |
| GraphQL field-level authorization | Campo sensível é consultado sem validação no resolver. | Política por campo e objeto, testes de roles e tenants. |
| gRPC authorization gaps | Métodos internos são invocados sem autenticação/autorização. | Interceptors, mTLS conforme arquitetura e policy em cada serviço. |
| gRPC metadata trust | Metadata de cliente é usada como identidade sem validação. | Garantir identidade criptograficamente verificável e confiar apenas em proxy autorizado. |
| WebSocket cross-site hijacking | Conexão com cookie é iniciada de origem indevida. | Validar `Origin`, autenticação e CSRF contextual para handshake. |
| WebSocket message authorization | Auth na abertura não é reavaliada para mensagens/objetos. | Autorizar ação por mensagem, tenant e objeto. |
| WebSocket flood | Conexões persistentes, frames ou mensagens excedem recursos. | Limites de conexão/frame, heartbeats, quotas e backpressure. |
| Webhook spoofing | Serviço aceita callback sem verificar remetente/integridade. | Assinatura HMAC/assimétrica, comparação constante e segredos rotativos. |
| Webhook replay | Evento legítimo é reenviado e processado mais de uma vez. | Identificador de evento, timestamp, tolerância temporal e idempotência. |
| Webhook SSRF | Destino fornecido por cliente alcança rede interna. | Destinos permitidos, egress proxy, DNS/IP e limites de protocolo. |
| API key scope overreach | Uma chave concede acesso amplo a vários recursos/tenants. | Escopos curtos, restrições por operação, rotação e logs de uso. |
| API pagination scraping | Paginação ilimitada permite extração massiva. | Limites, autorização, quotas por custo e detecção de coleta anômala. |
| Unsafe content-type parsing | Requisições ambíguas passam por parser diferente do esperado. | Aceitar content-types explícitos, limites de corpo e rejeição de ambiguidades. |
| API trust of `X-Forwarded-For` | Cliente forja IP e contorna rate limit/geoblocking. | Configurar proxies confiáveis e extrair IP apenas da cadeia validada. |
| API enumeration / predictable IDs | IDs incrementais facilitam descoberta, embora não sejam causa de acesso indevido por si. | Autorização real, rate limiting e IDs opacos quando úteis. |
| ETag/conditional request leakage | Metadados de cache/revalidação revelam estado de outro usuário. | Variação por identidade/tenant, `Cache-Control` adequado e testes de cache. |
| API request replay after network retry | Retentativas duplicam criação, cobrança ou alteração. | Idempotency keys por operação, transações e consistência de fila. |

### 5.6 Lógica de negócio, automação abusiva e fraude

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Workflow bypass | Usuário salta etapas obrigatórias de aprovação ou confirmação. | State machine server-side e invariantes nas transições. |
| Price manipulation | Cliente altera preço, frete, desconto ou quantidade arbitrariamente. | Preço calculado no servidor e verificação final na transação. |
| Coupon stacking | Combinações indevidas de promoções resultam em prejuízo. | Regras atômicas de elegibilidade, limite por usuário/pedido e testes concorrentes. |
| Voucher/token enumeration | Códigos previsíveis podem ser descobertos em massa. | Entropia adequada, limites de tentativas, auditoria e validade. |
| Double spending | Valor ou crédito é gasto em duas operações concorrentes. | Lock transacional, invariantes de saldo, ledger e idempotência. |
| Race condition em estoque | Requisições simultâneas reservam mais do que disponível. | Operações atômicas, locks/constraints no banco e fila apropriada. |
| TOCTOU no checkout | Preço, permissão ou estoque muda após validação inicial. | Revalidação em transação final e versões de objeto. |
| Refund fraud | Fluxo de estorno permite duplicidade ou destinatário incorreto. | Vincular reembolso à transação original e reconciliar com provedor. |
| Payment callback spoofing | Endpoint toma como verdadeiro pagamento declarado pelo cliente. | Verificar evento assinado/status diretamente com provedor, idempotência. |
| Payment webhook replay | Notificação repetida gera créditos ou liberação de serviço duplicada. | Deduplicação por ID, event store e transação idempotente. |
| Insecure payment status trust | Frontend define compra como paga após redirect. | Confirmar estado em fonte oficial no backend. |
| Subscription bypass | Cancelamento, expiração ou trial não revoga direitos no servidor. | Entitlement verificado server-side e eventos consistentes. |
| Free trial abuse | Criação massiva de contas contorna limites por usuário. | Anti-abuso proporcional, verificação de identidade contextual e controle de dispositivos. |
| Carding | Tentativas automatizadas verificam cartões/credenciais de pagamento. | Provedor compatível, controles antifraude, limites e observabilidade sem guardar dados sensíveis. |
| Card cracking | Tentativas de adivinhar atributos de cartões por respostas diferenciadas. | Respostas uniformes, antifraude e bloqueio adaptativo. |
| Scalping | Bots capturam estoque/ingressos de disponibilidade limitada. | Filas justas, quotas por comprador, antifraude e controles de reserva. |
| Inventory denial | Bots prendem estoques em carrinhos sem comprar. | Reserva com TTL, limites por usuário e recuperação automática. |
| Scraping massivo | Coleta automatizada amplia exposição/custo de dados. | Auth, quotas, paginação, rate limit por custo e monitoramento. |
| Account creation abuse | Contas artificiais viabilizam spam, fraude ou consumo de bônus. | Controles de risco, verificação, rate limit e prevenção de abuso. |
| Fake reviews/ratings | Usuários ou bots manipulam reputação e ranking. | Detecção comportamental, moderação e limites de avaliações. |
| Referral abuse | Referências artificiais geram benefícios indevidos. | Identificar autopatrocínio, loops, vínculos e pagamento de incentivo verificado. |
| Search/ranking manipulation | Volume artificial distorce recomendação, busca ou métricas. | Sinais antifraude, separação de métricas e auditoria. |
| Marketplace account takeover | Conta legítima é usada para desviar saque ou alterar recebedor. | Passkey/MFA, step-up em mudanças financeiras e janela de análise. |
| Data export abuse | Usuário legítimo aciona exportações em massa além do necessário. | Quotas, justificativas, aprovação e detecção de padrões atípicos. |
| Time-of-check business logic flaw | Elegibilidade é verificada sob estado antigo e aplicada posteriormente. | Checagem final autoritativa na mesma transação. |

### 5.7 Criptografia, dados e exposição de informações

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Plaintext credentials | Credenciais ficam em texto claro em banco, código ou backup. | Hash apropriado para senha, secret manager, secrets scanning e rotação. |
| Weak password hashing | MD5/SHA rápido permite tentativa offline eficiente após vazamento. | Argon2id/scrypt ou equivalente aprovado com parâmetros atualizados. |
| Hardcoded cryptographic key | Chave é publicada em código, pacote ou binário cliente. | Gerenciar segredos externamente e rotacionar material exposto. |
| Insufficient entropy | Tokens, nonces ou chaves gerados de fonte previsível. | CSPRNG da plataforma e revisão de inicialização/entropia. |
| Nonce/IV reuse | Reutilização incorreta compromete confidencialidade/integridade de cifras específicas. | Geração e unicidade por chave, bibliotecas AEAD corretas. |
| ECB mode information leakage | Blocos iguais de dados produzem padrões reconhecíveis. | Usar modos autenticados modernos, não ECB para dados confidenciais. |
| CBC padding oracle | Erros/timing de padding revelam informações em sistemas vulneráveis. | AEAD, rejeição uniforme e remoção de protocolos legados frágeis. |
| Cryptographic downgrade | Compatibilidade permite aceitar protocolo ou algoritmo vulnerável. | Política de algoritmos permitidos, versões mínimas e negociação segura. |
| Weak RSA/ECC parameters | Tamanho, curva ou implementação inadequados enfraquecem assinaturas/segredo. | Parâmetros atuais reconhecidos, bibliotecas revisadas, KMS. |
| Signature validation bypass | Aplicação não valida assinatura ou aceita chave fornecida pelo atacante. | Verificação completa da cadeia de confiança, algoritmo, finalidade e contexto. |
| Certificate expiry/outage | Expiração de certificado interrompe comunicação ou incentiva bypass inseguro. | Renovação automatizada, alertas e testes de falha segura. |
| Improper TLS validation | Serviço aceita hostname ou CA indevida. | Verificação completa de TLS, testes de certificado inválido. |
| Timing side channel | Diferença de tempo revela token, segredo ou estado. | Comparações apropriadas, respostas consistentes e análise contextual. |
| Compression side channel | Compressão de dados secretos com entradas controladas pode revelar padrões. | Evitar mistura de segredo e entrada atacante em compressão observável. |
| Secret in URL | Tokens aparecem em logs, histórico, Referer e ferramentas intermediárias. | Usar cabeçalhos/canais adequados, `no-store` e redação de logs. |
| Secret in build artifacts | `.env`, source maps ou cache de pipeline vazam credenciais. | Regras de empacotamento, scanners e controle de acesso a artefatos. |
| Public database exposure | Banco ou dump é acessível pela Internet ou bucket público. | Rede privada, IAM mínimo, autenticação e scanning de exposição. |
| Backup exposure | Cópias não criptografadas ou públicas revelam dados históricos. | Criptografia, backup imutável, ACL restrita e inventário. |
| Data remanence | Dados permanecem em mídia, snapshots ou objetos antigos após descarte. | Lifecycle, destruição criptográfica quando aplicável e política de retenção. |
| Cross-tenant leakage | Consulta, cache, fila ou storage retorna informação de outro tenant. | Escopo de dados, RLS, isolamento de chaves de cache e testes cruzados. |
| Sensitive debug logs | Exceções e logs contêm senha, CPF, tokens ou dados financeiros. | Redaction, logging schema e inspeção de ambientes produtivos. |
| Excessive data retention | Informações antigas permanecem sem finalidade ou controle. | Classificação, retenção por finalidade e exclusão programada. |
| Misconfigured object storage | Bucket permite leitura, listagem ou escrita pública indevida. | Block public access, políticas mínimas e auditoria contínua. |
| Insecure presigned URL | URL assinada dura demais, concede escopo excessivo ou é exposta. | Prazo curto conforme operação, escopo restrito e rastreamento. |
| API error disclosure | Mensagem de exceção retorna consulta SQL, paths ou stack trace. | Resposta pública genérica e observabilidade protegida. |
| Data poisoning through ingestion | Fonte externa contamina dados usados em decisões/relatórios. | Proveniência, validação, trilha de alteração e revisão de integridade. |
| Integrity check omitted | Artefato ou dado crítico é processado sem verificação de origem. | Assinatura/MAC ou checksum de fonte confiável conforme caso. |

### 5.8 Redes, transporte, DNS e disponibilidade (DoS/DDoS)

**Diferença importante:** DoS tenta tornar serviço indisponível; DDoS distribui origens ou recursos do ataque. Ataques volumétricos de rede **não são resolvidos somente com rate limiting no código**, pois podem saturar links e infraestrutura antes de alcançar a aplicação. Proteção exige camadas complementares, capacidade upstream e coordenação operacional.

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Volumetric DDoS | Alto volume de tráfego satura link, backbone, edge ou origem. | Mitigação upstream/Anycast/CDN, scrubbing, runbook e monitoramento. |
| UDP flood | Tráfego UDP excessivo consome capacidade de transporte ou processamento. | Filtragem upstream, ACL e mitigação L3/L4 no provedor. |
| TCP SYN flood | Excesso de handshakes incompletos consome estados de conexão. | SYN cookies, proteção L4, tuning e mitigação upstream. |
| TCP connection exhaustion | Conexões numerosas ou persistentes esgotam descritores e workers. | Limits por origem, backlog, timeouts e balanceamento. |
| ICMP flood | ICMP em volume elevado consome banda ou CPU. | Políticas ICMP adequadas e mitigação upstream, sem bloquear diagnóstico indiscriminadamente. |
| DNS amplification/reflection | Respostas DNS maiores que consultas refletem tráfego à vítima. | Proteção DDoS, BCP38/anti-spoofing e evitar recursão aberta. |
| NTP amplification | Serviço NTP mal configurado é usado para reflexão/amplificação. | Desativar funções abusáveis, atualização, restrições e anti-spoofing. |
| Memcached amplification | Instância UDP exposta é abusada como amplificador. | Bloquear UDP público, isolar serviço e atualizar software. |
| SSDP/CLDAP amplification | Protocolos de descoberta/diretório são usados como refletores. | Restringir exposição, filtrar tráfego e mitigação na borda. |
| HTTP GET/POST flood | Volume de requisições esgota aplicação, cache ou banco. | WAF/WAAP, cache, rate limits por custo, quotas e autoscaling com orçamento. |
| Slowloris / slow HTTP | Conexões enviam dados lentamente e prendem recursos. | Timeout de leitura, tamanho de cabeçalho, limites de conexão e proxy robusto. |
| Slow POST/body trickle | Upload extremamente lento ocupa sockets/workers. | Timeout por taxa mínima, limites de body e controle de conexões. |
| TLS handshake flood | Excesso de handshakes provoca custo criptográfico. | Edge TLS offload, limites, mitigação L4/L7 e capacidade. |
| HTTP/2 stream exhaustion | Exploração de streams ou resets causa carga desproporcional. | Proxies corrigidos, limites de streams e recursos, mitigação edge. |
| HTTP/3 QUIC flood | Tráfego e estados QUIC em volume excedem capacidade do serviço. | Edge atualizado, quotas de conexão e mitigação no provedor. |
| DNS query flood | Consultas massivas degradam DNS autoritativo. | Anycast DNS, proteção especializada, redundância e monitoramento. |
| DNS random-subdomain attack | Consultas a subdomínios inexistentes forçam lookups excessivos. | Proteção DNS, cache negativo e controles de autoridade. |
| NXDOMAIN flood | Respostas negativas em massa pressionam resolutores e DNS. | Filtragem, cache negativo e capacidade resiliente. |
| Application expensive-query DoS | Busca, relatório ou ordenação pesada causa consumo extremo. | Índices, timeout, paginação, orçamento por consulta e quotas. |
| Regex DoS | Padrão regex gera backtracking de custo elevado. | Revisão das regex, engine adequada e limites de input/CPU. |
| Decompression bomb DoS | Arquivo compactado consome espaço/memória desproporcional. | Limits de descompressão, sandbox e tempo máximo. |
| JSON/XML depth bomb | Estrutura recursiva sobrecarrega parser ou memória. | Limites de profundidade e tamanho, parsers seguros. |
| Queue flooding | Mensagens acima da capacidade acumulam backlog e atrasam serviços. | Quotas, backpressure, DLQ, prioridade e métricas. |
| Log flooding | Eventos excessivos esgotam disco/ingestão e ocultam incidentes. | Limites, particionamento, retenção e alertas de volume. |
| Cache bypass flood | Requisições variáveis impedem cache e atingem origem. | Normalização, cache keys, políticas edge e proteção de origin. |
| Origin IP discovery | Ataque ignora CDN e acessa IP real do origin. | Firewall permitindo somente proxy legítimo, inventário e proteção DNS. |
| Botnet distributed low-rate attack | Tráfego baixo por IP, alto no agregado, contorna limites simples. | Detecção comportamental, identidade, reputação e regras por custo. |
| Carpet-bombing DDoS | Tráfego espalhado por muitos IPs do mesmo prefixo dificulta detecção local. | Defesa de provedor, visibilidade em prefixo e planejamento de roteamento. |
| Application-layer amplification | Uma requisição desencadeia centenas de operações no backend. | Budget de fan-out, limites de dependências, cache e circuit breaker. |
| Retry storm | Retentativas simultâneas ampliam uma falha transitória. | Exponential backoff com jitter, idempotência, circuit breaker. |
| Thundering herd | Muitos clientes recomputam mesmo dado após expiração simultânea. | Cache jitter, stale-while-revalidate, single-flight. |
| Resource starvation | Uma carga monopoliza CPU, memória, conexões ou threads. | Isolamento de pools, quotas por tenant e prioridades. |
| DNS spoofing/cache poisoning | Respostas DNS fraudulentas direcionam tráfego a destino incorreto. | DNSSEC quando aplicável, resolvers confiáveis e proteção operacional. |
| ARP spoofing | Ator em rede local altera resolução IP/MAC para interceptação. | Segmentação, DAI, segurança de switch, criptografia ponta a ponta. |
| Man-in-the-middle (MITM) | Ator intermediário intercepta/modifica comunicação sem validação adequada. | TLS válido, autenticação de pares e segmentação. |
| BGP hijack / route leak | Anúncio incorreto ou malicioso redireciona ou interrompe rotas IP. | RPKI/ROA, monitoramento BGP e coordenação com operadoras. |
| DHCP spoofing | Servidor falso entrega gateway/DNS malicioso em rede local. | DHCP snooping, NAC e segmentação. |
| Rogue Wi-Fi / evil twin | Rede sem fio falsa captura ou redireciona tráfego. | WPA3/802.1X, validação de certificado e educação. |
| DNS tunneling | DNS é usado como canal encoberto de comunicação/exfiltração. | Egress DNS controlado, detecção de padrões e listas aprovadas. |
| Network scanning/reconnaissance | Serviços expostos e versões são enumerados para identificar oportunidades. | Minimizar superfície, firewall, inventário e logs de sondagem. |
| IP spoofing | Origem de pacote/cabeçalho é falsificada para abuso ou bypass. | BCP38, validação de proxy e não confiar em headers do cliente. |
| Port/service exposure | Administração e bancos acessíveis à Internet aumentam risco. | Private networking, ACL, VPN/ZTNA, autenticação e patching. |
| VPN credential compromise | Acesso remoto com credencial roubada permite intrusão. | MFA FIDO2, postura de dispositivo, restrições, logs e revogação. |
| DNS rebinding against local services | Domínio controlado passa a resolver para serviços internos do browser/backend. | Host/origin validation, egress e bloqueio de endereços internos. |

### 5.9 Cloud, infraestrutura, sistema operacional e diretórios

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Public cloud storage exposure | Bucket ou arquivo privado é compartilhado publicamente. | Block public access, IAM e scanning contínuo. |
| Cloud IAM privilege escalation | Políticas permitem criar roles, anexar permissões ou assumir papel amplo. | IAM mínimo, deny guardrails, SCP/organização e revisão de caminhos de escalada. |
| Overly broad trust policy | Identidades externas podem assumir roles sem restrições suficientes. | Restringir principal, condições de audiência, subject e origem. |
| Cloud credential theft | Keys long-lived são vazadas e usadas por terceiro. | OIDC/workload identity, credenciais efêmeras, secrets scanning e rotação. |
| Metadata token theft | SSRF ou processo local acessa credenciais do metadata service. | IMDSv2 quando aplicável, isolamento, egress e roles mínimas. |
| Exposed management console | Interfaces de cloud/hipervisor ficam públicas ou sem MFA. | SSO forte, MFA FIDO2, IP/ZTNA, auditoria. |
| Security group misconfiguration | Porta administrativa/DB é aberta para `0.0.0.0/0` sem necessidade. | Regras mínimas, IaC scanning e verificações em runtime. |
| Cloud logging disabled | Eventos maliciosos não são rastreáveis por falta de trilhas. | Auditar configuração central, retenção protegida e alertas de desativação. |
| Snapshot/data volume theft | Snapshots e discos são compartilhados sem autorização. | Controle de ACL/compartilhamento, criptografia e auditoria. |
| Serverless function abuse | Função exposta ou com IAM elevado executa ações indevidas. | Auth, limite de invocação, IAM mínimo e egress controls. |
| Serverless event injection | Eventos não confiáveis acionam lógica privilegiada. | Schema, autenticidade do evento, deduplicação e mínimo privilégio. |
| Cloud cost exhaustion | Recursos sob demanda geram despesa enorme por abuso. | Budgets, quotas, alertas e rate limit de operações custosas. |
| Cross-account confused deputy | Serviço assume acesso a conta errada por relação de confiança ampla. | Condições como external ID/subject e escopos apropriados ao fornecedor. |
| Instance/VM escape | Falha de hipervisor permite escapar isolamento da instância. | Patch de hypervisor, isolamento e estratégia de blast radius. |
| Privilege escalation via sudo | Sudoers, binários ou serviços permitem subir privilégios. | Hardening, sudo mínimo, patch e revisão de permissões. |
| SUID/SGID abuse | Binários privilegiados inseguros são usados para elevar direitos. | Revisão de SUID, patching, montagens `nosuid` onde viável. |
| Writable service executable | Conta não privilegiada altera binário iniciado com maior privilégio. | ACL e propriedade corretas, EDR e revisão de serviços. |
| Unquoted service path | Caminho de execução ambíguo pode iniciar binário não autorizado. | Configuração correta, hardening de serviços e ACL. |
| DLL search order hijacking | Dependência dinâmica é carregada de diretório controlado. | Paths absolutos, assinaturas, ACL e carga segura de bibliotecas. |
| PATH hijacking | Executável de diretório não confiável substitui ferramenta esperada. | Paths absolutos e ambiente sanitizado. |
| Cron/systemd persistence | Agendadores ou serviços são usados para execução persistente. | Auditoria de tarefas, ACL, EDR e monitoramento de mudanças. |
| SSH key theft | Chaves privadas expostas permitem acesso remoto. | Agentes protegidos, passphrases, rotação e controle de acessos. |
| Default credentials | Appliance/serviço mantém credenciais de fábrica. | Credenciais únicas, desabilitar padrão e inventário. |
| Exposed admin dashboards | Dashboards internos ficam acessíveis sem controle forte. | ZTNA/VPN, SSO, MFA, autorização e inventário. |
| Patch management gap | Serviço vulnerável permanece exposto após correção do fornecedor. | Inventário, patch SLO, KEV-first e controles compensatórios. |
| End-of-life components | Software sem suporte acumula falhas sem correção. | Substituição planejada e isolamento temporário rigoroso. |
| Directory/AD password attack | Senhas fracas ou expostas possibilitam comprometimento de domínio. | MFA, hardening AD, contas privilegiadas separadas e monitoramento. |
| Kerberoasting | Tickets de serviço podem permitir tentativas offline contra senhas fracas. | Senhas longas/gerenciadas, gMSA, privilégios mínimos, monitoramento. |
| AS-REP roasting | Contas com pré-autenticação desativada expõem material a ataque offline. | Habilitar preauth, senhas fortes, auditoria do AD. |
| Pass-the-hash | Hash roubado é usado como credencial em protocolos vulneráveis. | Credential Guard, reduzir NTLM, segmentação e isolamento de administradores. |
| Pass-the-ticket | Tickets Kerberos roubados são reutilizados para acessar serviços. | Proteção de credenciais, expiração, EDR e Kerberos hardening. |
| NTLM relay | Credenciais de desafio-resposta são encaminhadas a serviços sem proteção adequada. | SMB signing, EPA, bloquear NTLM onde possível, segmentação. |
| Lateral movement through RDP/SMB | Conta comprometida alcança outros hosts e eleva impacto. | Segmentação, MFA/JIT, PAM, EDR e redução de serviços. |
| Persistence via identity provider | Ator malicioso cria credenciais, app registrations ou grants persistentes. | Auditoria IAM/IdP, revisões de consentimentos e alertas de criação. |
| SaaS OAuth token compromise | Token com permissões amplas permite exportar dados de SaaS. | App governance, DLP, scope mínimo, monitoramento e revogação. |
| Cloud object version manipulation | Versionamento/backups são alterados para ocultar ou destruir dados. | Imutabilidade, MFA-delete quando pertinente, least privilege. |
| Remote management abuse | Ferramentas legítimas de administração são usadas por invasor. | Allowlist de software, auditoria de sessões e controles JIT. |

### 5.10 Containers, Kubernetes, service mesh e ambientes de execução

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Container running as root | Processo privilegiado amplia impacto de falhas da aplicação. | Non-root, `runAsNonRoot`, usuário dedicado e capability drop. |
| Privileged container | Pod/container com privilégios excessivos pode alcançar host. | Proibir privileged, usar Pod Security e admission policies. |
| Docker socket exposure | Processo com acesso ao socket Docker pode controlar hosts/containers. | Não montar socket em workload não confiável; isolamento. |
| HostPath mount abuse | Montagem de diretórios críticos do host rompe isolamento. | Restringir volumes, validar paths e admission controls. |
| Container escape | Falha de kernel/runtime permite acesso fora do container. | Atualização, sandbox, seccomp, LSM e mínimo privilégio. |
| Kubernetes RBAC wildcard | Service account possui verbos/recursos amplos demais. | RBAC mínimo, revisar `*`, namespaces e impersonation. |
| Service account token exposure | Token montado em pod sem necessidade é extraído. | `automountServiceAccountToken: false` quando possível; tokens projetados. |
| Kubernetes API public exposure | API server ou etcd expostos facilitam acesso indevido. | Endpoints privados, controle de rede, autenticação e auditoria. |
| Etcd data disclosure | Segredos/dados de cluster acessíveis por configuração inadequada. | Criptografia em repouso, ACL e proteção da rede de controle. |
| Kubernetes secret misuse | Secrets em manifestos/Git/logs tornam credenciais recuperáveis. | Secret manager, criptografia, RBAC e rotação. |
| Namespace trust confusion | Namespace é tratado como fronteira de segurança suficiente. | NetworkPolicy, RBAC, admission, policies e isolamento de workloads. |
| Missing NetworkPolicy | Todos os pods podem comunicar-se desnecessariamente. | Default-deny ingress/egress e políticas específicas. |
| Malicious admission controller | Webhook de admissão comprometido pode alterar workloads. | Proteger webhook, certificado, revisões e privilégio mínimo. |
| Image tag mutability | Imagem `latest` muda sem revisão e executa código inesperado. | Pin por digest, assinatura e processo de promoção. |
| Vulnerable base image | Biblioteca ou sistema antigo contém CVE explorável. | Base mínima, patch automatizado e scanning contínuo. |
| Build secret leakage | Secrets acabam em layer, histórico ou cache de imagem. | BuildKit secrets, multi-stage, inspeção de layers e rotação. |
| Insecure container registry | Imagens podem ser substituídas ou publicadas por atores indevidos. | IAM, assinatura, namespaces de publicação e trilha de auditoria. |
| Pod resource exhaustion | Containers sem limites podem prejudicar outros tenants. | Requests/limits, quotas, prioridades e nós isolados. |
| Sidecar/service-mesh trust gaps | Identidade mTLS existe, mas autorização por método/recurso é ausente. | AuthZ explícita por serviço, mTLS e policy testing. |
| Insecure debug/exec endpoint | Ferramenta de debug permite shell em ambiente sensível. | Proteger acesso, desabilitar em produção e monitorar invocações. |
| Insecure CRD/operator | Controlador aceita configurações que resultam em ação privilegiada. | Validação de CRD, RBAC mínimo, admissão e revisão do operador. |
| CI runner inside cluster compromise | Runner de build comprometido obtém service accounts/segredos do cluster. | Isolamento de runners, identidades distintas e deploy controlado. |
| Multi-tenant cluster breakout | Um tenant obtém recursos de outro por RBAC, rede ou configuração. | Isolamento forte por conta/cluster quando risco exige, controles por camada. |

### 5.11 Supply chain, Git, dependências e CI/CD

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Dependency confusion | Registry resolve pacote externo com nome interno e executa código não confiável. | Namespace privado, configurações de registry e políticas de resolução. |
| Typosquatting de pacote | Pacote com nome semelhante a dependência legítima contém código malicioso. | Revisão de dependência, reputação, lockfile e registry aprovado. |
| Malicious maintainer/update | Nova versão de pacote confiável adiciona código nocivo. | SCA, release review, pinning e monitoramento de proveniência. |
| Transitive dependency compromise | Dependência indireta traz vulnerabilidade ou comportamento malicioso. | SBOM, análise transitiva e atualização controlada. |
| Package install-script abuse | Script de instalação executa ações inesperadas durante build. | Restringir scripts, sandbox de build e revisão de pacotes. |
| Compromised package registry | Artefato baixado não corresponde à versão confiável esperada. | Hash/assinatura, mirror confiável e provenance. |
| Source repository takeover | Conta/token comprometido modifica código ou releases. | MFA FIDO2, branch protection, revisão e signing. |
| Compromised CI/CD token | Token de pipeline permite publicar ou acessar produção. | OIDC de curta duração, escopos mínimos e ambiente isolado. |
| Poisoned pipeline execution | PR/workflow não confiável executa no contexto com secrets. | Separar contextos, restrição de eventos e revisão de workflows. |
| Workflow trigger abuse | Trigger permissivo usa privilégio de branch confiável com conteúdo externo. | Revisar triggers, permissions e handling de artefatos de PR. |
| Artifact replacement | Binário/build é alterado após validação ou antes de deploy. | Assinatura e verificação end-to-end, armazenamento imutável. |
| Build provenance forgery | Attestation não confiável declara origem falsa do artefato. | Verificar identidade do builder e assinatura, política SLSA. |
| Release signing key theft | Chave comprometida permite assinar distribuição maliciosa. | HSM/KMS, acesso JIT, rotação e revogação. |
| Insufficient branch protection | Commit entra em produção sem revisão, teste ou autorização. | Required checks, CODEOWNERS e proteção contra force push. |
| Malicious pull request | Contribuição altera lógica ou execução de CI de modo adverso. | Sandbox, revisão independente, testes e política de contributors. |
| Leaked `.env` in Git | Arquivo de segredo no histórico permanece recuperável mesmo após remoção no último commit. | Revogação, varredura de histórico e rewrite coordenado quando adequado. |
| Exposed Git metadata | Diretório `.git` publicado revela histórico, código e secrets. | Não servir metadados, deployment artifact allowlist e testes de exposição. |
| Compromised IaC module | Módulo Terraform ou Helm altera permissões ou cria recursos indevidos. | Pinning, revisão, assinatura, testes de plano e origin confiável. |
| Compromised GitHub Action | Action de terceiros executa código com credenciais do pipeline. | Fixar commit SHA, permissões mínimas e revisão de mudanças. |
| Secrets in CI logs | Debug de pipeline publica credenciais e tokens de nuvem. | Redaction, política de logs, evitar `set -x` e revisão. |
| Insecure self-hosted runner | Runner persiste material secreto entre jobs ou PRs não confiáveis. | Runner efêmero, isolado e sem secrets de produção em jobs externos. |
| Source code exfiltration via integration | Serviço de terceiros recebe repositório inteiro sem necessidade. | Escopos mínimos, controles de app, revisões e contrato de dados. |
| Vulnerable dependency not patched | CVE conhecido continua em produção após correção disponível. | SCA contínua, SBOM, prioridades KEV e patch SLO. |
| License/provenance blind spot | Dependências sem origem identificada dificultam resposta a falhas. | SBOM completo, metadados de fornecedor e processo de aprovação. |
| CI/CD log tampering | Logs de pipeline podem ser apagados ou modificados por mesmo ator. | Exportação imutável, segregação de auditoria e alertas. |

### 5.12 Endpoints, malware, persistência e operações adversárias

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Trojan | Software aparentemente legítimo inclui função maliciosa. | Origem confiável, assinaturas, EDR e controle de execução. |
| Ransomware | Arquivos são cifrados/indisponibilizados para extorsão. | Segmentação, MFA, EDR, patching e backups testados/imutáveis. |
| Data-wiping malware | Código destrói dados/sistemas sem objetivo de resgate. | Backups, controles de execução, isolamento e monitoramento. |
| Spyware / infostealer | Malware coleta credenciais, cookies e documentos. | EDR, atualização, proteção do navegador e revogação de sessões. |
| Keylogger | Entrada de teclado é interceptada por software ou hardware comprometido. | Hardening de endpoint, EDR, FIDO2 e integridade física. |
| Rootkit | Malware modifica camadas do sistema para ocultar atividade. | Secure Boot, atualização, EDR e verificações de integridade. |
| Bootkit / firmware compromise | Persistência abaixo do sistema operacional escapa verificações comuns. | Firmware assinado, Secure Boot, atualizações e validação de cadeia. |
| Fileless malware | Execução abusiva de ferramentas legítimas evita artefatos tradicionais. | EDR comportamental, logging de scripts e regras de execução. |
| Living-off-the-land | Ferramentas administrativas nativas são usadas para execução e coleta. | Restringir uso, logging, monitoramento de comportamento e JIT. |
| Macro/document malware | Arquivo recebido induz execução de código em leitor/office. | Desabilitar macros não confiáveis, sandbox e educação. |
| Browser compromise | Vulnerabilidade do navegador executa código ou rouba sessão. | Atualização, isolation, política de extensões e proteção de endpoint. |
| Privilege escalation exploit | Falha local amplia privilégio de usuário ou serviço. | Patching, proteção do kernel, menor privilégio e EDR. |
| Persistence via scheduled tasks | Tarefa agendada mantém execução não autorizada. | Controle de mudanças, ACL, EDR e inventário de jobs. |
| Web shell persistence | Arquivo malicioso no servidor web oferece execução remota. | Bloquear upload executável, integridade do webroot e detecção. |
| Command and control (C2) | Host comprometido se comunica com controle remoto. | DNS/egress monitoring, EDR, segmentação e listas de destino. |
| Lateral movement | Comprometimento inicial alcança outros hosts/sistemas. | Segmentação, credenciais únicas, MFA e monitoramento. |
| Credential dumping | Segredos são extraídos de memória, disco ou stores do sistema. | Credencial isolation, EDR, hardening e contas de privilégio mínimo. |
| Data staging | Dados são agregados em local intermediário antes de exfiltração. | DLP, monitoramento de arquivos/volumes e correlação de eventos. |
| Exfiltration over HTTPS | Dados saem por conexão web aparentemente legítima. | Egress policy, DLP, anomalia de volume e classificação dos dados. |
| Exfiltration over DNS | Dados são codificados em consultas DNS. | DNS logging central, restrição de resolvers e detecção de padrões. |
| Exfiltration to cloud storage | Conta externa recebe dados empresariais através de serviço comum. | CASB/DLP, allowlists e alertas sobre exportação. |
| Defense evasion / log clearing | Ator altera logs ou desliga agentes após comprometimento. | Logs remotos imutáveis, proteção anti-tamper, alertas. |
| Security tooling impairment | Ferramentas de defesa são desabilitadas ou mal configuradas. | Proteção de políticas, saúde de agentes, separação de privilégios. |
| Destructive command execution | Comandos de alto impacto são rodados após ganhar shell. | Limitar shell, políticas de execução, backups e segregação. |
| Cryptojacking | Recursos computacionais são desviados para mineração não autorizada. | Detecção de consumo anormal, quotas e proteção de workloads. |

### 5.13 Comunicação, e-mail, engenharia social e identidade organizacional

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Phishing | Mensagem simula entidade confiável para obter credenciais ou induzir ação. | MFA resistente a phishing, treinamento contextual e filtros de e-mail. |
| Spear phishing | Mensagem personalizada usa dados específicos da vítima. | Proteção de contas, verificação por segundo canal e exercícios de conscientização. |
| Whaling | Mensagem mira executivos ou responsáveis por pagamentos. | Dupla aprovação, verificação fora de banda e controles de financeiro. |
| Business Email Compromise (BEC) | Conta/domínio falsificado induz pagamento ou vazamento. | DMARC/SPF/DKIM, confirmação de alteração bancária e MFA. |
| Domain spoofing | E-mail ou site apresenta domínio visualmente semelhante. | Proteção DNS/e-mail, monitoramento de domínios e verificação de origem. |
| Homograph / IDN attack | Caracteres Unicode confundem visualmente nomes de domínio. | Verificar domínio canônico, alertas de lookalike e segurança no browser. |
| Email account takeover | Comprometimento de caixa postal expõe resets, contratos e mensagens. | MFA FIDO2, sessões gerenciadas, regras de forwarding auditadas. |
| Malicious forwarding rule | Regra criada pelo invasor encaminha e-mails silenciosamente. | Alertar criação de regra, auditar mailbox e revogar tokens. |
| QR phishing (quishing) | Código QR leva a site de login/ação fraudulenta. | Verificar destino, conscientização e proteção de navegação. |
| SMS phishing (smishing) | Mensagem em celular induz abertura de link ou contato fraudulento. | Treinamento, autenticação forte e confirmação de canais oficiais. |
| Voice phishing (vishing) | Ligação usa urgência ou falsa autoridade para obter credenciais. | Procedimento de validação por canal confiável e proibição de compartilhar OTP. |
| Deepfake voice/video fraud | Áudio/vídeo sintético simula pessoa autorizadora de transação. | Verificação multifatorial de processos, retorno via contato conhecido e duplo controle. |
| Helpdesk impersonation | Ator se passa por suporte ou usuário para redefinir MFA/senha. | Script de validação forte, auditoria e supervisão de exceções. |
| Pretexting | História fabricada induz acesso ou compartilhamento de dados. | Princípio need-to-know, confirmação de identidade e registro de solicitações. |
| Baiting / malicious removable media | Mídia/arquivo atraente induz execução de malware. | Controle de USB, EDR e política de execução. |
| Watering-hole compromise | Site frequentemente visitado pela organização é comprometido. | Proteção de navegador, patching e filtro de navegação. |
| Malvertising | Anúncio apresenta conteúdo ou link malicioso. | Navegação protegida, filtros e atualizações. |
| OAuth app phishing | App malicioso obtém consentimento amplo sem roubar senha. | Controles de OAuth grants, revisão de apps e restrição de scopes. |
| Search engine poisoning | Resultado de busca fraudulento direciona a download/login malicioso. | URLs oficiais, proteção endpoint e validação de assinaturas de software. |
| Fraudulent support contact | Falso canal de suporte solicita acesso remoto ou pagamento. | Diretório oficial de suporte, treinamento e confirmação por segundo canal. |
| Conversation spoofing | Mensagem é inserida em thread legítima ou simula interlocutor. | Verificação de remetente, autenticidade e processos para pedidos sensíveis. |
| Social engineering via collaboration tools | Chat corporativo é usado para solicitar token, código ou ação de alto risco. | MFA, política de approval e orientação de verificação. |
| Physical tailgating | Pessoa sem autorização entra em área restrita seguindo usuário. | Controle de acesso físico e treinamento. |

### 5.14 Aplicações mobile, desktop e dispositivos clientes

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Mobile insecure storage | Tokens e PII ficam em arquivos/Preferences sem proteção. | Keychain/Keystore, minimização e política de backup. |
| Mobile hardcoded secret | Chave de API privada é incorporada ao APK/IPA e extraível. | Evitar segredo privado no cliente, proxy backend e controle de escopos. |
| Mobile certificate validation bypass | App aceita TLS inválido ou ignora hostname. | Trust management correto e testes de falha segura. |
| Insecure deep links | Links internos permitem abrir funções ou parâmetros privilegiados. | Validar origem/destino, estado e autorização server-side. |
| Android exported component abuse | Activity/receiver/service exportado aceita chamadas sem proteção. | `exported=false` por padrão e permissões explícitas. |
| iOS URL scheme hijacking | Scheme customizado pode ser registrado por app adversário. | Universal Links/Associated Domains e validação do fluxo. |
| WebView JS bridge abuse | Página não confiável acessa bridge com recursos privilegiados. | Limitar conteúdo, remover bridges desnecessárias e validar origem. |
| Clipboard leakage | Senhas/tokens expostos na área de transferência podem ser capturados. | Evitar cópia de segredos, redaction e autoclearing quando adequado. |
| Screenshot / screen overlay | Dados sensíveis aparecem em capturas ou sobreposição maliciosa. | Redução de dados, controles de plataforma onde disponíveis, MFA. |
| Mobile reverse engineering | Código no pacote revela lógica e chaves, burlando controles locais. | Nunca confiar em lógica client-side, proteção do servidor e hardening. |
| App tampering / repackaging | App modificado distribui código adulterado e simula produto oficial. | Assinaturas, distribuição verificada, attestation como sinal adicional. |
| Root/jailbreak environment abuse | Ambiente comprometido permite inspeção/manipulação local ampliada. | Assumir cliente potencialmente hostil e reforçar verificações server-side. |
| Intent injection | Dados de Intent não confiável acionam fluxo inadequado. | Validação dos extras e permission checks. |
| Mobile insecure backup | Backups de sistema contêm dados e segredos que não deveriam ser exportados. | Configurar exclusões de backup e secure storage. |
| Push notification sensitive leakage | Dados privados são exibidos em notificações/bloqueio de tela. | Conteúdo mínimo, configuração de privacidade e autorização. |
| Desktop auto-update compromise | Atualizador aceita binário não assinado ou de canal inseguro. | Assinatura, TLS, canal confiável e rollback seguro. |
| Electron insecure nodeIntegration | Conteúdo remoto obtém acesso a APIs nativas. | `contextIsolation`, sandbox, Node integration desabilitada e IPC limitado. |
| Electron IPC privilege bypass | Renderer não confiável envia mensagens administrativas ao processo principal. | Autorização por canal/mensagem, validação de payload e origem. |
| Native app DLL/plugin loading | Extensão ou biblioteca de diretório indevido é carregada. | Assinatura, paths confiáveis e controle de plugins. |
| Insecure local API | Aplicação desktop expõe endpoint localhost sem controle de origem e auth. | Autenticação, CSRF/origin checks e acesso limitado. |
| MDM misconfiguration | Dispositivos corporativos perdem gestão, criptografia ou compliance. | Políticas MDM, postura de dispositivo e inventário. |

### 5.15 IoT, dispositivos, firmware e OT/ICS

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| IoT default credentials | Dispositivo mantém login de fábrica reutilizado em milhares de unidades. | Credenciais únicas por dispositivo, onboarding seguro. |
| Insecure firmware update | Atualização não é assinada ou validada corretamente. | Secure Boot, assinaturas de firmware e rollback controlado. |
| Unencrypted telemetry | Sensores enviam dados/controle em canal sem autenticidade. | TLS/mTLS ou protocolos apropriados e identidade por dispositivo. |
| Device cloning | Identidade do dispositivo é copiável entre unidades. | Chaves em secure element/TPM e provisionamento único. |
| Insecure exposed management service | Telnet, painel ou API de configuração fica acessível publicamente. | Rede isolada, desabilitar serviços e gestão via canal protegido. |
| Firmware secret extraction | Chaves comuns incorporadas ao firmware são extraídas. | Segredos por unidade, secure storage e rotação. |
| Replay of device command | Comando legítimo repetido provoca ação não autorizada. | Nonce, sequência, timestamp e autenticação. |
| Sensor/data spoofing | Dados falsos provocam decisão operacional errada. | Integridade/autenticidade, validação cruzada e detecção de anomalia. |
| OT lateral movement | Rede corporativa comprometida alcança controles industriais. | Segmentação forte IT/OT, acesso mediado e monitoramento. |
| Safety system bypass | Controles de segurança física/operacional são desabilitados. | Controles independentes, mudança aprovada e validação operacional. |
| Insecure industrial protocol | Protocolo legado sem autenticação permite comandos indevidos. | Gateway seguro, segregação e compensação operacional. |
| Device fleet botnet recruitment | Dispositivos vulneráveis tornam-se nós de ataques distribuídos. | Patch OTA, credenciais únicas, bloqueio de portas e telemetria. |

### 5.16 IA generativa, LLM, RAG, agentes, ferramentas e MCP

**Recomendação de arquitetura:** tratar instruções de sistema/desenvolvedor como política, mas **não considerar prompts secretos como barreira de segurança**. Documentos, resultados de pesquisa, e-mails, páginas web, mensagens, embeddings e saídas de ferramentas são entradas potencialmente hostis. O servidor deve verificar permissões independentemente da decisão textual do modelo.

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Direct prompt injection | Usuário tenta substituir objetivos/instruções em interface de LLM. | Separação de instruções/dados, validação de ferramentas e testes adversariais. |
| Indirect prompt injection | Página, PDF, e-mail ou resultado de ferramenta contém comandos destinados ao agente. | Marcação de fonte não confiável, controle de ações e checagem externa ao modelo. |
| Tool output laundering | Resposta de ferramenta é tratada como instrução autoritativa. | Classificação de origem e validação semântica/estrutural no orquestrador. |
| Retrieval-augmented injection | Documento recuperado em RAG desvia comportamento do modelo. | Fontes confiáveis, filtros, metadados de proveniência, políticas fora do prompt. |
| RAG cross-tenant leakage | Busca vetorial retorna documentos de outro cliente/usuário. | Filtro de autorização no mecanismo de retrieval e no documento final. |
| Embedding/vector store poisoning | Dados artificiais contaminam índice e resultados de recuperação. | Curadoria de ingestão, proveniência, aprovação e reindexação auditável. |
| Training-data poisoning | Dados de treino manipulados induzem comportamento indevido. | Proveniência, validação de datasets, avaliação e isolamento do pipeline. |
| Model supply-chain compromise | Modelo/pesos/adapters ou conversores são manipulados. | Artefatos assinados, revisão de origem, scanning e sandbox. |
| Sensitive information disclosure | Resposta revela segredos, PII ou dados conectados sem permissão. | Redação, políticas de acesso e filtros antes da recuperação/ferramenta. |
| System prompt extraction | Ator tenta obter instruções internas ou informações embutidas. | Não guardar segredos em prompts, restringir ferramentas e outputs. |
| Excessive agency | Agente tem capacidade ampla de enviar, apagar, pagar ou configurar sem controle. | Least privilege, ações permitidas, limites e aprovação humana para alto impacto. |
| Agent goal hijacking | Contexto adversarial modifica metas de execução do agente. | Objetivo assinado/estável fora do modelo e avaliação de cada ação. |
| Tool misuse | Ferramenta legítima é invocada com objetivo ou parâmetros impróprios. | Validação de argumentos, escopo, autorização e auditoria por ferramenta. |
| MCP tool poisoning | Descrição/resultado de ferramenta MCP contém instruções enganosas. | Registrar servidores confiáveis, revisar schemas e não confiar em descrições como política. |
| MCP server impersonation | Servidor de ferramenta falso se apresenta como integração legítima. | Autenticação do servidor, identidade verificável e allowlist de conectores. |
| Tool schema spoofing | Modelo recebe definição adulterada de ferramenta e concede poder indevido. | Schemas versionados/assinados, validação no executor e change control. |
| Cross-tool exfiltration | Agente lê dado sensível em uma ferramenta e envia via outra. | Políticas de fluxo de dados, escopos separados e aprovação para saída externa. |
| Agent identity and privilege abuse | Agente usa credencial do usuário para operação não autorizada. | Consentimento por ação/escopo, identidade delegada curta e aprovação contextual. |
| Memory poisoning | Texto malicioso é registrado como memória persistente e influencia ações futuras. | Revisão da origem, distinção dados/instruções, TTL e edição/auditoria de memória. |
| Context poisoning | Histórico/contexto é contaminado para alterar decisões e classificações. | Proveniência de mensagens, integridade, limites e verificação independente. |
| Multi-agent trust confusion | Agente secundário confia irrestritamente na saída de outro. | Credenciais e contexto por agente, autenticação interagente e contratos. |
| Unbounded token/cost consumption | Prompts, loops e chamadas de ferramenta consomem orçamento descontrolado. | Quotas por usuário/tarefa, limite de iterações/tokens e circuit breaker. |
| Output handling injection | LLM produz HTML, SQL ou shell que aplicação executa sem validação. | Tratar saída do modelo como não confiável e proteger sinks tradicionais. |
| Hallucination as authoritative action | Informação incorreta induz pagamento, alteração ou decisão sensível. | Validação com fonte primária, supervisão e limites de autonomia. |
| Unsafe code generation | Código sugerido introduz segredos, execuções inseguras ou falhas de auth. | Revisão humana, SAST/SCA, testes de segurança e templates seguros. |
| Model extraction | Consultas revelam comportamento/modelo proprietário e custo operacional. | Rate limit, termos de uso, detecção de padrões e segurança de API. |
| Model inversion / membership inference | Saídas revelam informação sobre dados de treinamento em certos cenários. | Privacidade de treinamento, avaliação e exposição mínima. |
| Unsafe model tool execution | Agente executa código sem isolamento e acessa dados/host. | Sandbox efêmero, sem root, rede restrita, FS mínimo e orçamento. |
| HITL approval manipulation | Conteúdo externo fabrica ou influencia aprovação humana para ação perigosa. | Interface mostra ação exata, origem confiável e confirmação fora do conteúdo. |
| Browser-agent web prompt injection | Página visitada instrui agente a mudar objetivos, enviar dados ou clicar. | Limitar navegação e ferramentas, autorização por ação, egress e auditoria. |
| AI-generated phishing/deepfakes | Automação torna fraude e impersonação mais convincentes. | Processos de aprovação independentes, FIDO2 e verificação de identidade. |
| Tool-result provenance loss | Resposta perde referência a origem e vira afirmação confiável. | Citações verificáveis, metadados de trust level e checagem de fontes. |
| Automated agent loop/recursion | Agente invoca ferramentas ou outros agentes indefinidamente. | Limites de profundidade, tempo, ações, orçamento e watchdog. |

### 5.17 Segurança física, disponibilidade operacional e fator humano

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Theft of unlocked device | Equipamento desbloqueado dá acesso a sessão e arquivos. | Bloqueio automático, FDE, autenticação e MDM. |
| Theft of backup media | Mídia de backup é perdida/roubada sem proteção. | Criptografia, inventário e cadeia de custódia. |
| Unauthorized data center access | Ator sem autorização acessa hardware ou consoles. | Controle físico, registro, alarmes e segregação. |
| Shoulder surfing | Senha/dados são observados durante digitação/consulta. | Privacidade de tela, MFA e conscientização. |
| Unauthorized USB peripherals | Dispositivo USB malicioso se apresenta como teclado/rede. | Controle de periféricos, políticas e proteção endpoint. |
| Power/environmental outage | Falhas de energia, climatização ou instalações interrompem serviços. | Redundância, UPS, monitoramento ambiental e recuperação. |
| Insider misuse | Usuário legítimo usa privilégio para finalidade indevida. | Menor privilégio, trilhas, separação de funções e revisões. |
| Negligent data handling | Compartilhamento indevido por erro humano expõe dados. | Classificação, DLP, UX segura e controles de compartilhamento. |
| Social trust exploitation | Autoridade aparente induz quebra de procedimento de segurança. | Processo verificável, dupla aprovação e treinamento. |
| Vendor onsite access abuse | Terceiro obtém acesso físico/lógico além de serviço contratado. | Acesso temporário supervisionado, escopo e logging. |

### 5.18 Segurança de memória, compiladores e exploração binária

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Stack buffer overflow | Escrita além do espaço alocado na pilha pode corromper dados e controle. | Linguagens memory-safe, análise estática, bounds checks, ASLR, stack canaries. |
| Heap buffer overflow | Escrita fora da área alocada no heap causa corrupção e eventual execução. | Memory-safe, sanitizers, allocators protegidos, fuzzing de parsers. |
| Out-of-bounds read | Leitura indevida revela memória, segredos ou causa falhas. | Verificação de limites, ASan/UBSan e testes de entrada. |
| Out-of-bounds write | Escrita indevida altera estruturas internas e controle do processo. | Bounds checking, revisão de C/C++, fuzzing e hardening de compilador. |
| Use-after-free (UAF) | Ponteiro aponta para memória liberada e depois reutilizada. | Ownership/borrowing, sanitizers, fuzzing e atualização de componentes. |
| Double free | Memória é liberada duas vezes, corrompendo heap ou causando DoS. | RAII/ownership, sanitizers, APIs de gerenciamento seguro de memória. |
| Dangling pointer | Referência persistente aponta para objeto destruído. | Linguagens memory-safe, lifetime tracking e testes. |
| Integer overflow/underflow | Aritmética transborda e produz alocação/checagem incorreta. | Inteiros checados, validação de limites e sanitizers. |
| Signedness conversion | Conversão sinalizado/não sinalizado altera limites de tamanho e índices. | Tipos corretos, checagens explícitas e warnings como erro. |
| Type confusion | Objeto é interpretado como tipo incompatível e pode violar memória. | Verificação de tipos, runtime patches e sandbox. |
| Format string injection | Formatação controlada interpreta marcadores de memória/comando. | Strings de formato constantes e APIs seguras. |
| NULL pointer dereference | Uso de ponteiro nulo provoca crash ou comportamento indevido. | Checagens, programação defensiva e testes de estado. |
| Race condition de memória | Threads acessam estado compartilhado sem sincronização correta. | Locks, atomics, modelos de concorrência seguros e race detectors. |
| Return-Oriented Programming (ROP) | Cadeias de instruções existentes podem ser usadas após corrupção de memória. | Memory safety, DEP/NX, ASLR, CFI e correções na falha raiz. |
| JIT spraying | Código gerado dinamicamente amplia regiões executáveis controláveis. | W^X, proteção do JIT, sandbox e atualizações. |
| Speculative execution side channels | Efeitos microarquiteturais revelam dados em determinados processadores/cenários. | Patches de firmware/SO, isolamento e mitigações de fabricante. |
| Cache-timing side channel | Variação de cache pode revelar operações secretas. | Implementações constant-time, isolamento e bibliotecas criptográficas auditadas. |
| Rowhammer / disturbance errors | Alterações físicas em memória podem afetar bits adjacentes sob condições específicas. | Mitigações de hardware, ECC quando aplicável e atualização de plataforma. |
| DMA / malicious peripheral | Periférico com acesso direto à memória pode contornar controles tradicionais. | IOMMU, política de portas, Kernel DMA Protection e controle físico. |
| Malicious compiler/build toolchain | Compilador ou linker adulterado injeta alteração invisível ao código fonte. | Toolchain verificada, builds reprodutíveis, assinaturas e proveniência. |
| ABI/FFI boundary misuse | Conversão entre linguagens nativas e seguras introduz UAF/OOB. | Revisar código unsafe, encapsular FFI e fuzzing de fronteiras. |
| GPU/accelerator memory isolation | Falhas no driver/runtime expõem memória de outros processos/tenants. | Isolamento, patch de drivers e gestão de workloads sensíveis. |

### 5.19 Redes sem fio, proximidade, navegação e periféricos

| Ataque ou abuso | Vulnerabilidade, consequência ou precondição | Mitigação e validação defensiva |
|---|---|---|
| Wi-Fi deauthentication/disassociation abuse | Quadros de gestão desprotegidos permitem desconexões e indução de reconexão. | Protected Management Frames (802.11w/PMF), WPA3 e monitoramento. |
| Wi-Fi weak passphrase attack | Chave compartilhada fraca pode ser descoberta por tentativas offline. | WPA3/802.1X, senha forte e rotação. |
| Wireless rogue access point | Ponto de acesso não autorizado captura dispositivos ou expõe rede. | WIDS/WIPS, 802.1X e inventário de pontos. |
| Bluetooth/BLE spoofing | Dispositivo adversário imita periférico autorizado. | Pairing autenticado, bonding correto e identidade por dispositivo. |
| BLE weak pairing | Métodos sem confirmação forte permitem interposição em cenários aplicáveis. | Escolher modo de pareamento mais forte suportado e criptografia. |
| Bluetooth service exposure | Serviços de depuração/controle ficam acessíveis por rádio. | Desativar perfis desnecessários, autenticar e atualizar firmware. |
| RFID/NFC cloning | Credencial de proximidade fraca pode ser copiada. | Credenciais criptográficas com desafio-resposta e revogação. |
| NFC relay attack | Mensagens de proximidade são retransmitidas em outro local. | Controles de transação, supervisão de risco e protocolos resistentes quando disponíveis. |
| GPS/GNSS spoofing | Sinais falsos alteram percepção de posição/tempo. | Verificação de integridade multi-sensor e alarmes de anomalia. |
| GPS/GNSS jamming | Interferência impede recepção de sinais de navegação. | Fontes redundantes de posicionamento/tempo e monitoramento de interferência. |
| CAN bus injection | Mensagens veiculares não autenticadas podem alterar comportamento dos controladores. | Segmentação, gateways, autenticidade das mensagens e safety design. |
| Industrial wireless command spoofing | Comando de rádio sem autenticação pode alterar dispositivos OT. | Autenticação criptográfica, segmentação e monitoração física. |
| Smart lock replay | Mensagem de abertura é reutilizada sem mecanismo de frescor. | Nonce/contador, challenge-response e armazenamento protegido de chaves. |
| Side-channel via sensors | Sensores de movimento, luz ou som expõem indiretamente dados de usuário. | Permissões mínimas e restrição de acesso a sensores. |

## 6. MITRE CWE Top 25 (2025): fraquezas de referência

Esta lista permite a verificação objetiva das 25 fraquezas priorizadas pela MITRE em 2025. **Ranking anual não substitui risco contextual.**

| Rank | CWE | Descrição curta |
|---:|---|---|
| 1 | CWE-79 | Cross-Site Scripting (XSS) |
| 2 | CWE-89 | SQL Injection |
| 3 | CWE-352 | Cross-Site Request Forgery |
| 4 | CWE-862 | Missing Authorization |
| 5 | CWE-787 | Out-of-bounds Write |
| 6 | CWE-22 | Path Traversal |
| 7 | CWE-416 | Use After Free |
| 8 | CWE-125 | Out-of-bounds Read |
| 9 | CWE-78 | OS Command Injection |
| 10 | CWE-94 | Code Injection |
| 11 | CWE-120 | Classic Buffer Overflow |
| 12 | CWE-434 | Unrestricted Upload of Dangerous File Type |
| 13 | CWE-476 | NULL Pointer Dereference |
| 14 | CWE-121 | Stack-based Buffer Overflow |
| 15 | CWE-502 | Deserialization of Untrusted Data |
| 16 | CWE-122 | Heap-based Buffer Overflow |
| 17 | CWE-863 | Incorrect Authorization |
| 18 | CWE-20 | Improper Input Validation |
| 19 | CWE-284 | Improper Access Control |
| 20 | CWE-200 | Exposure of Sensitive Information |
| 21 | CWE-306 | Missing Authentication for Critical Function |
| 22 | CWE-918 | Server-Side Request Forgery |
| 23 | CWE-77 | Command Injection |
| 24 | CWE-639 | Authorization Bypass Through User-Controlled Key |
| 25 | CWE-770 | Allocation of Resources Without Limits/Throttling |

Fonte primária: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html

## 7. Roteiro de validação de segurança por superfície

A skill deve produzir uma análise por evidências. **Ausência de configuração no repositório não prova ausência de proteção**, pois o controle pode residir no CDN, gateway, IdP ou infraestrutura externa. Classificar como `NÃO VERIFICADO` quando não houver evidência suficiente. Nunca declarar sistema seguro apenas porque não foram encontrados problemas via análise estática.

### 7.1 Checklist para aplicação web + SPA

- [ ] Identificar framework, roteamento, rendering (SSR/CSR), subdomínios, proxies, CDN e limites de confiança.
- [ ] Verificar XSS refletido, persistente, DOM e conteúdo rico; identificar sinks perigosos (`innerHTML`, HTML não sanitizado e código dinâmico).
- [ ] Avaliar CSP efetiva e dependência de scripts externos, `frame-ancestors`, `nosniff`, HSTS e cache de páginas sensíveis.
- [ ] Verificar cookies reais em resposta, não apenas constantes no código: `HttpOnly`, `Secure`, `SameSite`, `Path`, `Domain`, TTL e nome.
- [ ] Inspecionar armazenamento de tokens no browser; explicar riscos específicos de localStorage e não generalizar.
- [ ] Se sessão por cookie: examinar anti-CSRF, `Origin` e Fetch Metadata para rotas de alteração de estado.
- [ ] Validar CORS com origens e credenciais; garantir que CORS não seja confundido com auth.
- [ ] Confirmar redirects permitidos e tratamento de parâmetros de retorno em login/OIDC.
- [ ] Confirmar ausência de secrets em bundle, source maps, HTML inicial, analytics e console.
- [ ] Verificar arquivos de upload, renderização de PDFs/HTML/Markdown e downloads com header apropriado.

### 7.2 Checklist para backend/REST/GraphQL

- [ ] Inventariar endpoints, métodos, schemas, middlewares e funções administrativas.
- [ ] Montar matriz de papéis, ações e recursos; testar IDOR/BOLA/BFLA/BOPLA e isolamento entre tenants.
- [ ] Verificar queries SQL parametrizadas e ordem dinâmica de colunas submetida a allowlist.
- [ ] Examinar NoSQL, template rendering, `eval`, shell, serialização, XML e parsers de dados externos.
- [ ] Avaliar SSRF de URLs, webhook destinations, renderizadores e fetch de arquivos externos.
- [ ] Configurar limites de payload, paginação, queries, profundidade, concorrência e tempo.
- [ ] Verificar idempotência, locks, transações e invariantes para dinheiro, créditos, estoque e status.
- [ ] Confirmar autenticação também em workers, filas, cron, webhooks e APIs internas.
- [ ] Verificar tratamento de erro, stack trace, logs de segurança e proteção de dados sensíveis.
- [ ] Confirmar configuração de produção de docs, debug, admin consoles e health checks.

### 7.3 Checklist de identidade e sessões

- [ ] Explicitar decisão arquitetural: sessão opaca, JWT, BFF, OAuth/OIDC, WebAuthn.
- [ ] Verificar proteção de login contra brute force, stuffing, spraying e enumeração.
- [ ] Inspecionar recuperação de senha, troca de e-mail, registro de novo MFA e ações de alto risco.
- [ ] Checar hash de senha, salt, custo adaptativo e ausência de senha em logs.
- [ ] Validar expiração idle/absolute, rotação de session ID, invalidação no logout e revogação administrativa.
- [ ] Para JWT, testar rejeição de algoritmo errado, issuer/audience errado, token expirado, propósito errado e assinatura inválida.
- [ ] Inspecionar refresh token rotation, detecção de reuse e proteção de credenciais persistentes.
- [ ] Validar escopo de autorização a cada objeto, inclusive após alteração de papel ou tenant.
- [ ] Revisar OAuth Authorization Code + PKCE, redirect URI, state/nonce conforme fluxo e validação de token.

### 7.4 Checklist de bancos e persistência

- [ ] Banco não exposto publicamente salvo exigência arquitetural justificada e protegida.
- [ ] Aplicação usa conta de banco sem privilégios de administração e com escopo adequado.
- [ ] Índices e limites protegem queries caras e evitar saturação.
- [ ] Constraints garantem integridade de valores e relações, independentemente de frontend.
- [ ] RLS, quando usada, é testada com **a role real da aplicação**, não com superuser.
- [ ] Dados de tenants não se misturam em conexões reutilizadas, cache ou workers.
- [ ] Backups criptografados, protegidos, versionados e com restauração testada.
- [ ] Senhas/tokens de conexão fora do código; rotação e revogação são possíveis.
- [ ] Exportações são auditadas e sujeitas a limites.

### 7.5 Checklist cloud, rede e disponibilidade

- [ ] Definir quais serviços são públicos; colocar banco, cache, admin e brokers em rede privada.
- [ ] Validar proteção do origin contra bypass de CDN/WAF.
- [ ] Revisar DDoS L3/L4 no provedor e L7 na borda, além de procedimento de escalonamento.
- [ ] Definir quotas por identidade, endpoint, tenant e custo, com estado compartilhado entre instâncias.
- [ ] Verificar configuração de proxy confiável para `X-Forwarded-For` e `Forwarded`.
- [ ] Verificar timeouts, circuit breakers, limites de conexão, CPU, memória e fila.
- [ ] Examinar políticas de cloud IAM, bucket ACL, metadados e exposição de portas.
- [ ] Confirmar logging, alertas, budgets e testes de recuperação.
- [ ] Verificar patches e componentes sem suporte.

### 7.6 Checklist de containers e CI/CD

- [ ] Dockerfile com base controlada, usuário sem root, mínima superfície e sem secrets em layers.
- [ ] Kubernetes com Pod Security, RBAC mínimo, NetworkPolicy, quotas, proteções de volume e admission policies.
- [ ] Imagens fixadas por digest quando houver necessidade de integridade reprodutível.
- [ ] Pipeline não recebe credencial de produção durante execução de código de PR não confiável.
- [ ] Dependências e GitHub Actions de terceiros revisadas; actions preferencialmente fixadas por commit.
- [ ] Secrets scanning, SAST, SCA, SBOM, IaC scanning e container scanning nos pontos relevantes do pipeline.
- [ ] Artefatos com integridade/proveniência verificáveis e branches protegidas.
- [ ] Logs não exibem segredos; runners e caches não persistem credenciais entre projetos.

### 7.7 Checklist IA / agentes / RAG

- [ ] Identificar todos os locais onde conteúdo não confiável entra no contexto do modelo.
- [ ] Garantir que política de acesso e autorização da ferramenta sejam feitas por código externo ao LLM.
- [ ] Verificar se a recuperação RAG impõe filtros de tenant/usuário antes de montar contexto.
- [ ] Testar prompt injection indireto em conteúdo sintético e autorizado, sem exfiltrar dados reais.
- [ ] Definir aprovação humana verificável para envio externo, pagamento, exclusão ou alteração crítica.
- [ ] Validar tipos/limites dos argumentos de cada ferramenta, inclusive MCP e conectores.
- [ ] Separar identidades de agentes, ferramentas e usuários; não compartilhar tokens globais.
- [ ] Controlar egress, leitura/escrita de arquivos, execução de código e cadeia de chamadas.
- [ ] Definir budgets de tokens, custo, número de ferramentas e duração máxima da tarefa.
- [ ] Registrar decisões, invocações, fonte dos dados e eventos de revisão humana sem vazar segredos.
- [ ] Prevenir memory poisoning e permitir inspeção/revogação de memórias operacionais persistidas.

## 8. Padrão de severidade, priorização e confiança

### 8.1 Criticidade por contexto

| Prioridade | Exemplos de condição | Resposta sugerida |
|---|---|---|
| **P0 Crítica** | Comprometimento em andamento, chave de produção exposta com uso indevido, RCE exposta em serviço crítico, vazamento grave confirmado | Conter imediatamente, revogar credenciais, preservar evidências e acionar resposta a incidentes. |
| **P1 Alta** | BOLA intertenant explorável, SQLi com dados sensíveis, auth bypass, upload executável, KEV aplicável exposta | Corrigir com prioridade máxima operacional, monitorar e validar regressão. |
| **P2 Média** | CSP parcial, rate limit insuficiente sem exploração evidente, informações internas expostas, dependência vulnerável sem caminho conhecido | Planejar correção, reduzir exposição e medir risco residual. |
| **P3 Baixa** | Hardening de defesa em profundidade, ajustes de cabeçalhos sem impacto comprovado, logging incompleto em ação não crítica | Incluir no backlog e revisar periodicamente. |
| **Informativa** | Boa prática ausente sem evidência de exploração ou orientação de arquitetura | Recomendar e marcar como sugestão, não como falha confirmada. |

A classificação é **orientativa**, não substitui metodologia organizacional nem CVSS contextual. A skill deve considerar confidencialidade, integridade, disponibilidade, privacidade, exposição pública, complexidade de exploração, privilégios necessários, dependência de interação, dados e criticidade do negócio.

### 8.2 Campos de confiança e estados

- **CONFIRMADO:** código, configuração ou teste demonstra a condição de risco com evidência suficiente.
- **POTENCIAL:** padrão suspeito identificado, mas exploração depende de configuração/fluxo não verificado.
- **NÃO VERIFICADO:** falta acesso a ambiente, proxy, segredo, banco, serviço externo ou evidência operacional.
- **MITIGADO:** há evidência verificável de controle efetivo para o cenário estudado.
- **NÃO APLICÁVEL:** tecnologia/superfície inexistente na arquitetura analisada.
- **FALSO POSITIVO:** investigação demonstrou que a hipótese não ocorre, com justificativa e evidência.

### 8.3 Matriz de risco mínimo

Para cada finding, registrar: recurso/superfície, pré-condições, ativo afetado, ameaça, consequência plausível, exposição externa, controles existentes, confiança da avaliação, esforço de correção, severidade, recomendação, teste de regressão e fonte oficial. **Não inventar exploração demonstrada se houve apenas leitura de código.**

## 9. Padrões recomendados para stacks full stack

### 9.1 React / Next.js

- Evitar renderizar HTML arbitrário. `dangerouslySetInnerHTML` exige fonte estritamente controlada ou sanitização robusta; o perigo depende do fluxo e contexto.
- Não confiar em checks de acesso em componentes, middleware de navegação ou ocultação de botões como única autorização.
- Diferenciar dados de cliente, SSR e server-only; não enviar segredos ao bundle, hydration payload ou client components.
- Proteger Route Handlers, Server Actions e endpoints RPC com autenticação/autorização por ação/recurso.
- Considerar BFF com cookie opaco `HttpOnly; Secure; SameSite` e anti-CSRF, conforme arquitetura de origin.
- Definir CSP compatível com rendering e scripts necessários, reduzindo dependência de `unsafe-inline`/`unsafe-eval`.
- Revisar cache ISR/SSR/CDN para não compartilhar dados autenticados entre usuários/tenants.
- Revisar uploads, redirecionamentos, `next/image` remoto e qualquer funcionalidade que realiza fetch de URLs externas em relação a SSRF.
- Fixar versões suportadas e conferir advisories do framework e de plugins.

### 9.2 Node.js / Express / NestJS

- Validar entradas com DTOs/schemas em runtime, rejeitando propriedades não previstas onde adequado.
- Usar Helmet/cabeçalhos equivalentes conscientemente, sem presumir que cabeçalhos substituem correções de código.
- Configurar proxy confiável, limite de body, rate limiting distribuído e shutdown gracioso.
- Aplicar guards/policies por rota, recurso, campo e tenant. Não confiar apenas no decorator de auth geral.
- Evitar `eval`, `Function`, `child_process.exec` com entrada externa, `deserialize` inseguro e parsers desatualizados.
- Usar prepared statements/ORM seguro e políticas de consulta para SQL dinâmico.
- Verificar webhooks por assinatura e controles anti-replay, antes de alterar estado.
- Configurar erros genéricos em produção e logs estruturados com request ID sem tokens.
- Inserir limites em workers, filas, uploads, fetch e operações de DB.

### 9.3 PostgreSQL

- Conexão TLS quando exigido pela topologia e por requisito de confidencialidade.
- Papel dedicado à aplicação, permissões mínimas, migrations com role separada da role de runtime.
- Prepared statements; não concatenar filtros/ordenação vindos do usuário.
- RLS com políticas `USING` e `WITH CHECK` quando multi-tenant justificar; revisar bypass por superuser/owner/roles especiais.
- `tenant_id` deve ser derivado do contexto de autenticação e submetido a validação em consultas e operações de workers.
- Constraints, transações e controles de concorrência para dinheiro, direitos e inventário.
- Logs e trilhas de consulta suficientes, sem expor dados sensíveis; backups e restore testados.

### 9.4 Redis / filas / jobs

- Nunca expor Redis público sem controle; usar rede privada e autenticação/ACL/TLS conforme topologia.
- Chaves de cache devem incluir contexto de tenant/usuário/permissões quando houver dados sensíveis.
- Rate limiting deve ser distribuído e corretamente atômico; avaliar consistência e falhas de disponibilidade.
- Filas precisam de retries com backoff, idempotência, DLQ e limites de trabalho.
- Payloads de jobs são entradas não confiáveis se provenientes de integrações; revalidar schema e autorização no consumidor.
- Não tratar cache como fonte de verdade para direitos críticos sem estratégia de invalidação.

### 9.5 Docker / Kubernetes / Cloud

- Usar secret manager e identidades de workload; não publicar `.env` em imagem nem em repositório.
- Non-root, filesystem read-only quando viável, capabilities mínimas, seccomp e atualização de base.
- Banco e Redis em subredes privadas, egress específico, WAF/CDN na borda, origin restrito.
- Backups imutáveis e monitorados, políticas de patch e observabilidade de segurança.
- CI/CD com revisão obrigatória, SBOM, SCA, SAST e assinatura/proveniência quando adequado.

## 10. Exemplos de controles verificáveis sem exploração de alvos

### 10.1 Estrutura de teste de autorização

```text
Dado: usuario_A autenticado no tenant_A
E: recurso_B pertence ao tenant_B
Quando: usuario_A solicita leitura/alteracao de recurso_B
Entao: resposta de autorizacao e nenhum dado de recurso_B e retornado
E: trilha de auditoria registra a negacao sem revelar informacao sensivel
```

### 10.2 Estrutura de teste de JWT

```text
Caso 1: token expirado => rejeitado
Caso 2: assinatura invalida => rejeitado
Caso 3: issuer nao confiavel => rejeitado
Caso 4: audience de outra API => rejeitado
Caso 5: token de ID usado como access token => rejeitado
Caso 6: usuario desativado ou sessao revogada => acesso rejeitado conforme desenho
Caso 7: tenant no token nao concede acesso a objeto de outro tenant
```

### 10.3 Estrutura de teste de cookies/CSRF

```text
1. Capturar Set-Cookie em ambiente autorizado.
2. Confirmar Secure, HttpOnly, SameSite, Path e Domain corretos para a arquitetura.
3. Confirmar que rotas mutaveis negam requisicoes cross-site sem prova anti-CSRF adequada.
4. Confirmar que GET/HEAD nao alteram estado.
5. Confirmar que logout invalida sessao no servidor, nao apenas remove cookie no navegador.
6. Testar CORS e Origin sem tentar explorar qualquer dominio de terceiros.
```

### 10.4 Estrutura de teste SQLi seguro

```text
1. Localizar queries dinamicas e identificar parametros de entrada.
2. Confirmar uso de bind parameters nos valores.
3. Para identificadores dinamicos (colunas/ordem), confirmar allowlist explicita.
4. Verificar role minima do banco e inexistencia de consultas com interpolacao insegura.
5. Criar testes unitarios/de integracao para que entradas inesperadas sejam tratadas como dados.
6. Executar analise dinamica apenas em ambiente autorizado, sem extrair ou modificar dados reais.
```

### 10.5 Estrutura de teste anti-DDoS e abuso

```text
1. Ler configuracao do CDN/provedor, regras WAF e protecao upstream.
2. Verificar limites de body, conexoes, tempo, queries e filas.
3. Testar localmente quotas com volume pequeno, dentro do ambiente de teste.
4. Simular falhas por injecao controlada de latencia/erro, sem gerar ataques de saturacao.
5. Verificar metricas e runbook de escalation ao provedor.
6. Diferenciar ausencia de configuracao no repositorio de ausencia de defesa no edge.
```

## 11. Projetando a futura skill de segurança

### 11.1 Missão

> Auditar projetos full stack de maneira defensiva e reproduzível. Identificar superfícies e limites de confiança; mapear fraquezas para categorias oficiais; coletar evidências; priorizar riscos; propor correções específicas à tecnologia; gerar testes de regressão; e registrar limitações, sem afirmar vulnerabilidades não comprovadas nem executar ações intrusivas sem autorização.

### 11.2 Estrutura sugerida de repositório

```text
security-audit-skill/
├── SKILL.md                       # instruções da skill e fluxo obrigatório
├── README.md                      # uso e limitações
├── references/
│   ├── catalogo-ataques.md        # famílias de ameaças e fraquezas
│   ├── catalogo-controles.md      # métodos defensivos
│   ├── arquitetura-autenticacao.md
│   ├── api-web-frontend.md
│   ├── infraestrutura-cloud.md
│   ├── cadeia-suprimentos.md
│   ├── seguranca-ia-agentes.md
│   ├── padroes-normativos.md
│   └── fontes-e-versoes.md
├── rules/
│   ├── auth-session.yml
│   ├── access-control.yml
│   ├── injection.yml
│   ├── api.yml
│   ├── frontend.yml
│   ├── cloud.yml
│   ├── devsecops.yml
│   ├── privacy.yml
│   └── llm-agents.yml
├── prompts/
│   ├── threat-model.md
│   ├── code-review.md
│   ├── remediation-plan.md
│   └── security-report.md
├── schemas/
│   ├── finding.schema.json
│   ├── control.schema.json
│   └── project-profile.schema.json
├── tests/
│   ├── fixtures-safe/
│   ├── false-positives/
│   └── regression/
├── scripts/
│   ├── catalog_lint.py
│   ├── validate_findings.py
│   └── generate_report.py
└── outputs/
    ├── relatorio-auditoria.md
    ├── findings.json
    ├── matriz-riscos.csv
    └── plano-correcao.md
```

### 11.3 Fluxo operacional obrigatório

1. **Descoberta:** ler árvore do projeto, manifestos, packages, IaC, CI, readmes e políticas. Identificar linguagem, frameworks, bibliotecas e serviços expostos.
2. **Escopo e autorização:** registrar alvos autorizados, ambientes, credenciais de teste disponíveis, exclusões e técnicas permitidas. Padrão: somente leitura e testes locais não destrutivos.
3. **Mapeamento:** recursos, usuários, tenants, endpoints, banco, fluxos de dados e fronteiras de confiança. Criar modelo resumido de ameaças.
4. **Verificação estática:** procurar sinks, middleware, guards, contratos, controle de acesso, segredos, dependências e configurações.
5. **Corroboração:** relacionar evidência a CWE/OWASP/ASVS sem inventar IDs. Comparar proteção em código e em infraestrutura conhecida.
6. **Testes não destrutivos autorizados:** executar testes unitários, integração e scanners configurados para escopo restrito. Não testar terceiros automaticamente.
7. **Priorização:** severidade contextual, confiança, exposição, facilidade de correção e risco de negócio.
8. **Correção:** apontar patch/arquitetura concreta, riscos de compatibilidade e teste esperado. Alterar código somente quando solicitado/autorizado.
9. **Regressão:** criar testes para reproduzir a condição de erro de forma segura e confirmar correção.
10. **Entrega:** relatório executivo, inventário de achados, matriz de risco, controles ausentes/não verificados e roadmap priorizado.
11. **Memória de auditoria:** registrar estado incremental por commit, data, escopo, resultado e decisões; não armazenar segredos.
12. **Atualização:** comparar versões dos referenciais, feeds de CVE/KEV e advisories; marcar fontes consultadas em data específica.

### 11.4 Contrato de saída de cada finding

```yaml
id: SEC-2026-001
titulo: "Exemplo ilustrativo: rota sem verificacao de propriedade"
status: POTENCIAL   # CONFIRMADO | POTENCIAL | NAO_VERIFICADO | MITIGADO | NAO_APLICAVEL | FALSO_POSITIVO
prioridade: P1      # P0 | P1 | P2 | P3 | INFORMATIVA
confianca: media    # baixa | media | alta
categoria: "Autorizacao por objeto"
referenciais:
  cwe: ["CWE-862", "CWE-639"]
  owasp_web: "A01:2025"
  owasp_api: "API1:2023"
ativo: "API de documentos"
precondicoes: "Conta autenticada com acesso a identificador de outro recurso"
evidencia:
  - arquivo: "src/routes/documents.ts"
    linha_inicio: 42
    linha_fim: 49
    observacao: "Exemplo: a consulta aparentemente nao filtra por proprietario/tenant"
impacto: "Acesso potencial entre usuarios/tenants"
controles_existentes: []
lacunas_de_validacao:
  - "Confirmar se existe RLS ou middleware externo"
recomendacao: "Validar propriedade no backend e restringir consulta por principal/tenant"
teste_regressao: "Usuario A nao pode ler documento do usuario B"
fontes:
  - "https://cwe.mitre.org/data/definitions/862.html"
alteracao_aplicada: false
```

Esse objeto é **um exemplo fictício**, não resultado de auditoria real.

### 11.5 Política de prova e rastreabilidade

- Todo achado deve citar **arquivo/linha** quando possível; recursos externos exigem evidência documentada sem divulgar segredo.
- Distinguir **fonte oficial**, **hipótese** e **observação**. Não deduzir configuração de CDN ausente em Git.
- Conectar cada finding aos controles pertinentes sem empilhar categorias irrelevantes.
- Se o sistema usa JWT em cookie, registrar **segurança do JWT e proteção do cookie/CSRF em campos diferentes**.
- Se houver `RateLimiter` no backend, não concluir automaticamente que existe defesa anti-DDoS volumétrica.
- Não indicar LGPD como "compliance alcançado" só porque há criptografia; aspectos jurídicos e organizacionais exigem avaliação própria.
- Nunca imprimir segredos descobertos; relatar tipo, caminho, hash parcial seguro quando cabível e ação de revogação.
- Respeitar arquivos ignorados e limites de consulta; nenhuma execução de script de terceiro não revisado apenas porque uma dependência o sugere.
- Não classificar todas as vulnerabilidades detectadas como críticas. Contexto e impacto são obrigatórios.

### 11.6 Proposta de módulos da skill

| Módulo | Insumos | Saídas |
|---|---|---|
| `discover` | Repositório, manifestos, docs, IaC | Perfil técnico e inventário |
| `threat-model` | Fluxos, ativos, identidades e endpoints | STRIDE, riscos e trust boundaries |
| `audit-auth` | Código de login, cookies, JWT, IdP | Achados IAM e testes |
| `audit-access` | Routes, services, ORM, tenants | Matriz BOLA/BFLA/BOPLA e achados |
| `audit-input` | Parsers, DB, templates, uploads | Achados SQLi/XSS/SSRF/injeção |
| `audit-api` | OpenAPI, GraphQL, gRPC, WebSockets | Contrato, quotas e autorização |
| `audit-infra` | Terraform, Docker, K8s, cloud | Exposições, IAM, resiliência |
| `audit-supplychain` | Lockfiles, packages, CI | SBOM/SCA, riscos e procedência |
| `audit-ai` | Tools, RAG, agents, model configs | Fluxos de confiança e riscos agentic |
| `test-safe` | Escopo autorizado, fixtures | Testes regressivos não destrutivos |
| `prioritize` | Findings + contexto | Ranking e roadmap |
| `report` | Findings e evidências | MD, JSON e resumo executivo |
| `update-intel` | Feeds oficiais | Mudanças de padrões e vulnerabilidades |

### 11.7 Critérios de qualidade para lançamento da skill

- **Cobertura:** verificação por grupos OWASP aplicáveis, API, sessões, infra, supply chain e IA quando houver.
- **Precisão:** suíte com casos positivos, negativos e falsos positivos; revisões humanas dos findings mais graves.
- **Reprodutibilidade:** mesma revisão de código e configuração gera resultados consistentes.
- **Segurança operacional:** nenhuma ação destrutiva por padrão; limite de escopo, rate e orçamento para testes.
- **Explicabilidade:** cada achado possui evidência, impacto, correção e teste de regressão.
- **Atualização:** fontes verificáveis, versões e data da consulta.
- **Privacidade:** não coletar nem armazenar dados sensíveis desnecessariamente.
- **Portabilidade:** regras independentes de stack e adaptadores por tecnologia.

## 12. Privacidade, dados pessoais e conformidade no Brasil

A proteção técnica de dados deve atender à finalidade e ao contexto de tratamento. No Brasil, considerar LGPD (Lei nº 13.709/2018), orientações aplicáveis da ANPD, políticas de retenção e procedimentos de resposta. **A implementação de controles técnicos não equivale, isoladamente, à comprovação de conformidade jurídica com a LGPD.**

| Dimensão | Pergunta de auditoria | Evidência desejada |
|---|---|---|
| Inventário | Quais dados pessoais são coletados, onde transitam e onde ficam armazenados? | Mapa de dados e sistemas, inventário por finalidade. |
| Necessidade | Há coleta e retenção além do necessário para a finalidade? | Schemas mínimos, políticas de retenção e descarte. |
| Acesso | Quem pode acessar CPF, e-mail, documentos, dados financeiros e dados sensíveis? | Matriz de autorização, logs e segregação. |
| Proteção | Existem criptografia, mascaramento, backups e proteção de credenciais adequados? | Configuração, testes e operação. |
| Terceiros | Quais fornecedores recebem dados ou acesso indireto? | Integrações, contratos, escopos e avaliações. |
| Incidentes | Há processo para detecção, contenção, análise, comunicação e documentação? | Runbook e registro de incidentes. |
| Direitos | Há operações controladas para acesso, correção e eliminação conforme aplicabilidade? | Fluxo auditável e autorização. |
| Retenção | Dados de produção vazam para logs, analytics e ambientes de testes? | Política de redaction, mascaramento e controles por ambiente. |

Consultar o guia e checklist da ANPD para agentes de tratamento de pequeno porte como referência operacional complementar, sem supor que medidas ou requisitos específicos se apliquem a todos os cenários igualmente.

## 13. Manutenção contínua do catálogo

Uma skill efetiva **não congela** o cenário de 2026. Implementar rotina de curadoria, com controle de versões:

1. Acompanhar novos advisories do framework/linguagem e CVEs que atinjam a SBOM do projeto.
2. Consultar o catálogo de vulnerabilidades exploradas conhecido da CISA (KEV) e fontes oficiais dos fornecedores.
3. Atualizar mapeamentos CWE, OWASP, ATT&CK e ASVS quando versões mudarem.
4. Acrescentar controles para técnicas emergentes, preservando histórico de regras anteriores.
5. Revisar falsos positivos, exclusões aprovadas, decisões de risco e regressões anteriores.
6. Controlar licença/atribuição dos referenciais consultados; usar links e resumos próprios, sem republicar integrais não autorizadas.
7. Registrar sempre fonte, versão, data de acesso e status de verificação. Não apresentar boletim antigo como vulnerabilidade ainda aberta sem checar versão afetada/correção.
8. Usar inteligência externa somente sob permissões adequadas e privilegiar feeds oficiais; não executar conteúdo externo obtido em advisories.

### 13.1 Cadência sugerida

| Evento | Ação |
|---|---|
| Novo commit/PR | SAST, secrets scanning, políticas de código e testes regressivos rápidos. |
| Dependência adicionada/atualizada | SCA, SBOM incremental, confiança do pacote e integridade. |
| Novo serviço/endpoint | Modelagem de ameaça, classificação e matriz de autorização. |
| Novo release | Conferir changelog de segurança, IaC, headers e limites no ambiente real. |
| Novo CVE/KEV aplicável | Revisar exposição, versão, mitigação e prioridade. |
| Mudança de IdP/token/cookie | Revalidar sessão, CSRF, CORS, autorização e recuperação. |
| Nova integração com IA/ferramenta | Revalidar permissões, fontes externas, exfiltração, budgets e auditoria. |
| Incidente ou achado externo | Gerar teste regressivo e atualizar regras/baselines. |

## 14. Fontes normativas e técnicas oficiais consultadas

Estas referências servem como **fontes primárias e catálogos vivos**. Suas versões e datas estão sujeitas a alterações. Links foram pesquisados para preparação desta versão em 04/11/2026.

### 14.1 OWASP

1. **OWASP Top 10:2025 (PT-BR)**: https://top10.owasp.org/2025/pt-BR/
2. **OWASP ASVS 5.0.0**: https://asvs.owasp.org/
3. **OWASP ASVS Downloads**: https://asvs.owasp.org/downloads/
4. **OWASP API Security Top 10 (2023)**: https://api-security.owasp.org/
5. **OWASP API Top 10 overview**: https://devguide.owasp.org/en/07-training-education/07-api-top-ten/
6. **OWASP WSTG v4.2 estável**: https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/
7. **OWASP Session Management Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet
8. **OWASP CSRF Prevention Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
9. **OWASP Password Storage Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
10. **OWASP HTTP Headers Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
11. **OWASP SSRF Prevention Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
12. **OWASP Logging Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
13. **OWASP Automated Threats**: https://owasp.org/projects/automated-threats-to-web-applications
14. **OWASP Mobile MASVS**: https://mas.owasp.org/MASVS/
15. **OWASP Mobile Top 10**: https://owasp.org/projects/mobile-top-10
16. **OWASP Kubernetes Top 10 2025**: https://kubernetes-top10.owasp.org/
17. **OWASP CI/CD Top 10**: https://owasp.org/projects/top-10-cicd-security-risks
18. **OWASP GenAI LLM Top 10 2026**: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
19. **OWASP Top 10 Agentic Applications 2026**: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
20. **OWASP GenAI project (novas pesquisas)**: https://genai.owasp.org/
21. **OWASP Security Component Verification**: https://scvs.owasp.org/
22. **OWASP attack pattern index**: https://community.owasp.org/attacks/

### 14.2 MITRE, NIST, CISA, padrões e especificações

23. **MITRE CWE Top 25 2025**: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html
24. **MITRE CWE catalog**: https://cwe.mitre.org/
25. **MITRE ATT&CK Enterprise**: https://attack.mitre.org/matrices/enterprise/
26. **MITRE ATT&CK techniques**: https://attack.mitre.org/techniques/
27. **MITRE CAPEC**: https://capec.mitre.org/
28. **MITRE ATLAS (IA)**: https://atlas.mitre.org/
29. **NIST CSF 2.0**: https://www.nist.gov/cyberframework
30. **NIST SP 800-218 SSDF 1.1**: https://csrc.nist.gov/pubs/sp/800/218/final
31. **NIST SP 800-63-4 Digital Identity**: https://csrc.nist.gov/pubs/sp/800/63/4/final
32. **NIST NVD (CVE/CVSS)**: https://nvd.nist.gov/
33. **CISA Known Exploited Vulnerabilities**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
34. **SLSA specification v1.2**: https://slsa.dev/spec/v1.2/
35. **RFC 8725 (JWT Best Current Practices)**: https://www.rfc-editor.org/rfc/rfc8725.html
36. **RFC 9700 (OAuth 2.0 Security Best Current Practice)**: https://www.rfc-editor.org/rfc/rfc9700.html
37. **RFC 7636 (PKCE)**: https://www.rfc-editor.org/rfc/rfc7636.html
38. **RFC 9449 (DPoP)**: https://www.rfc-editor.org/rfc/rfc9449.html
39. **RFC 8705 (OAuth mTLS)**: https://www.rfc-editor.org/rfc/rfc8705.html
40. **RFC 7519 (JWT)**: https://www.rfc-editor.org/rfc/rfc7519.html
41. **RFC 9116 (security.txt)**: https://www.rfc-editor.org/rfc/rfc9116.html
42. **ANPD: guia e checklist de segurança da informação**: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte
43. **Lei Geral de Proteção de Dados (Lei 13.709/2018)**: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

## 15. Glossário e decisões de arquitetura

| Termo | Definição útil |
|---|---|
| AuthN | Autenticação: verificar identidade. |
| AuthZ | Autorização: verificar permissão para uma ação/recurso. |
| BOLA | Falha de autorização ao nível de objeto; ocorre frequentemente em APIs. |
| BOPLA | Falha de autorização ao nível de propriedade/campo de objeto. |
| BFF | Backend-for-Frontend; pode isolar tokens OAuth do navegador. |
| CSP | Content Security Policy; defesa adicional contra injeções de conteúdo e scripts. |
| CSRF | Forgery de requisição autenticada por browser, associado a envio automático de credenciais. |
| CWE | Classe de fraqueza de software/hardware. |
| CVE | Identificador público de vulnerabilidade específica. |
| DAST | Teste dinâmico de segurança de aplicação. |
| DDoS | Negação de serviço distribuída. |
| DLP | Data Loss Prevention, controles para reduzir perda/exposição de dados. |
| EDR | Endpoint Detection and Response. |
| FIDO2/WebAuthn | Padrões de autenticação moderna com chaves criptográficas e resistência a phishing. |
| HSTS | Política para exigir HTTPS no navegador. |
| IAM | Identity and Access Management. |
| JWT/JWS/JWE | Token JSON; assinatura e criptografia são conceitos distintos. |
| KEV | Known Exploited Vulnerabilities: catálogo de exploração conhecida mantido pela CISA. |
| Least privilege | Princípio de atribuição da menor permissão necessária. |
| mTLS | TLS com autenticação de cliente e servidor por certificados. |
| RAG | Retrieval-Augmented Generation; LLM usa documentos recuperados. |
| RLS | Row Level Security; políticas do banco em nível de linha. |
| SAST | Análise estática de segurança no código. |
| SBOM | Lista de componentes e dependências de software. |
| SCA | Software Composition Analysis, análise de composição/dependências. |
| SSRF | Server-Side Request Forgery, requisição de saída indevida feita por servidor. |
| SLO | Service Level Objective; meta de nível de serviço. |
| SLSA | Estrutura de níveis para integridade/proveniência de cadeia de suprimentos. |
| STRIDE | Modelo de ameaça: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. |
| WAAP/WAF | Proteção de aplicações web e APIs / Firewall de aplicação web. |
| Zero Trust | Modelo de verificação explícita, privilégio mínimo e redução de confiança implícita. |

---

**Conclusão:** este documento é uma **base extensível de engenharia de segurança** para criação posterior de uma skill. A implementação real deverá separar regras automatizáveis das que dependem de arquitetura e verificação humana, guardar a evidência de cada conclusão e atualizar periodicamente as fontes. Não contém roteiros para ataques destrutivos ou exploração de terceiros.
