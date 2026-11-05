# Security

[![CI](https://github.com/lucianumm/Security/actions/workflows/skill-tests.yml/badge.svg)](https://github.com/lucianumm/Security/actions/workflows/skill-tests.yml)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue.svg)](LICENSE)
![Python 3.10 ou superior](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Skill 1.2.0](https://img.shields.io/badge/skill-1.2.0-24292f)
![507 cenários](https://img.shields.io/badge/cen%C3%A1rios-507-6f42c1)
![136 controles](https://img.shields.io/badge/controles-136-0969da)

**Uma skill defensiva para ler o projeto, investigar vulnerabilidades, propor controles e,
com sua autorização, aplicar correções e testar o resultado.**

A **security-auditor** orienta o agente de IA a entender a arquitetura real do projeto, relacionar
o código ao catálogo de segurança, verificar evidências e contraprovas, priorizar os riscos e
preparar mudanças específicas para a tecnologia utilizada. Depois da sua aprovação do plano e do
diff, o agente implementa o escopo autorizado, executa as verificações disponíveis e registra o
que foi efetivamente corrigido, testado ou deixado pendente.

## Apoie o projeto

<p align="center">
  <img src="security-auditor/assets/me-pague-um-cafe.png" width="240" alt="QR Code Pix para apoiar a manutenção do projeto Security">
  <br>
  <strong>Me pague um Café</strong>
</p>

<p align="center">
  <sub>No aplicativo do seu banco, escolha Pix &gt; Ler QR Code e aponte a câmera.</sub>
</p>

Se a Security ajudou você a revisar e melhorar a segurança do seu projeto, considere apoiar com
um café. A contribuição ajuda a atualizar o catálogo, aprimorar as análises, manter exemplos e
desenvolver correções e testes melhores. O apoio é opcional; o projeto continua disponível sob
[licença MIT](LICENSE).

<details>
<summary><strong>☕ Pix copia e cola — clique para abrir</strong></summary>

Copie a linha inteira abaixo ou use o botão de copiar do bloco. No aplicativo do banco, escolha
**Pix → Copia e Cola**, cole o código e confira o destinatário e o valor antes de confirmar.

```text
00020126580014br.gov.bcb.pix01369c9afabf-3a30-417d-a9e0-801480ca57965204000053039865802BR5924Lucianum Magnum Inacio P6009Sao Paulo62230519daqr1441345083046826304F37E
```

Este é o conteúdo extraído do mesmo QR Code exibido acima. O código não define um valor de
contribuição. A conferência do CRC verifica a integridade do texto; a confirmação dos dados do
pagamento acontece no aplicativo do banco.

</details>

## Navegação

- [O que está incluído](#o-que-esta-incluido)
- [Como a análise funciona](#como-funciona)
- [Instalação e requisitos](#instalacao)
- [Pedidos prontos para usar](#como-usar)
- [Modos e opções](#modos)
- [Cobertura por domínio](#cobertura)
- [Todos os cenários do catálogo](#catalogo-completo)
- [Controles de segurança](#controles)
- [Correções e implementações possíveis](#correcoes)
- [Autorização das mudanças](#autorizacao)
- [Testes e revalidação](#testes)
- [Relatórios e estado persistente](#resultados)
- [Scripts e integração com CI](#scripts)
- [Contribuição e comunidade](#contribuir)
- [Reporte privado de vulnerabilidades](#reporte)
- [Limites da análise](#limites)
- [Licença e créditos](#licenca)

<a id="o-que-esta-incluido"></a>

## O que está incluído

| Componente | Conteúdo |
| --- | --- |
| Skill | [`security-auditor/SKILL.md`](security-auditor/SKILL.md), com modos, fluxo, limites e referências. |
| Catálogo | **507 cenários em 19 domínios**, com precondições, impacto e defesas para revisão. |
| Controles | **136 controles** de governança, identidade, aplicação, APIs, dados, infraestrutura, desenvolvimento e operação. |
| Módulos | **25 módulos** carregados conforme as tecnologias e superfícies relevantes. |
| Evidências | Achados com IDs persistentes, arquivos e linhas, impacto, confiança, contraprovas e testes. |
| Correção | Plano e diff revisáveis, aprovação do lote, implementação autorizada e verificação posterior. |
| Auxiliares | Descoberta local, validação de schemas, cobertura, digests, checagem de aprovação e gate de estado. |
| CI | Templates para GitHub Actions e GitLab CI que precisam ser adaptados e protegidos no projeto consumidor. |
| Comunidade | Licença MIT, código de conduta, guia de contribuição, suporte e templates de issues e PR. |

A fonte original declara 506 cenários, mas suas tabelas contêm **507 entradas reais**. A importação
preserva todas elas e registra a divergência. O catálogo é uma base de revisão pelo agente;
carregar uma entrada não significa ter executado um detector ou confirmado uma vulnerabilidade.

Fonte: [enciclopédia original](security-auditor/references/encyclopedia-v1.0.md) ·
[catálogo estruturado](security-auditor/catalog/encyclopedia.json) ·
[status de implementação](IMPLEMENTATION_STATUS.md).

<a id="como-funciona"></a>

## Como a análise funciona

```text
LER O PROJETO → DESCOBRIR A STACK → MAPEAR ATIVOS E FRONTEIRAS DE CONFIANÇA
      ↓
SELECIONAR CONTROLES E CENÁRIOS APLICÁVEIS → REVISAR CÓDIGO E CONFIGURAÇÃO
      ↓
COLETAR EVIDÊNCIAS → VALIDAR CONTRAPROVAS → PRIORIZAR OS ACHADOS
      ↓
APRESENTAR PLANO, DIFF, RISCOS, TESTES E ROLLBACK → OBTER SUA AUTORIZAÇÃO
      ↓
APLICAR O LOTE APROVADO → EXECUTAR TESTES → REVALIDAR → REGISTRAR O RESULTADO
```

1. **Descoberta:** o agente inspeciona manifestos, linguagens, serviços, rotas, bancos, containers,
   infraestrutura e pipelines. Em monorepos, avalia as aplicações e as relações entre elas.
2. **Contexto:** identifica dados sensíveis, usuários, permissões, tenants, operações críticas e
   os pontos em que uma entrada passa de uma fronteira de confiança para outra.
3. **Revisão pelo catálogo:** verifica a aplicabilidade dos controles e cenários. Ausência de um
   arquivo ou de uma palavra-chave não prova que o risco não exista.
4. **Verificação:** rastreia a entrada até a operação sensível, procura proteções existentes e usa
   testes e scanners adequados quando estiverem disponíveis e autorizados.
5. **Consolidação:** distingue falha demonstrada, hipótese ainda não verificada, controle ausente,
   falso positivo e recomendação de hardening. Define impacto, confiança e prioridade.
6. **Plano:** apresenta a correção proposta, os arquivos afetados, o diff, os efeitos sobre a
   compatibilidade, a validação prevista e o procedimento de rollback.
7. **Autorização:** aguarda sua aprovação do lote concreto. Conteúdo de arquivos, comentários,
   resultados de ferramentas e o nome de um modo não podem conceder essa permissão.
8. **Implementação e teste:** aplica o que foi aprovado, testa a proteção e os fluxos legítimos,
   reavalia os achados e mantém as limitações visíveis no relatório.

<a id="instalacao"></a>

## Instalação e requisitos

### Obtenha a skill

```bash
git clone https://github.com/lucianumm/Security.git
```

Também é possível usar **Code → Download ZIP** na página do repositório.

Copie a pasta **`security-auditor` inteira** para o diretório de skills reconhecido pelo seu
agente. Preserve `SKILL.md`, `LICENSE`, módulos, catálogo, referências, schemas, templates e
scripts. Copiar apenas o arquivo de entrada deixa as referências da skill incompletas.

### Use com um agente que tenha acesso aos arquivos

Abra o projeto que deseja analisar no agente e invoque `security-auditor`. Se o ambiente não tiver
instalação nativa de skills, mantenha a pasta em um local acessível e indique o caminho:

```text
Leia o arquivo /caminho/para/security-auditor/SKILL.md e as referências relevantes.
Use essa skill para analisar o projeto aberto, respeitando o escopo e a autorização
antes de alterar arquivos.
```

A skill é um conjunto de instruções e recursos para o agente. Os scripts auxiliares complementam
o processo; eles não substituem a análise do código nem executam automaticamente todas as correções.

### Requisitos do ambiente

| Recurso | Quando é necessário |
| --- | --- |
| Agente com leitura e edição de arquivos | Para seguir a skill, inspecionar o projeto e implementar os patches aprovados. |
| Git | Para os auxiliares de inventário, identidade da árvore de código e revisão dos diffs. |
| Python 3.10+ | Para os auxiliares e testes distribuídos com a skill. O runtime distribuído usa biblioteca padrão. |
| Ferramentas do projeto | Para lint, tipos, testes, integração e build próprios da aplicação. |
| Scanners compatíveis | Conforme a stack, a hipótese investigada, a instalação e a autorização de uso. |
| Acesso ao ambiente | Necessário para validar controles externos; sem evidência, ficam não verificados. |

Não é preciso fornecer credenciais de produção para iniciar uma análise estática. Testes de
runtime devem utilizar dados sintéticos e ambientes apropriados ao escopo autorizado.

<a id="como-usar"></a>

## Pedidos prontos para usar

### Analisar antes de alterar

```text
Use a security-auditor para ler este projeto e analisar sua segurança com base no
catálogo. Identifique vulnerabilidades e controles necessários, apresente evidências,
arquivos afetados, impacto, contraprovas e um plano com o diff das correções.
Aguarde minha autorização antes de alterar código, dependências, configurações ou testes.
```

### Preparar correções e controles necessários

```text
Use a security-auditor em HARDEN. Analise as superfícies aplicáveis, priorize os riscos
e prepare um lote de correções e controles necessários. Explique compatibilidade,
testes de regressão, ações externas e rollback. Apresente o plano para minha aprovação.
Depois de autorizado, implemente o lote, teste e revalide os achados.
```

### Aprovar um lote já revisado

```text
Autorizo as ações PLAN-0001 e PLAN-0002 do lote apresentado, nos arquivos e no diff
revisados. Aplique essas correções e execute os testes locais descritos no plano.
```

Substitua os IDs pelos que aparecerem na sua análise. A aprovação deve corresponder ao plano
concreto e à versão do código revisada; não use um exemplo de aprovação como consentimento real.

### Rever autorização ou uma área específica

```text
security-auditor TARGETED_AUDIT authorization --scope services/api
```

Também é possível pedir: “revise autenticação e sessões”, “analise os webhooks”, “verifique a
segurança do Docker” ou “audite as ferramentas e o isolamento de tenants do meu agente de IA”.

### Reavaliar depois das mudanças

```text
security-auditor VERIFY
```

Peça os testes realmente executados, o resultado de cada correção, os achados ainda abertos,
as regressões e os controles que dependem de verificação externa.

<a id="modos"></a>

## Modos e opções

As instruções abaixo são pedidos no chat do **agente de IA**, não comandos de um programa CLI.

| Modo | Uso | Alterações no projeto |
| --- | --- | --- |
| `AUDIT` | Diagnóstico completo, evidências e propostas. É o padrão. | Sem patches; relatórios e estado podem ser gravados quando permitido. |
| `AUDIT_AND_FIX` | Análise, plano, correção autorizada, testes e revalidação. | Apenas o lote explicitamente aprovado. |
| `HARDEN` | Também propõe controles necessários que ainda não existem. | Implementação local somente após aprovação e análise de compatibilidade. |
| `VERIFY` | Reavalia achados e procura regressões com as verificações autorizadas. | Não autoriza novos patches ou arquivos de teste por si só. |
| `TARGETED_AUDIT <área>` | Concentra a análise em autenticação, API, Docker ou outro recorte. | Conforme o pedido e a aprovação concreta. |
| `CI_GATE` | Avalia o estado de auditoria contra a política configurada. | Não executa correções nem todos os scanners. |
| `INCIDENT_REVIEW` | Examina evidências de possível comprometimento e preserva as limitações. | Sem contenção ou alteração de produção automática. |

| Opção | Efeito |
| --- | --- |
| `--scope <caminho>` | Limita a análise ao caminho ou componente indicado. |
| `--no-write` | Entrega no chat, sem criar relatórios, estado ou outros arquivos no projeto. |
| `--offline` | Trabalha sem rede; inteligência de vulnerabilidades atualizada pode ficar indisponível. |
| `--incremental` | Analisa mudanças e seus impactos em relação à baseline existente. |
| `--full` | Solicita uma revisão completa do escopo. |
| `--allow-dynamic` | Acompanha a autorização de testes dinâmicos; ainda exige alvo, técnicas e limites definidos. |

<a id="cobertura"></a>

## Cobertura por domínio

A análise seleciona os cenários pertinentes à arquitetura e aos ativos encontrados. Alguns
domínios exigem configurações, artefatos ou evidências que não ficam no repositório.

| Domínio | Cenários | Módulos de referência |
| --- | ---: | --- |
| ENC-D01 — Identidade, autenticação e sessões | 35 | `authentication`, `sessions` |
| ENC-D02 — Autorização e separação de privilégios | 24 | `authorization`, `database` |
| ENC-D03 — Injeção, interpretação e execução de código | 43 | `backend`, `uploads`, `database` |
| ENC-D04 — Web, navegador, HTTP, cache e origens | 35 | `frontend`, `nginx`, `sessions` |
| ENC-D05 — APIs, GraphQL, gRPC, WebSockets e integrações | 29 | `api`, `webhooks` |
| ENC-D06 — Lógica de negócio, automação abusiva e fraude | 25 | `business-logic`, `payments` |
| ENC-D07 — Criptografia, dados e exposição de informações | 27 | `cryptography`, `secrets`, `database`, `logging` |
| ENC-D08 — Redes, transporte, DNS e disponibilidade (DoS/DDoS) | 44 | `cloud`, `nginx`, `monitoring` |
| ENC-D09 — Cloud, infraestrutura, sistema operacional e diretórios | 37 | `cloud`, `secrets` |
| ENC-D10 — Containers, Kubernetes, service mesh e ambientes de execução | 23 | `docker`, `kubernetes` |
| ENC-D11 — Supply chain, Git, dependências e CI/CD | 25 | `supply-chain`, `ci-cd` |
| ENC-D12 — Endpoints, malware, persistência e operações adversárias | 25 | `incident-response`, `extended-surfaces` |
| ENC-D13 — Comunicação, e-mail, engenharia social e identidade organizacional | 23 | `extended-surfaces` |
| ENC-D14 — Aplicações mobile, desktop e dispositivos clientes | 21 | `extended-surfaces` |
| ENC-D15 — IoT, dispositivos, firmware e OT/ICS | 12 | `extended-surfaces` |
| ENC-D16 — IA generativa, LLM, RAG, agentes, ferramentas e MCP | 33 | `ai-security` |
| ENC-D17 — Segurança física, disponibilidade operacional e fator humano | 10 | `backup`, `incident-response`, `extended-surfaces` |
| ENC-D18 — Segurança de memória, compiladores e exploração binária | 22 | `extended-surfaces` |
| ENC-D19 — Redes sem fio, proximidade, navegação e periféricos | 14 | `extended-surfaces` |

Os 25 módulos e o roteiro operacional estão em [`SKILL.md`](security-auditor/SKILL.md). Para
mobile/desktop, firmware/OT, memória, comunicação, redes sem fio e processos físicos/humanos,
consulte também [`extended-surfaces.md`](security-auditor/modules/extended-surfaces.md).

<a id="catalogo-completo"></a>

## Todos os cenários do catálogo

Abra cada domínio para consultar **todas as 507 entradas**, suas precondições e as defesas ou
validações propostas pela enciclopédia. Os IDs `ENC-Dxx-Sxxx` são identificadores locais; não são
IDs oficiais de CWE ou CVE. As linhas de origem estão vinculadas em cada entrada.

Estas são perguntas de revisão e referências defensivas. Elas não representam 507 detectores
automatizados nem uma afirmação de que o projeto auditado possui todas essas falhas. As defesas
devem ser adaptadas à stack, à exposição, aos controles existentes e à autorização recebida.

<details>
<summary><strong>ENC-D01 — Identidade, autenticação e sessões (35 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D01-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L336)<br>**Brute force online** | Sem controle de tentativas, credenciais podem ser adivinhadas repetidamente. | MFA, limites por conta/rede, alertas, respostas uniformes e testes de limites. |
| [ENC-D01-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L337)<br>**Credential stuffing** | Pares usuário/senha vazados são reutilizados em serviços diferentes. | MFA/passkeys, monitoramento de vazamentos, proteção anti-bot, detecção de logins anômalos. |
| [ENC-D01-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L338)<br>**Password spraying** | Mesma senha comum testada contra múltiplas contas, evitando limiares por usuário. | Detecção agregada por origem/campanha, MFA e rate limits multidimensionais. |
| [ENC-D01-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L339)<br>**Ataque de dicionário offline** | Base de hashes vazada pode permitir tentativa de senhas em massa. | Argon2id/scrypt com sal único, parâmetros robustos, pepper protegido quando adotado. |
| [ENC-D01-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L340)<br>**Rainbow tables** | Hash rápido sem salt é passível de comparação com tabelas pré-computadas. | Salt aleatório e hash adaptativo adequado, sem SHA-256 puro. |
| [ENC-D01-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L341)<br>**Credential phishing** | Usuário é induzido a divulgar senha/código em página fraudulenta. | Passkeys/FIDO2, conscientização, monitoramento de domínio, proteção de e-mail. |
| [ENC-D01-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L342)<br>**Adversary-in-the-middle de login** | Proxy fraudulento intercepta sessão ou credencial de autenticação não resistente a phishing. | FIDO2/passkeys, validação de origem, detecção de token/rede anômalos, step-up. |
| [ENC-D01-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L343)<br>**MFA fatigue / push bombing** | Requisições repetidas levam usuário a aprovar indevidamente. | Number matching, limitação de prompts, fatores resistentes a phishing e alertas. |
| [ENC-D01-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L344)<br>**SIM swap** | Controle do número telefônico compromete recuperação ou MFA baseado em SMS. | Preferir passkeys/TOTP/chaves, controles adicionais para recuperação e mudanças. |
| [ENC-D01-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L345)<br>**OTP guessing/replay** | Códigos com entropia ou validação inadequada são adivinhados ou reutilizados. | TTL curto, uso único, limite de tentativas e vinculação de transação. |
| [ENC-D01-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L346)<br>**Bypass de MFA** | Rotas auxiliares, APIs ou fluxos legados dispensam o segundo fator. | Testar cobertura em todos os fluxos, negar sessão parcialmente autenticada. |
| [ENC-D01-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L347)<br>**Account enumeration** | Login, cadastro e reset revelam contas válidas por mensagens ou tempo. | Respostas uniformes, limitar endpoints de descoberta e telemetria. |
| [ENC-D01-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L348)<br>**Reset token prediction** | Token de recuperação previsível ou curto permite tomada de conta. | CSPRNG, uso único, expiração, armazenamento hash e validação no backend. |
| [ENC-D01-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L349)<br>**Reset token leakage** | Links de recuperação aparecem em logs, Referer, analytics ou terceiros. | Remover tokens de telemetria, `Referrer-Policy`, `no-store`, fluxo adequado. |
| [ENC-D01-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L350)<br>**Account recovery abuse** | Suporte ou fluxo de recuperação tem verificação de identidade fraca. | Verificações proporcionais ao risco, rastreamento, notificações e atrasos de segurança quando pertinentes. |
| [ENC-D01-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L351)<br>**Session hijacking** | Cookie ou token é roubado e usado em outro contexto. | TLS, HttpOnly, XSS prevention, revogação, monitoramento de sessão. |
| [ENC-D01-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L352)<br>**Session fixation** | Identificador conhecido pelo atacante persiste após autenticação. | Regenerar sessão no login e alterações de privilégio. |
| [ENC-D01-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L353)<br>**Session prediction** | IDs sequenciais ou gerados por PRNG inadequado permitem adivinhação. | IDs de alta entropia com CSPRNG e testes estatísticos básicos. |
| [ENC-D01-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L354)<br>**Session replay** | Token capturado continua válido indefinidamente ou sem restrições. | Expiração, revogação, rotação, detecção de reuse e sender constraint quando apropriado. |
| [ENC-D01-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L355)<br>**Sessão não invalidada no logout** | Cookie some do browser, mas token segue válido no servidor. | Revogação efetiva e teste de reutilização pós-logout. |
| [ENC-D01-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L356)<br>**Autorização defasada no JWT** | Privilégio foi revogado, porém claims antigos seguem aceitos. | Tokens curtos, políticas servidor, sessão/versionamento e invalidação de eventos. |
| [ENC-D01-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L357)<br>**JWT `alg=none` / confusão algorítmica** | Validador confia em algoritmo não permitido ou confunde chaves. | Allowlist estrita, tipagem de token, biblioteca madura e testes negativos. |
| [ENC-D01-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L358)<br>**JWT `kid`/`jku`/`x5u` manipulation** | Metadados não confiáveis controlam busca de chaves ou URL externa. | JWKS confiável fixado, validação de parâmetros, bloqueio de SSRF. |
| [ENC-D01-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L359)<br>**JWT audience/issuer confusion** | Token destinado a outra aplicação ou emissor é aceito. | Validar `aud`, `iss`, finalidade e tipo do token no receptor. |
| [ENC-D01-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L360)<br>**Refresh token reuse** | Refresh token antigo reaparece após rotação, indicando cópia. | Detecção e revogação de família/dispositivo, logs e resposta. |
| [ENC-D01-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L361)<br>**OAuth authorization code interception** | Código é interceptado ou reusado em fluxo inadequado. | PKCE, HTTPS, redirect URI exata, código curto e uso único. |
| [ENC-D01-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L362)<br>**OAuth redirect URI manipulation** | Redirect permissivo recebe códigos/tokens em destino controlado. | Match exato, destinos registrados, proibir open redirect no fluxo. |
| [ENC-D01-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L363)<br>**OAuth mix-up / token substitution** | Cliente confunde provedores, destinatários ou classes de token. | `iss`, `state`, `nonce` onde aplicável, metadados de issuer e token validation. |
| [ENC-D01-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L364)<br>**OAuth scope escalation** | Escopo não solicitado/consentido ou permissões excedentes são concedidos. | Scopes mínimos, consentimento e autorização servidor por recurso. |
| [ENC-D01-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L365)<br>**OAuth consent phishing** | Aplicação maliciosa solicita consentimento amplo de conta legítima. | App governance, consentimento controlado, auditoria e revogação de grants. |
| [ENC-D01-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L366)<br>**SAML signature wrapping** | Parser e validador selecionam elementos XML diferentes. | Validar o elemento efetivamente consumido, assinatura, issuer, audience e destination. |
| [ENC-D01-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L367)<br>**SAML replay** | Assertion válida é reutilizada por falta de controle de ID/tempo. | `InResponseTo`, janela temporal, cache de assertions usadas e validação de destinatário. |
| [ENC-D01-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L368)<br>**Passkey account-linking confusion** | Credencial é vinculada à conta errada devido a contexto incorreto. | Vincular challenge, RP ID, usuário, operação e estado autenticado. |
| [ENC-D01-S034](security-auditor/references/encyclopedia-v1.0.md?plain=1#L369)<br>**API key leakage** | Chave em Git, front-end, logs ou URL permite chamadas não autorizadas. | Vault, escopos, revogação, secrets scanning e limites de uso. |
| [ENC-D01-S035](security-auditor/references/encyclopedia-v1.0.md?plain=1#L370)<br>**Shared admin credentials** | Ausência de identidade individual impede revogação e atribuição. | Contas nominativas, PAM/JIT e auditoria. |

</details>

<details>
<summary><strong>ENC-D02 — Autorização e separação de privilégios (24 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D02-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L376)<br>**IDOR (Insecure Direct Object Reference)** | Identificador alterado dá acesso a objeto de outra pessoa. | Autorizar propriedade e tenant em todo acesso, não apenas validar ID. |
| [ENC-D02-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L377)<br>**BOLA (Broken Object Level Authorization)** | API verifica login, mas não se usuário pode acessar cada objeto. | Verificação no backend, consultas contextualizadas e testes interusuários. |
| [ENC-D02-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L378)<br>**BFLA (Broken Function Level Authorization)** | Usuário comum consegue invocar função administrativa. | Guards por operação, políticas centralizadas e testes de papéis. |
| [ENC-D02-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L379)<br>**BOPLA (Broken Object Property Level Authorization)** | Campo sensível pode ser lido/modificado sem permissão. | DTOs de resposta/escrita com allowlist e política por atributo. |
| [ENC-D02-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L380)<br>**Horizontal privilege escalation** | Uma conta alcança dados/ações de usuário de mesmo nível. | Políticas por objeto, subject e tenant; testes cruzados. |
| [ENC-D02-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L381)<br>**Vertical privilege escalation** | Usuário de baixo privilégio executa funções administrativas. | RBAC/ABAC/ReBAC no servidor, deny-by-default e segregação. |
| [ENC-D02-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L382)<br>**Forced browsing** | URL interna ou endpoint não exibido no menu é acessível diretamente. | Verificar permissão em cada rota; interface não é controle de segurança. |
| [ENC-D02-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L383)<br>**Tenant escape** | Falta de filtro por `tenant_id` expõe dados de outros clientes. | Tenant derivado da sessão, escopo nas queries, RLS e testes multi-tenant. |
| [ENC-D02-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L384)<br>**Mass assignment** | JSON recebido altera `role`, `isAdmin`, saldo, status ou proprietário. | Schemas explícitos de escrita, jamais espalhar corpo bruto para ORM. |
| [ENC-D02-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L385)<br>**Overposting / underposting** | Campos inesperados ou omitidos alteram lógica/autorização. | Contratos de entrada estritos e autorização por campo. |
| [ENC-D02-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L386)<br>**Insecure default role** | Cadastro recebe privilégios excessivos por configuração padrão. | Role mínimo, revisão de onboarding, teste de novos usuários. |
| [ENC-D02-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L387)<br>**RBAC rule conflict** | Regra ampla sobrepõe restrição específica ou negação. | Avaliação determinística, deny precedence e testes de política. |
| [ENC-D02-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L388)<br>**Client-side role trust** | Permissões são aceitas por parâmetro ou estado do frontend. | Decidir no servidor, assinar contexto apenas quando necessário e verificar fonte. |
| [ENC-D02-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L389)<br>**Admin endpoint exposure** | API administrativa fica pública ou sem proteção adicional. | Separação, rede restrita, SSO/MFA, authorization e logs. |
| [ENC-D02-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L390)<br>**Multi-step authorization bypass** | Fluxo confere permissão no início, mas não no passo final. | Autorizar cada operação final, revalidar estado e ownership. |
| [ENC-D02-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L391)<br>**TOCTOU (check/use race)** | Permissão ou condição muda entre validação e uso. | Transações, locks, verificações atômicas e invariantes no banco. |
| [ENC-D02-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L392)<br>**Authorization caching flaw** | Decisão cacheada é reutilizada entre usuários/tenants. | Cache key contendo principal, tenant, recurso, ação e versão de política. |
| [ENC-D02-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L393)<br>**RLS policy bypass** | Papel com BYPASSRLS ou conexão privilegiada ignora política. | Conexões de aplicação sem superuser, testes do papel real e RLS rigoroso. |
| [ENC-D02-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L394)<br>**File ACL inheritance abuse** | Arquivo herda permissão ampla e fica visível publicamente. | ACL explícita, least privilege e scanner de objetos públicos. |
| [ENC-D02-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L395)<br>**Insecure impersonation** | Suporte assume identidade de cliente sem controle ou rastreio. | Aprovação contextual, tempo limitado, banner, auditoria e controles restritos. |
| [ENC-D02-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L396)<br>**Cross-tenant job/queue confusion** | Worker processa job sob tenant errado por falta de contexto confiável. | Propagar identidade assinada/validada, isolamento e checagem no consumidor. |
| [ENC-D02-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L397)<br>**Confused deputy** | Serviço com privilégios elevados atende pedido de ator não autorizado. | Autorizar ação em nome do principal, delegação restrita e auditável. |
| [ENC-D02-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L398)<br>**Broken access on exports** | PDF/CSV/exportações ignoram filtros da interface. | Aplicar mesma autorização e scoping em jobs assíncronos. |
| [ENC-D02-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L399)<br>**Partial-object exposure** | Endpoint retorna objeto inteiro e frontend esconde campos. | Serialização mínima e teste de payload de rede. |

</details>

<details>
<summary><strong>ENC-D03 — Injeção, interpretação e execução de código (43 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D03-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L405)<br>**SQL Injection (SQLi)** | Entrada concatenada em SQL muda a consulta e pode expor/alterar dados. | Prepared statements, bind parameters, roles restritas e teste SAST/DAST. |
| [ENC-D03-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L406)<br>**SQLi blind/time-based** | Respostas sem dados ainda podem vazar informações via diferenças de comportamento/tempo. | Parametrização em todos os caminhos, erros neutros e monitoramento. |
| [ENC-D03-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L407)<br>**SQLi em ORM/raw query** | Uso indevido de `raw`, interpolação de colunas ou ordenação dinâmica. | Query builders seguros, allowlist de identificadores e revisão de sinks. |
| [ENC-D03-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L408)<br>**NoSQL Injection** | Operadores/objetos inesperados alteram filtros de busca/autenticação. | Validar tipos de JSON, não aceitar operadores arbitrários do usuário. |
| [ENC-D03-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L409)<br>**MongoDB operator injection** | Objeto recebido é interpretado como operador de consulta. | DTO com tipos escalares e parâmetros seguros de driver. |
| [ENC-D03-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L410)<br>**GraphQL injection into backend** | Resolver transforma argumentos em SQL, shell ou chamadas perigosas. | Validação dos resolvers e controles do sink final. |
| [ENC-D03-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L411)<br>**LDAP Injection** | Entrada manipula filtros de diretório e regras de busca. | APIs de filtro com encoding apropriado e restrição de busca. |
| [ENC-D03-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L412)<br>**XPath/XQuery Injection** | Parâmetro altera expressão de consulta XML. | Bind variables e validação de esquema/consulta. |
| [ENC-D03-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L413)<br>**OS Command Injection** | Entrada chega a shell ou comando de sistema. | Evitar shell; usar APIs nativas, argumentos separados e sandbox. |
| [ENC-D03-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L414)<br>**Code Injection / eval** | Conteúdo não confiável vira código interpretado. | Proibir `eval` em dados externos e usar formatos declarativos estritos. |
| [ENC-D03-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L415)<br>**Remote Code Execution (RCE)** | Falha permite execução de instruções em contexto do servidor. | Patches, sandbox, menor privilégio, bloqueio de execução dinâmica e EDR. |
| [ENC-D03-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L416)<br>**Server-Side Template Injection (SSTI)** | Dados controlados são interpretados como template com expressões. | Templates estáticos, autoescape e ausência de avaliação de templates arbitrários. |
| [ENC-D03-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L417)<br>**Expression Language injection** | Linguagem de expressões recebe conteúdo não confiável. | Não executar expressões fornecidas pelo cliente; allowlists e isolamento. |
| [ENC-D03-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L418)<br>**Prototype Pollution (JavaScript)** | Merge de objetos permite contaminar protótipos e lógica posterior. | Bloquear chaves especiais, objetos sem protótipo quando cabível, bibliotecas corrigidas. |
| [ENC-D03-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L419)<br>**Insecure deserialization** | Objetos com tipos/gadgets perigosos são reconstruídos. | Formatos seguros, allowlist de tipos e proibir serialização executável. |
| [ENC-D03-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L420)<br>**PHP object injection** | Dados serializados acionam métodos mágicos/gadgets perigosos. | Não usar `unserialize` em dados externos; validar tipos e remover gadgets. |
| [ENC-D03-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L421)<br>**Java deserialization gadgets** | Deserializador aceita classes/objetos com efeitos colaterais. | ObjectInputFilter, tipos permitidos e formatos neutros. |
| [ENC-D03-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L422)<br>**YAML unsafe load** | Parser instancia objetos ou executa construções indevidas. | Safe loader, schemas estritos e limites. |
| [ENC-D03-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L423)<br>**XML External Entity (XXE)** | Processador XML resolve entidades externas, podendo ler arquivos ou fazer SSRF. | Desabilitar DTD/entities externas e recursos de rede. |
| [ENC-D03-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L424)<br>**XML/XSLT transformation injection** | Transformação permite extensões, leitura ou execução indevida. | Restringir transformadores, esquemas e acesso externo. |
| [ENC-D03-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L425)<br>**Server-Side Includes Injection** | Conteúdo interpretado como diretiva de SSI. | Não avaliar conteúdo de usuário como SSI; restringir configuração. |
| [ENC-D03-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L426)<br>**CRLF Injection** | Quebras de linha são interpretadas em headers, logs ou protocolos. | APIs seguras, rejeição de caracteres de controle, encoding contextual. |
| [ENC-D03-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L427)<br>**HTTP Response Splitting** | Cabeçalho controlado cria resposta HTTP manipulada. | Validar headers e não interpolar entrada em linhas de protocolo. |
| [ENC-D03-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L428)<br>**HTTP Header Injection** | Host, Referer ou campos controlados alteram lógica downstream. | Validar campos de confiança, normalização e allowlists. |
| [ENC-D03-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L429)<br>**Log Injection / log forging** | Texto malicioso cria entradas falsas ou quebra formato da trilha. | Logs JSON estruturados, escaping e limitação de tamanho. |
| [ENC-D03-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L430)<br>**Email header injection** | Entrada com controles altera destinatários ou cabeçalhos SMTP. | APIs de e-mail, validação de endereços e rejeição de CRLF. |
| [ENC-D03-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L431)<br>**CSV/Formula Injection** | Células exportadas executam fórmulas ao abrir planilha. | Neutralizar valores perigosos conforme software de destino. |
| [ENC-D03-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L432)<br>**Regex DoS (ReDoS)** | Expressão com backtracking excessivo consome CPU. | RegEx linear/segura, limites de input e timeout. |
| [ENC-D03-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L433)<br>**HTTP Parameter Pollution (HPP)** | Parâmetros duplicados são interpretados de formas distintas por camadas. | Política única de parsing e rejeição de duplicatas inesperadas. |
| [ENC-D03-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L434)<br>**JSON parser differential** | Proxy e backend interpretam mesmo JSON com regras diferentes. | Canonicalização, parser uniforme e testes de ambiguidades. |
| [ENC-D03-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L435)<br>**Unicode normalization bypass** | Formas Unicode distintas contornam validações ou ACL. | Normalização consistente, IDs canônicos e testes de caracteres equivalentes. |
| [ENC-D03-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L436)<br>**Path Traversal / `../`** | Caminho controlado sai do diretório permitido e acessa arquivos indevidos. | Paths fixos/IDs, canonicalização, isolamento e permissões mínimas. |
| [ENC-D03-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L437)<br>**Local File Inclusion (LFI)** | Parâmetro seleciona arquivo local fora da área autorizada. | Templates fixos, mapeamento por IDs e restrição de diretórios. |
| [ENC-D03-S034](security-auditor/references/encyclopedia-v1.0.md?plain=1#L438)<br>**Remote File Inclusion (RFI)** | Aplicação carrega recurso remoto como código ou conteúdo interpretado. | Proibir inclusão por URL e limitar origens. |
| [ENC-D03-S035](security-auditor/references/encyclopedia-v1.0.md?plain=1#L439)<br>**ZIP Slip** | Arquivo comprimido contém paths que escrevem fora do destino. | Normalizar cada entrada, restringir raiz e evitar symlink abuse. |
| [ENC-D03-S036](security-auditor/references/encyclopedia-v1.0.md?plain=1#L440)<br>**Arbitrary File Upload** | Upload de arquivo executável ou perigoso gera comprometimento. | Armazenamento fora de webroot, tipos validados, renomeação, sandbox/AV. |
| [ENC-D03-S037](security-auditor/references/encyclopedia-v1.0.md?plain=1#L441)<br>**Polyglot file upload** | Arquivo se apresenta como formato inocente e executável em outro parser. | Validar conteúdo real, transcoding e servir como download. |
| [ENC-D03-S038](security-auditor/references/encyclopedia-v1.0.md?plain=1#L442)<br>**Archive / decompression bomb** | Arquivo pequeno expande para consumo enorme de recursos. | Limitar tamanho expandido, arquivos, profundidade e CPU. |
| [ENC-D03-S039](security-auditor/references/encyclopedia-v1.0.md?plain=1#L443)<br>**Image/PDF parser exploit** | Parser vulnerável executa código ou esgota recursos ao processar arquivo. | Atualizações, isolamento, formatos seguros, limites e análise de mídia. |
| [ENC-D03-S040](security-auditor/references/encyclopedia-v1.0.md?plain=1#L444)<br>**SSRF** | Backend acessa URL controlada, alcançando redes internas ou serviços protegidos. | Allowlist, validação DNS/IP na conexão, egress, bloqueio de metadata. |
| [ENC-D03-S041](security-auditor/references/encyclopedia-v1.0.md?plain=1#L445)<br>**Blind SSRF** | Resposta não aparece ao atacante, mas chamada indevida ocorre. | Políticas de saída, logs de rede/DNS e validação de destino. |
| [ENC-D03-S042](security-auditor/references/encyclopedia-v1.0.md?plain=1#L446)<br>**DNS Rebinding** | Endereço aprovado muda para IP interno antes da conexão. | Resolver e conectar a IP validado, checagem pós-resolução e egress. |
| [ENC-D03-S043](security-auditor/references/encyclopedia-v1.0.md?plain=1#L447)<br>**Open Redirect** | Navegação legítima redireciona a destino fraudulento arbitrário. | URLs de destino fixas/allowlist e validação por origem completa. |

</details>

<details>
<summary><strong>ENC-D04 — Web, navegador, HTTP, cache e origens (35 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D04-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L453)<br>**Reflected XSS** | Entrada aparece em resposta HTML sem encoding adequado. | Escape contextual, frameworks seguros, CSP e testes de sinks. |
| [ENC-D04-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L454)<br>**Stored XSS** | Conteúdo persistido executa script para outros usuários. | Sanitização de conteúdo rico e saída codificada contextual. |
| [ENC-D04-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L455)<br>**DOM-based XSS** | JavaScript usa dados não confiáveis em sinks DOM perigosos. | `textContent`, APIs seguras, Trusted Types e CSP. |
| [ENC-D04-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L456)<br>**Mutation XSS (mXSS)** | DOM normalizado pelo navegador converte HTML aparentemente seguro em conteúdo ativo. | Sanitizador atualizado, contexto de saída controlado e testes por navegador. |
| [ENC-D04-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L457)<br>**CSS/Style injection** | Valores CSS inseguros alteram aparência ou provocam vazamentos contextuais. | Restringir estilos a propriedades/valores permitidos. |
| [ENC-D04-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L458)<br>**HTML injection** | Conteúdo externo manipula interface, formulários ou links sem necessariamente executar JS. | Escape HTML, sanitização e CSP. |
| [ENC-D04-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L459)<br>**DOM clobbering** | IDs/names HTML interferem em variáveis e propriedades usadas por scripts. | Evitar busca global implícita, checar tipos e usar referências explícitas. |
| [ENC-D04-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L460)<br>**Clickjacking** | Página é incorporada em frame para induzir cliques invisíveis ou desviados. | CSP `frame-ancestors`, confirmação de ações sensíveis. |
| [ENC-D04-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L461)<br>**Reverse tabnabbing** | Nova aba acessa `window.opener` e redireciona aba de origem. | `rel="noopener noreferrer"` e padrões modernos de abertura. |
| [ENC-D04-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L462)<br>**CSRF** | Browser envia cookies automaticamente em operação forjada de outro contexto. | Token anti-CSRF, Origin/Fetch Metadata, SameSite e métodos corretos. |
| [ENC-D04-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L463)<br>**Client-side CSRF** | JS legítimo é convencido a produzir request malicioso no próprio origin. | Validar dados que compõem URL/ação, permitir destinos fixos. |
| [ENC-D04-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L464)<br>**CORS misconfiguration** | API permite leitura por origem indevida, especialmente com credenciais. | Allowlist exata de origens, `Vary: Origin`, revisão de credentials. |
| [ENC-D04-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L465)<br>**CORS `null` origin trust** | Origem nula é tratada como confiável indiscriminadamente. | Rejeitar origem nula fora de casos explicitamente justificados. |
| [ENC-D04-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L466)<br>**Subdomain takeover** | DNS aponta para serviço externo desalocado que pode ser reivindicado. | Inventário, apagar registros órfãos e verificar posse de serviços. |
| [ENC-D04-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L467)<br>**Cookie tossing / cookie injection** | Subdomínios conseguem plantar cookies em domínio pai. | `__Host-`, evitar Domain amplo, isolamento de subdomínios. |
| [ENC-D04-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L468)<br>**Session cookie theft via XSS** | Script malicioso acessa cookie sem HttpOnly ou atua na sessão autenticada. | HttpOnly e mitigação de XSS; revalidação de ações críticas. |
| [ENC-D04-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L469)<br>**Mixed content** | Recursos HTTP comprometem confidencialidade/integridade de página HTTPS. | HTTPS em toda a cadeia, CSP e HSTS conforme planejamento. |
| [ENC-D04-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L470)<br>**HTTPS stripping** | Navegação é reduzida para conexão sem proteção. | HTTPS obrigatório, HSTS corretamente configurado. |
| [ENC-D04-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L471)<br>**TLS downgrade** | Negociação permite versão/cifra obsoleta. | TLS moderno, configuração e monitoramento. |
| [ENC-D04-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L472)<br>**Certificate validation bypass** | Cliente aceita certificado inválido ou não verifica hostname. | Validação rigorosa, trust store legítima e testes negativos. |
| [ENC-D04-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L473)<br>**Cache poisoning** | Entrada controlada contamina versão cacheada servida a outros usuários. | Cache keys corretas, cabeçalhos canonizados e edge/backend consistentes. |
| [ENC-D04-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L474)<br>**Web cache deception** | Endpoint privado é armazenado como conteúdo público. | Cache-Control apropriado e regras de cache conscientes da autenticação. |
| [ENC-D04-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L475)<br>**Host header poisoning** | Host não validado altera links, redirects, reset de senha ou roteamento. | `Host`/proxy confiáveis, hostname canônico e configuração de forwarded headers. |
| [ENC-D04-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L476)<br>**HTTP request smuggling (CL.TE/TE.CL e variantes)** | Frontend e backend divergem no framing das requisições, misturando tráfego. | Parsers alinhados, atualizações de proxies e testes controlados de protocolo. |
| [ENC-D04-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L477)<br>**HTTP/2 request desync** | Conversão HTTP/2 para HTTP/1 gera interpretação divergente. | Normalização, proxy atualizado e revisão do downgrade. |
| [ENC-D04-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L478)<br>**HTTP/3 edge parser ambiguity** | Implementações divergentes em borda e origem podem causar roteamento inseguro. | Patching, validação e testes de protocolos sob carga controlada. |
| [ENC-D04-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L479)<br>**Request routing ambiguity** | Path ou header ambíguo seleciona backend não previsto. | Canonicalização e matching estritos, remoção de caminhos legados. |
| [ENC-D04-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L480)<br>**Browser storage exfiltration** | Tokens em `localStorage` ou IndexedDB são acessados por scripts comprometidos. | Evitar tokens bearer persistentes acessíveis a JS quando houver opção mais segura. |
| [ENC-D04-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L481)<br>**Service Worker poisoning** | Service worker malicioso persiste e intercepta recursos no escopo. | CSP, segurança da origem, escopo restrito e rotina de atualização/revogação. |
| [ENC-D04-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L482)<br>**Third-party script compromise** | JS de fornecedor carrega na origem e recebe privilégios da página. | Reduzir terceiros, SRI quando viável, CSP, isolamento e monitoramento. |
| [ENC-D04-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L483)<br>**XS-Leaks** | Diferenças em tempo, cache ou comportamento revelam informação cross-origin. | Isolamento de recursos, headers COOP/COEP/CORP conforme arquitetura, respostas uniformes. |
| [ENC-D04-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L484)<br>**Referrer data leakage** | URLs com identificadores/token são enviadas em `Referer` a terceiros. | Não usar secrets em URL, política de referência restrita. |
| [ENC-D04-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L485)<br>**Browser extension compromise** | Extensão com privilégios pode ler/modificar páginas ou dados do usuário. | Gestão de extensões, browser corporativo e minimizar dados expostos. |
| [ENC-D04-S034](security-auditor/references/encyclopedia-v1.0.md?plain=1#L486)<br>**Client-side source map exposure** | Mapas de fonte públicos revelam estruturas internas e ajudam reconhecimento. | Política de publicação e revisão de artefatos, sem segredos no bundle. |
| [ENC-D04-S035](security-auditor/references/encyclopedia-v1.0.md?plain=1#L487)<br>**Error detail disclosure** | Stack traces, dumps e frameworks expõem informações sensíveis. | Erro público mínimo, observabilidade interna com controle de acesso. |

</details>

<details>
<summary><strong>ENC-D05 — APIs, GraphQL, gRPC, WebSockets e integrações (29 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D05-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L493)<br>**REST BOLA** | API retorna qualquer recurso pelo ID sem ownership. | Contextualizar consultas, checar tenant e usuário a cada operação. |
| [ENC-D05-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L494)<br>**REST BFLA** | Método proibido ao papel atual é alcançado por endpoint alternativo. | Política por rota/método e testes por função. |
| [ENC-D05-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L495)<br>**API excessive data exposure** | Endpoint envia campos demais, mesmo se frontend não os exibe. | Modelos explícitos de resposta e minimização de dados. |
| [ENC-D05-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L496)<br>**API mass assignment** | Campos arbitrários do corpo sobrepõem estado sensível. | Schema de escrita com whitelist e separação de DTO/entidade. |
| [ENC-D05-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L497)<br>**Excessive resource consumption** | Paginação, export ou busca consome CPU, memória e banco sem limites. | Quotas por operação/custo, paginação máxima, budgets e circuit breaker. |
| [ENC-D05-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L498)<br>**Shadow API** | Serviço não documentado escapa das políticas de segurança. | API discovery, inventário de gateway e remoção de versões não suportadas. |
| [ENC-D05-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L499)<br>**Deprecated API exposure** | Versão antiga mantém falhas corrigidas nas versões novas. | Deprecar com prazo, bloquear rotas e aplicar patches em todas as versões ativas. |
| [ENC-D05-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L500)<br>**API schema bypass** | Validação na documentação não é aplicada no runtime. | Middleware de schema testado e falha fechada. |
| [ENC-D05-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L501)<br>**Unsafe API consumption** | Resposta de fornecedor externo é confiada como entrada validada. | Verificar assinatura quando disponível, validar schema e tratar como não confiável. |
| [ENC-D05-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L502)<br>**GraphQL deep query** | Consulta profundamente aninhada exige trabalho desproporcional. | Depth, complexity e timeout por operação. |
| [ENC-D05-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L503)<br>**GraphQL alias/fragment abuse** | Aliases/fragments multiplicam resoluções e podem contornar limites ingênuos. | Custo do plano executado, limites de alias e análise de AST. |
| [ENC-D05-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L504)<br>**GraphQL batching abuse** | Múltiplas operações em uma requisição contornam limites por request. | Quotas por operação e por identidade, batching limitado. |
| [ENC-D05-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L505)<br>**GraphQL introspection exposure** | Schema revela superfície de ataque sem necessidade operacional. | Política consciente de introspection; controle de auth e ambientes. |
| [ENC-D05-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L506)<br>**GraphQL field-level authorization** | Campo sensível é consultado sem validação no resolver. | Política por campo e objeto, testes de roles e tenants. |
| [ENC-D05-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L507)<br>**gRPC authorization gaps** | Métodos internos são invocados sem autenticação/autorização. | Interceptors, mTLS conforme arquitetura e policy em cada serviço. |
| [ENC-D05-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L508)<br>**gRPC metadata trust** | Metadata de cliente é usada como identidade sem validação. | Garantir identidade criptograficamente verificável e confiar apenas em proxy autorizado. |
| [ENC-D05-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L509)<br>**WebSocket cross-site hijacking** | Conexão com cookie é iniciada de origem indevida. | Validar `Origin`, autenticação e CSRF contextual para handshake. |
| [ENC-D05-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L510)<br>**WebSocket message authorization** | Auth na abertura não é reavaliada para mensagens/objetos. | Autorizar ação por mensagem, tenant e objeto. |
| [ENC-D05-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L511)<br>**WebSocket flood** | Conexões persistentes, frames ou mensagens excedem recursos. | Limites de conexão/frame, heartbeats, quotas e backpressure. |
| [ENC-D05-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L512)<br>**Webhook spoofing** | Serviço aceita callback sem verificar remetente/integridade. | Assinatura HMAC/assimétrica, comparação constante e segredos rotativos. |
| [ENC-D05-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L513)<br>**Webhook replay** | Evento legítimo é reenviado e processado mais de uma vez. | Identificador de evento, timestamp, tolerância temporal e idempotência. |
| [ENC-D05-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L514)<br>**Webhook SSRF** | Destino fornecido por cliente alcança rede interna. | Destinos permitidos, egress proxy, DNS/IP e limites de protocolo. |
| [ENC-D05-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L515)<br>**API key scope overreach** | Uma chave concede acesso amplo a vários recursos/tenants. | Escopos curtos, restrições por operação, rotação e logs de uso. |
| [ENC-D05-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L516)<br>**API pagination scraping** | Paginação ilimitada permite extração massiva. | Limites, autorização, quotas por custo e detecção de coleta anômala. |
| [ENC-D05-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L517)<br>**Unsafe content-type parsing** | Requisições ambíguas passam por parser diferente do esperado. | Aceitar content-types explícitos, limites de corpo e rejeição de ambiguidades. |
| [ENC-D05-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L518)<br>**API trust of `X-Forwarded-For`** | Cliente forja IP e contorna rate limit/geoblocking. | Configurar proxies confiáveis e extrair IP apenas da cadeia validada. |
| [ENC-D05-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L519)<br>**API enumeration / predictable IDs** | IDs incrementais facilitam descoberta, embora não sejam causa de acesso indevido por si. | Autorização real, rate limiting e IDs opacos quando úteis. |
| [ENC-D05-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L520)<br>**ETag/conditional request leakage** | Metadados de cache/revalidação revelam estado de outro usuário. | Variação por identidade/tenant, `Cache-Control` adequado e testes de cache. |
| [ENC-D05-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L521)<br>**API request replay after network retry** | Retentativas duplicam criação, cobrança ou alteração. | Idempotency keys por operação, transações e consistência de fila. |

</details>

<details>
<summary><strong>ENC-D06 — Lógica de negócio, automação abusiva e fraude (25 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D06-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L527)<br>**Workflow bypass** | Usuário salta etapas obrigatórias de aprovação ou confirmação. | State machine server-side e invariantes nas transições. |
| [ENC-D06-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L528)<br>**Price manipulation** | Cliente altera preço, frete, desconto ou quantidade arbitrariamente. | Preço calculado no servidor e verificação final na transação. |
| [ENC-D06-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L529)<br>**Coupon stacking** | Combinações indevidas de promoções resultam em prejuízo. | Regras atômicas de elegibilidade, limite por usuário/pedido e testes concorrentes. |
| [ENC-D06-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L530)<br>**Voucher/token enumeration** | Códigos previsíveis podem ser descobertos em massa. | Entropia adequada, limites de tentativas, auditoria e validade. |
| [ENC-D06-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L531)<br>**Double spending** | Valor ou crédito é gasto em duas operações concorrentes. | Lock transacional, invariantes de saldo, ledger e idempotência. |
| [ENC-D06-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L532)<br>**Race condition em estoque** | Requisições simultâneas reservam mais do que disponível. | Operações atômicas, locks/constraints no banco e fila apropriada. |
| [ENC-D06-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L533)<br>**TOCTOU no checkout** | Preço, permissão ou estoque muda após validação inicial. | Revalidação em transação final e versões de objeto. |
| [ENC-D06-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L534)<br>**Refund fraud** | Fluxo de estorno permite duplicidade ou destinatário incorreto. | Vincular reembolso à transação original e reconciliar com provedor. |
| [ENC-D06-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L535)<br>**Payment callback spoofing** | Endpoint toma como verdadeiro pagamento declarado pelo cliente. | Verificar evento assinado/status diretamente com provedor, idempotência. |
| [ENC-D06-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L536)<br>**Payment webhook replay** | Notificação repetida gera créditos ou liberação de serviço duplicada. | Deduplicação por ID, event store e transação idempotente. |
| [ENC-D06-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L537)<br>**Insecure payment status trust** | Frontend define compra como paga após redirect. | Confirmar estado em fonte oficial no backend. |
| [ENC-D06-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L538)<br>**Subscription bypass** | Cancelamento, expiração ou trial não revoga direitos no servidor. | Entitlement verificado server-side e eventos consistentes. |
| [ENC-D06-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L539)<br>**Free trial abuse** | Criação massiva de contas contorna limites por usuário. | Anti-abuso proporcional, verificação de identidade contextual e controle de dispositivos. |
| [ENC-D06-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L540)<br>**Carding** | Tentativas automatizadas verificam cartões/credenciais de pagamento. | Provedor compatível, controles antifraude, limites e observabilidade sem guardar dados sensíveis. |
| [ENC-D06-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L541)<br>**Card cracking** | Tentativas de adivinhar atributos de cartões por respostas diferenciadas. | Respostas uniformes, antifraude e bloqueio adaptativo. |
| [ENC-D06-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L542)<br>**Scalping** | Bots capturam estoque/ingressos de disponibilidade limitada. | Filas justas, quotas por comprador, antifraude e controles de reserva. |
| [ENC-D06-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L543)<br>**Inventory denial** | Bots prendem estoques em carrinhos sem comprar. | Reserva com TTL, limites por usuário e recuperação automática. |
| [ENC-D06-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L544)<br>**Scraping massivo** | Coleta automatizada amplia exposição/custo de dados. | Auth, quotas, paginação, rate limit por custo e monitoramento. |
| [ENC-D06-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L545)<br>**Account creation abuse** | Contas artificiais viabilizam spam, fraude ou consumo de bônus. | Controles de risco, verificação, rate limit e prevenção de abuso. |
| [ENC-D06-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L546)<br>**Fake reviews/ratings** | Usuários ou bots manipulam reputação e ranking. | Detecção comportamental, moderação e limites de avaliações. |
| [ENC-D06-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L547)<br>**Referral abuse** | Referências artificiais geram benefícios indevidos. | Identificar autopatrocínio, loops, vínculos e pagamento de incentivo verificado. |
| [ENC-D06-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L548)<br>**Search/ranking manipulation** | Volume artificial distorce recomendação, busca ou métricas. | Sinais antifraude, separação de métricas e auditoria. |
| [ENC-D06-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L549)<br>**Marketplace account takeover** | Conta legítima é usada para desviar saque ou alterar recebedor. | Passkey/MFA, step-up em mudanças financeiras e janela de análise. |
| [ENC-D06-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L550)<br>**Data export abuse** | Usuário legítimo aciona exportações em massa além do necessário. | Quotas, justificativas, aprovação e detecção de padrões atípicos. |
| [ENC-D06-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L551)<br>**Time-of-check business logic flaw** | Elegibilidade é verificada sob estado antigo e aplicada posteriormente. | Checagem final autoritativa na mesma transação. |

</details>

<details>
<summary><strong>ENC-D07 — Criptografia, dados e exposição de informações (27 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D07-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L557)<br>**Plaintext credentials** | Credenciais ficam em texto claro em banco, código ou backup. | Hash apropriado para senha, secret manager, secrets scanning e rotação. |
| [ENC-D07-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L558)<br>**Weak password hashing** | MD5/SHA rápido permite tentativa offline eficiente após vazamento. | Argon2id/scrypt ou equivalente aprovado com parâmetros atualizados. |
| [ENC-D07-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L559)<br>**Hardcoded cryptographic key** | Chave é publicada em código, pacote ou binário cliente. | Gerenciar segredos externamente e rotacionar material exposto. |
| [ENC-D07-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L560)<br>**Insufficient entropy** | Tokens, nonces ou chaves gerados de fonte previsível. | CSPRNG da plataforma e revisão de inicialização/entropia. |
| [ENC-D07-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L561)<br>**Nonce/IV reuse** | Reutilização incorreta compromete confidencialidade/integridade de cifras específicas. | Geração e unicidade por chave, bibliotecas AEAD corretas. |
| [ENC-D07-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L562)<br>**ECB mode information leakage** | Blocos iguais de dados produzem padrões reconhecíveis. | Usar modos autenticados modernos, não ECB para dados confidenciais. |
| [ENC-D07-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L563)<br>**CBC padding oracle** | Erros/timing de padding revelam informações em sistemas vulneráveis. | AEAD, rejeição uniforme e remoção de protocolos legados frágeis. |
| [ENC-D07-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L564)<br>**Cryptographic downgrade** | Compatibilidade permite aceitar protocolo ou algoritmo vulnerável. | Política de algoritmos permitidos, versões mínimas e negociação segura. |
| [ENC-D07-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L565)<br>**Weak RSA/ECC parameters** | Tamanho, curva ou implementação inadequados enfraquecem assinaturas/segredo. | Parâmetros atuais reconhecidos, bibliotecas revisadas, KMS. |
| [ENC-D07-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L566)<br>**Signature validation bypass** | Aplicação não valida assinatura ou aceita chave fornecida pelo atacante. | Verificação completa da cadeia de confiança, algoritmo, finalidade e contexto. |
| [ENC-D07-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L567)<br>**Certificate expiry/outage** | Expiração de certificado interrompe comunicação ou incentiva bypass inseguro. | Renovação automatizada, alertas e testes de falha segura. |
| [ENC-D07-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L568)<br>**Improper TLS validation** | Serviço aceita hostname ou CA indevida. | Verificação completa de TLS, testes de certificado inválido. |
| [ENC-D07-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L569)<br>**Timing side channel** | Diferença de tempo revela token, segredo ou estado. | Comparações apropriadas, respostas consistentes e análise contextual. |
| [ENC-D07-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L570)<br>**Compression side channel** | Compressão de dados secretos com entradas controladas pode revelar padrões. | Evitar mistura de segredo e entrada atacante em compressão observável. |
| [ENC-D07-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L571)<br>**Secret in URL** | Tokens aparecem em logs, histórico, Referer e ferramentas intermediárias. | Usar cabeçalhos/canais adequados, `no-store` e redação de logs. |
| [ENC-D07-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L572)<br>**Secret in build artifacts** | `.env`, source maps ou cache de pipeline vazam credenciais. | Regras de empacotamento, scanners e controle de acesso a artefatos. |
| [ENC-D07-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L573)<br>**Public database exposure** | Banco ou dump é acessível pela Internet ou bucket público. | Rede privada, IAM mínimo, autenticação e scanning de exposição. |
| [ENC-D07-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L574)<br>**Backup exposure** | Cópias não criptografadas ou públicas revelam dados históricos. | Criptografia, backup imutável, ACL restrita e inventário. |
| [ENC-D07-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L575)<br>**Data remanence** | Dados permanecem em mídia, snapshots ou objetos antigos após descarte. | Lifecycle, destruição criptográfica quando aplicável e política de retenção. |
| [ENC-D07-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L576)<br>**Cross-tenant leakage** | Consulta, cache, fila ou storage retorna informação de outro tenant. | Escopo de dados, RLS, isolamento de chaves de cache e testes cruzados. |
| [ENC-D07-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L577)<br>**Sensitive debug logs** | Exceções e logs contêm senha, CPF, tokens ou dados financeiros. | Redaction, logging schema e inspeção de ambientes produtivos. |
| [ENC-D07-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L578)<br>**Excessive data retention** | Informações antigas permanecem sem finalidade ou controle. | Classificação, retenção por finalidade e exclusão programada. |
| [ENC-D07-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L579)<br>**Misconfigured object storage** | Bucket permite leitura, listagem ou escrita pública indevida. | Block public access, políticas mínimas e auditoria contínua. |
| [ENC-D07-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L580)<br>**Insecure presigned URL** | URL assinada dura demais, concede escopo excessivo ou é exposta. | Prazo curto conforme operação, escopo restrito e rastreamento. |
| [ENC-D07-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L581)<br>**API error disclosure** | Mensagem de exceção retorna consulta SQL, paths ou stack trace. | Resposta pública genérica e observabilidade protegida. |
| [ENC-D07-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L582)<br>**Data poisoning through ingestion** | Fonte externa contamina dados usados em decisões/relatórios. | Proveniência, validação, trilha de alteração e revisão de integridade. |
| [ENC-D07-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L583)<br>**Integrity check omitted** | Artefato ou dado crítico é processado sem verificação de origem. | Assinatura/MAC ou checksum de fonte confiável conforme caso. |

</details>

<details>
<summary><strong>ENC-D08 — Redes, transporte, DNS e disponibilidade (DoS/DDoS) (44 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D08-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L591)<br>**Volumetric DDoS** | Alto volume de tráfego satura link, backbone, edge ou origem. | Mitigação upstream/Anycast/CDN, scrubbing, runbook e monitoramento. |
| [ENC-D08-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L592)<br>**UDP flood** | Tráfego UDP excessivo consome capacidade de transporte ou processamento. | Filtragem upstream, ACL e mitigação L3/L4 no provedor. |
| [ENC-D08-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L593)<br>**TCP SYN flood** | Excesso de handshakes incompletos consome estados de conexão. | SYN cookies, proteção L4, tuning e mitigação upstream. |
| [ENC-D08-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L594)<br>**TCP connection exhaustion** | Conexões numerosas ou persistentes esgotam descritores e workers. | Limits por origem, backlog, timeouts e balanceamento. |
| [ENC-D08-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L595)<br>**ICMP flood** | ICMP em volume elevado consome banda ou CPU. | Políticas ICMP adequadas e mitigação upstream, sem bloquear diagnóstico indiscriminadamente. |
| [ENC-D08-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L596)<br>**DNS amplification/reflection** | Respostas DNS maiores que consultas refletem tráfego à vítima. | Proteção DDoS, BCP38/anti-spoofing e evitar recursão aberta. |
| [ENC-D08-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L597)<br>**NTP amplification** | Serviço NTP mal configurado é usado para reflexão/amplificação. | Desativar funções abusáveis, atualização, restrições e anti-spoofing. |
| [ENC-D08-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L598)<br>**Memcached amplification** | Instância UDP exposta é abusada como amplificador. | Bloquear UDP público, isolar serviço e atualizar software. |
| [ENC-D08-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L599)<br>**SSDP/CLDAP amplification** | Protocolos de descoberta/diretório são usados como refletores. | Restringir exposição, filtrar tráfego e mitigação na borda. |
| [ENC-D08-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L600)<br>**HTTP GET/POST flood** | Volume de requisições esgota aplicação, cache ou banco. | WAF/WAAP, cache, rate limits por custo, quotas e autoscaling com orçamento. |
| [ENC-D08-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L601)<br>**Slowloris / slow HTTP** | Conexões enviam dados lentamente e prendem recursos. | Timeout de leitura, tamanho de cabeçalho, limites de conexão e proxy robusto. |
| [ENC-D08-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L602)<br>**Slow POST/body trickle** | Upload extremamente lento ocupa sockets/workers. | Timeout por taxa mínima, limites de body e controle de conexões. |
| [ENC-D08-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L603)<br>**TLS handshake flood** | Excesso de handshakes provoca custo criptográfico. | Edge TLS offload, limites, mitigação L4/L7 e capacidade. |
| [ENC-D08-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L604)<br>**HTTP/2 stream exhaustion** | Exploração de streams ou resets causa carga desproporcional. | Proxies corrigidos, limites de streams e recursos, mitigação edge. |
| [ENC-D08-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L605)<br>**HTTP/3 QUIC flood** | Tráfego e estados QUIC em volume excedem capacidade do serviço. | Edge atualizado, quotas de conexão e mitigação no provedor. |
| [ENC-D08-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L606)<br>**DNS query flood** | Consultas massivas degradam DNS autoritativo. | Anycast DNS, proteção especializada, redundância e monitoramento. |
| [ENC-D08-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L607)<br>**DNS random-subdomain attack** | Consultas a subdomínios inexistentes forçam lookups excessivos. | Proteção DNS, cache negativo e controles de autoridade. |
| [ENC-D08-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L608)<br>**NXDOMAIN flood** | Respostas negativas em massa pressionam resolutores e DNS. | Filtragem, cache negativo e capacidade resiliente. |
| [ENC-D08-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L609)<br>**Application expensive-query DoS** | Busca, relatório ou ordenação pesada causa consumo extremo. | Índices, timeout, paginação, orçamento por consulta e quotas. |
| [ENC-D08-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L610)<br>**Regex DoS** | Padrão regex gera backtracking de custo elevado. | Revisão das regex, engine adequada e limites de input/CPU. |
| [ENC-D08-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L611)<br>**Decompression bomb DoS** | Arquivo compactado consome espaço/memória desproporcional. | Limits de descompressão, sandbox e tempo máximo. |
| [ENC-D08-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L612)<br>**JSON/XML depth bomb** | Estrutura recursiva sobrecarrega parser ou memória. | Limites de profundidade e tamanho, parsers seguros. |
| [ENC-D08-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L613)<br>**Queue flooding** | Mensagens acima da capacidade acumulam backlog e atrasam serviços. | Quotas, backpressure, DLQ, prioridade e métricas. |
| [ENC-D08-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L614)<br>**Log flooding** | Eventos excessivos esgotam disco/ingestão e ocultam incidentes. | Limites, particionamento, retenção e alertas de volume. |
| [ENC-D08-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L615)<br>**Cache bypass flood** | Requisições variáveis impedem cache e atingem origem. | Normalização, cache keys, políticas edge e proteção de origin. |
| [ENC-D08-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L616)<br>**Origin IP discovery** | Ataque ignora CDN e acessa IP real do origin. | Firewall permitindo somente proxy legítimo, inventário e proteção DNS. |
| [ENC-D08-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L617)<br>**Botnet distributed low-rate attack** | Tráfego baixo por IP, alto no agregado, contorna limites simples. | Detecção comportamental, identidade, reputação e regras por custo. |
| [ENC-D08-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L618)<br>**Carpet-bombing DDoS** | Tráfego espalhado por muitos IPs do mesmo prefixo dificulta detecção local. | Defesa de provedor, visibilidade em prefixo e planejamento de roteamento. |
| [ENC-D08-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L619)<br>**Application-layer amplification** | Uma requisição desencadeia centenas de operações no backend. | Budget de fan-out, limites de dependências, cache e circuit breaker. |
| [ENC-D08-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L620)<br>**Retry storm** | Retentativas simultâneas ampliam uma falha transitória. | Exponential backoff com jitter, idempotência, circuit breaker. |
| [ENC-D08-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L621)<br>**Thundering herd** | Muitos clientes recomputam mesmo dado após expiração simultânea. | Cache jitter, stale-while-revalidate, single-flight. |
| [ENC-D08-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L622)<br>**Resource starvation** | Uma carga monopoliza CPU, memória, conexões ou threads. | Isolamento de pools, quotas por tenant e prioridades. |
| [ENC-D08-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L623)<br>**DNS spoofing/cache poisoning** | Respostas DNS fraudulentas direcionam tráfego a destino incorreto. | DNSSEC quando aplicável, resolvers confiáveis e proteção operacional. |
| [ENC-D08-S034](security-auditor/references/encyclopedia-v1.0.md?plain=1#L624)<br>**ARP spoofing** | Ator em rede local altera resolução IP/MAC para interceptação. | Segmentação, DAI, segurança de switch, criptografia ponta a ponta. |
| [ENC-D08-S035](security-auditor/references/encyclopedia-v1.0.md?plain=1#L625)<br>**Man-in-the-middle (MITM)** | Ator intermediário intercepta/modifica comunicação sem validação adequada. | TLS válido, autenticação de pares e segmentação. |
| [ENC-D08-S036](security-auditor/references/encyclopedia-v1.0.md?plain=1#L626)<br>**BGP hijack / route leak** | Anúncio incorreto ou malicioso redireciona ou interrompe rotas IP. | RPKI/ROA, monitoramento BGP e coordenação com operadoras. |
| [ENC-D08-S037](security-auditor/references/encyclopedia-v1.0.md?plain=1#L627)<br>**DHCP spoofing** | Servidor falso entrega gateway/DNS malicioso em rede local. | DHCP snooping, NAC e segmentação. |
| [ENC-D08-S038](security-auditor/references/encyclopedia-v1.0.md?plain=1#L628)<br>**Rogue Wi-Fi / evil twin** | Rede sem fio falsa captura ou redireciona tráfego. | WPA3/802.1X, validação de certificado e educação. |
| [ENC-D08-S039](security-auditor/references/encyclopedia-v1.0.md?plain=1#L629)<br>**DNS tunneling** | DNS é usado como canal encoberto de comunicação/exfiltração. | Egress DNS controlado, detecção de padrões e listas aprovadas. |
| [ENC-D08-S040](security-auditor/references/encyclopedia-v1.0.md?plain=1#L630)<br>**Network scanning/reconnaissance** | Serviços expostos e versões são enumerados para identificar oportunidades. | Minimizar superfície, firewall, inventário e logs de sondagem. |
| [ENC-D08-S041](security-auditor/references/encyclopedia-v1.0.md?plain=1#L631)<br>**IP spoofing** | Origem de pacote/cabeçalho é falsificada para abuso ou bypass. | BCP38, validação de proxy e não confiar em headers do cliente. |
| [ENC-D08-S042](security-auditor/references/encyclopedia-v1.0.md?plain=1#L632)<br>**Port/service exposure** | Administração e bancos acessíveis à Internet aumentam risco. | Private networking, ACL, VPN/ZTNA, autenticação e patching. |
| [ENC-D08-S043](security-auditor/references/encyclopedia-v1.0.md?plain=1#L633)<br>**VPN credential compromise** | Acesso remoto com credencial roubada permite intrusão. | MFA FIDO2, postura de dispositivo, restrições, logs e revogação. |
| [ENC-D08-S044](security-auditor/references/encyclopedia-v1.0.md?plain=1#L634)<br>**DNS rebinding against local services** | Domínio controlado passa a resolver para serviços internos do browser/backend. | Host/origin validation, egress e bloqueio de endereços internos. |

</details>

<details>
<summary><strong>ENC-D09 — Cloud, infraestrutura, sistema operacional e diretórios (37 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D09-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L640)<br>**Public cloud storage exposure** | Bucket ou arquivo privado é compartilhado publicamente. | Block public access, IAM e scanning contínuo. |
| [ENC-D09-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L641)<br>**Cloud IAM privilege escalation** | Políticas permitem criar roles, anexar permissões ou assumir papel amplo. | IAM mínimo, deny guardrails, SCP/organização e revisão de caminhos de escalada. |
| [ENC-D09-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L642)<br>**Overly broad trust policy** | Identidades externas podem assumir roles sem restrições suficientes. | Restringir principal, condições de audiência, subject e origem. |
| [ENC-D09-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L643)<br>**Cloud credential theft** | Keys long-lived são vazadas e usadas por terceiro. | OIDC/workload identity, credenciais efêmeras, secrets scanning e rotação. |
| [ENC-D09-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L644)<br>**Metadata token theft** | SSRF ou processo local acessa credenciais do metadata service. | IMDSv2 quando aplicável, isolamento, egress e roles mínimas. |
| [ENC-D09-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L645)<br>**Exposed management console** | Interfaces de cloud/hipervisor ficam públicas ou sem MFA. | SSO forte, MFA FIDO2, IP/ZTNA, auditoria. |
| [ENC-D09-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L646)<br>**Security group misconfiguration** | Porta administrativa/DB é aberta para `0.0.0.0/0` sem necessidade. | Regras mínimas, IaC scanning e verificações em runtime. |
| [ENC-D09-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L647)<br>**Cloud logging disabled** | Eventos maliciosos não são rastreáveis por falta de trilhas. | Auditar configuração central, retenção protegida e alertas de desativação. |
| [ENC-D09-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L648)<br>**Snapshot/data volume theft** | Snapshots e discos são compartilhados sem autorização. | Controle de ACL/compartilhamento, criptografia e auditoria. |
| [ENC-D09-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L649)<br>**Serverless function abuse** | Função exposta ou com IAM elevado executa ações indevidas. | Auth, limite de invocação, IAM mínimo e egress controls. |
| [ENC-D09-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L650)<br>**Serverless event injection** | Eventos não confiáveis acionam lógica privilegiada. | Schema, autenticidade do evento, deduplicação e mínimo privilégio. |
| [ENC-D09-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L651)<br>**Cloud cost exhaustion** | Recursos sob demanda geram despesa enorme por abuso. | Budgets, quotas, alertas e rate limit de operações custosas. |
| [ENC-D09-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L652)<br>**Cross-account confused deputy** | Serviço assume acesso a conta errada por relação de confiança ampla. | Condições como external ID/subject e escopos apropriados ao fornecedor. |
| [ENC-D09-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L653)<br>**Instance/VM escape** | Falha de hipervisor permite escapar isolamento da instância. | Patch de hypervisor, isolamento e estratégia de blast radius. |
| [ENC-D09-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L654)<br>**Privilege escalation via sudo** | Sudoers, binários ou serviços permitem subir privilégios. | Hardening, sudo mínimo, patch e revisão de permissões. |
| [ENC-D09-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L655)<br>**SUID/SGID abuse** | Binários privilegiados inseguros são usados para elevar direitos. | Revisão de SUID, patching, montagens `nosuid` onde viável. |
| [ENC-D09-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L656)<br>**Writable service executable** | Conta não privilegiada altera binário iniciado com maior privilégio. | ACL e propriedade corretas, EDR e revisão de serviços. |
| [ENC-D09-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L657)<br>**Unquoted service path** | Caminho de execução ambíguo pode iniciar binário não autorizado. | Configuração correta, hardening de serviços e ACL. |
| [ENC-D09-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L658)<br>**DLL search order hijacking** | Dependência dinâmica é carregada de diretório controlado. | Paths absolutos, assinaturas, ACL e carga segura de bibliotecas. |
| [ENC-D09-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L659)<br>**PATH hijacking** | Executável de diretório não confiável substitui ferramenta esperada. | Paths absolutos e ambiente sanitizado. |
| [ENC-D09-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L660)<br>**Cron/systemd persistence** | Agendadores ou serviços são usados para execução persistente. | Auditoria de tarefas, ACL, EDR e monitoramento de mudanças. |
| [ENC-D09-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L661)<br>**SSH key theft** | Chaves privadas expostas permitem acesso remoto. | Agentes protegidos, passphrases, rotação e controle de acessos. |
| [ENC-D09-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L662)<br>**Default credentials** | Appliance/serviço mantém credenciais de fábrica. | Credenciais únicas, desabilitar padrão e inventário. |
| [ENC-D09-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L663)<br>**Exposed admin dashboards** | Dashboards internos ficam acessíveis sem controle forte. | ZTNA/VPN, SSO, MFA, autorização e inventário. |
| [ENC-D09-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L664)<br>**Patch management gap** | Serviço vulnerável permanece exposto após correção do fornecedor. | Inventário, patch SLO, KEV-first e controles compensatórios. |
| [ENC-D09-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L665)<br>**End-of-life components** | Software sem suporte acumula falhas sem correção. | Substituição planejada e isolamento temporário rigoroso. |
| [ENC-D09-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L666)<br>**Directory/AD password attack** | Senhas fracas ou expostas possibilitam comprometimento de domínio. | MFA, hardening AD, contas privilegiadas separadas e monitoramento. |
| [ENC-D09-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L667)<br>**Kerberoasting** | Tickets de serviço podem permitir tentativas offline contra senhas fracas. | Senhas longas/gerenciadas, gMSA, privilégios mínimos, monitoramento. |
| [ENC-D09-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L668)<br>**AS-REP roasting** | Contas com pré-autenticação desativada expõem material a ataque offline. | Habilitar preauth, senhas fortes, auditoria do AD. |
| [ENC-D09-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L669)<br>**Pass-the-hash** | Hash roubado é usado como credencial em protocolos vulneráveis. | Credential Guard, reduzir NTLM, segmentação e isolamento de administradores. |
| [ENC-D09-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L670)<br>**Pass-the-ticket** | Tickets Kerberos roubados são reutilizados para acessar serviços. | Proteção de credenciais, expiração, EDR e Kerberos hardening. |
| [ENC-D09-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L671)<br>**NTLM relay** | Credenciais de desafio-resposta são encaminhadas a serviços sem proteção adequada. | SMB signing, EPA, bloquear NTLM onde possível, segmentação. |
| [ENC-D09-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L672)<br>**Lateral movement through RDP/SMB** | Conta comprometida alcança outros hosts e eleva impacto. | Segmentação, MFA/JIT, PAM, EDR e redução de serviços. |
| [ENC-D09-S034](security-auditor/references/encyclopedia-v1.0.md?plain=1#L673)<br>**Persistence via identity provider** | Ator malicioso cria credenciais, app registrations ou grants persistentes. | Auditoria IAM/IdP, revisões de consentimentos e alertas de criação. |
| [ENC-D09-S035](security-auditor/references/encyclopedia-v1.0.md?plain=1#L674)<br>**SaaS OAuth token compromise** | Token com permissões amplas permite exportar dados de SaaS. | App governance, DLP, scope mínimo, monitoramento e revogação. |
| [ENC-D09-S036](security-auditor/references/encyclopedia-v1.0.md?plain=1#L675)<br>**Cloud object version manipulation** | Versionamento/backups são alterados para ocultar ou destruir dados. | Imutabilidade, MFA-delete quando pertinente, least privilege. |
| [ENC-D09-S037](security-auditor/references/encyclopedia-v1.0.md?plain=1#L676)<br>**Remote management abuse** | Ferramentas legítimas de administração são usadas por invasor. | Allowlist de software, auditoria de sessões e controles JIT. |

</details>

<details>
<summary><strong>ENC-D10 — Containers, Kubernetes, service mesh e ambientes de execução (23 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D10-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L682)<br>**Container running as root** | Processo privilegiado amplia impacto de falhas da aplicação. | Non-root, `runAsNonRoot`, usuário dedicado e capability drop. |
| [ENC-D10-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L683)<br>**Privileged container** | Pod/container com privilégios excessivos pode alcançar host. | Proibir privileged, usar Pod Security e admission policies. |
| [ENC-D10-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L684)<br>**Docker socket exposure** | Processo com acesso ao socket Docker pode controlar hosts/containers. | Não montar socket em workload não confiável; isolamento. |
| [ENC-D10-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L685)<br>**HostPath mount abuse** | Montagem de diretórios críticos do host rompe isolamento. | Restringir volumes, validar paths e admission controls. |
| [ENC-D10-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L686)<br>**Container escape** | Falha de kernel/runtime permite acesso fora do container. | Atualização, sandbox, seccomp, LSM e mínimo privilégio. |
| [ENC-D10-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L687)<br>**Kubernetes RBAC wildcard** | Service account possui verbos/recursos amplos demais. | RBAC mínimo, revisar `*`, namespaces e impersonation. |
| [ENC-D10-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L688)<br>**Service account token exposure** | Token montado em pod sem necessidade é extraído. | `automountServiceAccountToken: false` quando possível; tokens projetados. |
| [ENC-D10-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L689)<br>**Kubernetes API public exposure** | API server ou etcd expostos facilitam acesso indevido. | Endpoints privados, controle de rede, autenticação e auditoria. |
| [ENC-D10-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L690)<br>**Etcd data disclosure** | Segredos/dados de cluster acessíveis por configuração inadequada. | Criptografia em repouso, ACL e proteção da rede de controle. |
| [ENC-D10-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L691)<br>**Kubernetes secret misuse** | Secrets em manifestos/Git/logs tornam credenciais recuperáveis. | Secret manager, criptografia, RBAC e rotação. |
| [ENC-D10-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L692)<br>**Namespace trust confusion** | Namespace é tratado como fronteira de segurança suficiente. | NetworkPolicy, RBAC, admission, policies e isolamento de workloads. |
| [ENC-D10-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L693)<br>**Missing NetworkPolicy** | Todos os pods podem comunicar-se desnecessariamente. | Default-deny ingress/egress e políticas específicas. |
| [ENC-D10-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L694)<br>**Malicious admission controller** | Webhook de admissão comprometido pode alterar workloads. | Proteger webhook, certificado, revisões e privilégio mínimo. |
| [ENC-D10-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L695)<br>**Image tag mutability** | Imagem `latest` muda sem revisão e executa código inesperado. | Pin por digest, assinatura e processo de promoção. |
| [ENC-D10-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L696)<br>**Vulnerable base image** | Biblioteca ou sistema antigo contém CVE explorável. | Base mínima, patch automatizado e scanning contínuo. |
| [ENC-D10-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L697)<br>**Build secret leakage** | Secrets acabam em layer, histórico ou cache de imagem. | BuildKit secrets, multi-stage, inspeção de layers e rotação. |
| [ENC-D10-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L698)<br>**Insecure container registry** | Imagens podem ser substituídas ou publicadas por atores indevidos. | IAM, assinatura, namespaces de publicação e trilha de auditoria. |
| [ENC-D10-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L699)<br>**Pod resource exhaustion** | Containers sem limites podem prejudicar outros tenants. | Requests/limits, quotas, prioridades e nós isolados. |
| [ENC-D10-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L700)<br>**Sidecar/service-mesh trust gaps** | Identidade mTLS existe, mas autorização por método/recurso é ausente. | AuthZ explícita por serviço, mTLS e policy testing. |
| [ENC-D10-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L701)<br>**Insecure debug/exec endpoint** | Ferramenta de debug permite shell em ambiente sensível. | Proteger acesso, desabilitar em produção e monitorar invocações. |
| [ENC-D10-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L702)<br>**Insecure CRD/operator** | Controlador aceita configurações que resultam em ação privilegiada. | Validação de CRD, RBAC mínimo, admissão e revisão do operador. |
| [ENC-D10-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L703)<br>**CI runner inside cluster compromise** | Runner de build comprometido obtém service accounts/segredos do cluster. | Isolamento de runners, identidades distintas e deploy controlado. |
| [ENC-D10-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L704)<br>**Multi-tenant cluster breakout** | Um tenant obtém recursos de outro por RBAC, rede ou configuração. | Isolamento forte por conta/cluster quando risco exige, controles por camada. |

</details>

<details>
<summary><strong>ENC-D11 — Supply chain, Git, dependências e CI/CD (25 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D11-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L710)<br>**Dependency confusion** | Registry resolve pacote externo com nome interno e executa código não confiável. | Namespace privado, configurações de registry e políticas de resolução. |
| [ENC-D11-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L711)<br>**Typosquatting de pacote** | Pacote com nome semelhante a dependência legítima contém código malicioso. | Revisão de dependência, reputação, lockfile e registry aprovado. |
| [ENC-D11-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L712)<br>**Malicious maintainer/update** | Nova versão de pacote confiável adiciona código nocivo. | SCA, release review, pinning e monitoramento de proveniência. |
| [ENC-D11-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L713)<br>**Transitive dependency compromise** | Dependência indireta traz vulnerabilidade ou comportamento malicioso. | SBOM, análise transitiva e atualização controlada. |
| [ENC-D11-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L714)<br>**Package install-script abuse** | Script de instalação executa ações inesperadas durante build. | Restringir scripts, sandbox de build e revisão de pacotes. |
| [ENC-D11-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L715)<br>**Compromised package registry** | Artefato baixado não corresponde à versão confiável esperada. | Hash/assinatura, mirror confiável e provenance. |
| [ENC-D11-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L716)<br>**Source repository takeover** | Conta/token comprometido modifica código ou releases. | MFA FIDO2, branch protection, revisão e signing. |
| [ENC-D11-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L717)<br>**Compromised CI/CD token** | Token de pipeline permite publicar ou acessar produção. | OIDC de curta duração, escopos mínimos e ambiente isolado. |
| [ENC-D11-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L718)<br>**Poisoned pipeline execution** | PR/workflow não confiável executa no contexto com secrets. | Separar contextos, restrição de eventos e revisão de workflows. |
| [ENC-D11-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L719)<br>**Workflow trigger abuse** | Trigger permissivo usa privilégio de branch confiável com conteúdo externo. | Revisar triggers, permissions e handling de artefatos de PR. |
| [ENC-D11-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L720)<br>**Artifact replacement** | Binário/build é alterado após validação ou antes de deploy. | Assinatura e verificação end-to-end, armazenamento imutável. |
| [ENC-D11-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L721)<br>**Build provenance forgery** | Attestation não confiável declara origem falsa do artefato. | Verificar identidade do builder e assinatura, política SLSA. |
| [ENC-D11-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L722)<br>**Release signing key theft** | Chave comprometida permite assinar distribuição maliciosa. | HSM/KMS, acesso JIT, rotação e revogação. |
| [ENC-D11-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L723)<br>**Insufficient branch protection** | Commit entra em produção sem revisão, teste ou autorização. | Required checks, CODEOWNERS e proteção contra force push. |
| [ENC-D11-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L724)<br>**Malicious pull request** | Contribuição altera lógica ou execução de CI de modo adverso. | Sandbox, revisão independente, testes e política de contributors. |
| [ENC-D11-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L725)<br>**Leaked `.env` in Git** | Arquivo de segredo no histórico permanece recuperável mesmo após remoção no último commit. | Revogação, varredura de histórico e rewrite coordenado quando adequado. |
| [ENC-D11-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L726)<br>**Exposed Git metadata** | Diretório `.git` publicado revela histórico, código e secrets. | Não servir metadados, deployment artifact allowlist e testes de exposição. |
| [ENC-D11-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L727)<br>**Compromised IaC module** | Módulo Terraform ou Helm altera permissões ou cria recursos indevidos. | Pinning, revisão, assinatura, testes de plano e origin confiável. |
| [ENC-D11-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L728)<br>**Compromised GitHub Action** | Action de terceiros executa código com credenciais do pipeline. | Fixar commit SHA, permissões mínimas e revisão de mudanças. |
| [ENC-D11-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L729)<br>**Secrets in CI logs** | Debug de pipeline publica credenciais e tokens de nuvem. | Redaction, política de logs, evitar `set -x` e revisão. |
| [ENC-D11-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L730)<br>**Insecure self-hosted runner** | Runner persiste material secreto entre jobs ou PRs não confiáveis. | Runner efêmero, isolado e sem secrets de produção em jobs externos. |
| [ENC-D11-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L731)<br>**Source code exfiltration via integration** | Serviço de terceiros recebe repositório inteiro sem necessidade. | Escopos mínimos, controles de app, revisões e contrato de dados. |
| [ENC-D11-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L732)<br>**Vulnerable dependency not patched** | CVE conhecido continua em produção após correção disponível. | SCA contínua, SBOM, prioridades KEV e patch SLO. |
| [ENC-D11-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L733)<br>**License/provenance blind spot** | Dependências sem origem identificada dificultam resposta a falhas. | SBOM completo, metadados de fornecedor e processo de aprovação. |
| [ENC-D11-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L734)<br>**CI/CD log tampering** | Logs de pipeline podem ser apagados ou modificados por mesmo ator. | Exportação imutável, segregação de auditoria e alertas. |

</details>

<details>
<summary><strong>ENC-D12 — Endpoints, malware, persistência e operações adversárias (25 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D12-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L740)<br>**Trojan** | Software aparentemente legítimo inclui função maliciosa. | Origem confiável, assinaturas, EDR e controle de execução. |
| [ENC-D12-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L741)<br>**Ransomware** | Arquivos são cifrados/indisponibilizados para extorsão. | Segmentação, MFA, EDR, patching e backups testados/imutáveis. |
| [ENC-D12-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L742)<br>**Data-wiping malware** | Código destrói dados/sistemas sem objetivo de resgate. | Backups, controles de execução, isolamento e monitoramento. |
| [ENC-D12-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L743)<br>**Spyware / infostealer** | Malware coleta credenciais, cookies e documentos. | EDR, atualização, proteção do navegador e revogação de sessões. |
| [ENC-D12-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L744)<br>**Keylogger** | Entrada de teclado é interceptada por software ou hardware comprometido. | Hardening de endpoint, EDR, FIDO2 e integridade física. |
| [ENC-D12-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L745)<br>**Rootkit** | Malware modifica camadas do sistema para ocultar atividade. | Secure Boot, atualização, EDR e verificações de integridade. |
| [ENC-D12-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L746)<br>**Bootkit / firmware compromise** | Persistência abaixo do sistema operacional escapa verificações comuns. | Firmware assinado, Secure Boot, atualizações e validação de cadeia. |
| [ENC-D12-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L747)<br>**Fileless malware** | Execução abusiva de ferramentas legítimas evita artefatos tradicionais. | EDR comportamental, logging de scripts e regras de execução. |
| [ENC-D12-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L748)<br>**Living-off-the-land** | Ferramentas administrativas nativas são usadas para execução e coleta. | Restringir uso, logging, monitoramento de comportamento e JIT. |
| [ENC-D12-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L749)<br>**Macro/document malware** | Arquivo recebido induz execução de código em leitor/office. | Desabilitar macros não confiáveis, sandbox e educação. |
| [ENC-D12-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L750)<br>**Browser compromise** | Vulnerabilidade do navegador executa código ou rouba sessão. | Atualização, isolation, política de extensões e proteção de endpoint. |
| [ENC-D12-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L751)<br>**Privilege escalation exploit** | Falha local amplia privilégio de usuário ou serviço. | Patching, proteção do kernel, menor privilégio e EDR. |
| [ENC-D12-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L752)<br>**Persistence via scheduled tasks** | Tarefa agendada mantém execução não autorizada. | Controle de mudanças, ACL, EDR e inventário de jobs. |
| [ENC-D12-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L753)<br>**Web shell persistence** | Arquivo malicioso no servidor web oferece execução remota. | Bloquear upload executável, integridade do webroot e detecção. |
| [ENC-D12-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L754)<br>**Command and control (C2)** | Host comprometido se comunica com controle remoto. | DNS/egress monitoring, EDR, segmentação e listas de destino. |
| [ENC-D12-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L755)<br>**Lateral movement** | Comprometimento inicial alcança outros hosts/sistemas. | Segmentação, credenciais únicas, MFA e monitoramento. |
| [ENC-D12-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L756)<br>**Credential dumping** | Segredos são extraídos de memória, disco ou stores do sistema. | Credencial isolation, EDR, hardening e contas de privilégio mínimo. |
| [ENC-D12-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L757)<br>**Data staging** | Dados são agregados em local intermediário antes de exfiltração. | DLP, monitoramento de arquivos/volumes e correlação de eventos. |
| [ENC-D12-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L758)<br>**Exfiltration over HTTPS** | Dados saem por conexão web aparentemente legítima. | Egress policy, DLP, anomalia de volume e classificação dos dados. |
| [ENC-D12-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L759)<br>**Exfiltration over DNS** | Dados são codificados em consultas DNS. | DNS logging central, restrição de resolvers e detecção de padrões. |
| [ENC-D12-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L760)<br>**Exfiltration to cloud storage** | Conta externa recebe dados empresariais através de serviço comum. | CASB/DLP, allowlists e alertas sobre exportação. |
| [ENC-D12-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L761)<br>**Defense evasion / log clearing** | Ator altera logs ou desliga agentes após comprometimento. | Logs remotos imutáveis, proteção anti-tamper, alertas. |
| [ENC-D12-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L762)<br>**Security tooling impairment** | Ferramentas de defesa são desabilitadas ou mal configuradas. | Proteção de políticas, saúde de agentes, separação de privilégios. |
| [ENC-D12-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L763)<br>**Destructive command execution** | Comandos de alto impacto são rodados após ganhar shell. | Limitar shell, políticas de execução, backups e segregação. |
| [ENC-D12-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L764)<br>**Cryptojacking** | Recursos computacionais são desviados para mineração não autorizada. | Detecção de consumo anormal, quotas e proteção de workloads. |

</details>

<details>
<summary><strong>ENC-D13 — Comunicação, e-mail, engenharia social e identidade organizacional (23 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D13-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L770)<br>**Phishing** | Mensagem simula entidade confiável para obter credenciais ou induzir ação. | MFA resistente a phishing, treinamento contextual e filtros de e-mail. |
| [ENC-D13-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L771)<br>**Spear phishing** | Mensagem personalizada usa dados específicos da vítima. | Proteção de contas, verificação por segundo canal e exercícios de conscientização. |
| [ENC-D13-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L772)<br>**Whaling** | Mensagem mira executivos ou responsáveis por pagamentos. | Dupla aprovação, verificação fora de banda e controles de financeiro. |
| [ENC-D13-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L773)<br>**Business Email Compromise (BEC)** | Conta/domínio falsificado induz pagamento ou vazamento. | DMARC/SPF/DKIM, confirmação de alteração bancária e MFA. |
| [ENC-D13-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L774)<br>**Domain spoofing** | E-mail ou site apresenta domínio visualmente semelhante. | Proteção DNS/e-mail, monitoramento de domínios e verificação de origem. |
| [ENC-D13-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L775)<br>**Homograph / IDN attack** | Caracteres Unicode confundem visualmente nomes de domínio. | Verificar domínio canônico, alertas de lookalike e segurança no browser. |
| [ENC-D13-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L776)<br>**Email account takeover** | Comprometimento de caixa postal expõe resets, contratos e mensagens. | MFA FIDO2, sessões gerenciadas, regras de forwarding auditadas. |
| [ENC-D13-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L777)<br>**Malicious forwarding rule** | Regra criada pelo invasor encaminha e-mails silenciosamente. | Alertar criação de regra, auditar mailbox e revogar tokens. |
| [ENC-D13-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L778)<br>**QR phishing (quishing)** | Código QR leva a site de login/ação fraudulenta. | Verificar destino, conscientização e proteção de navegação. |
| [ENC-D13-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L779)<br>**SMS phishing (smishing)** | Mensagem em celular induz abertura de link ou contato fraudulento. | Treinamento, autenticação forte e confirmação de canais oficiais. |
| [ENC-D13-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L780)<br>**Voice phishing (vishing)** | Ligação usa urgência ou falsa autoridade para obter credenciais. | Procedimento de validação por canal confiável e proibição de compartilhar OTP. |
| [ENC-D13-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L781)<br>**Deepfake voice/video fraud** | Áudio/vídeo sintético simula pessoa autorizadora de transação. | Verificação multifatorial de processos, retorno via contato conhecido e duplo controle. |
| [ENC-D13-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L782)<br>**Helpdesk impersonation** | Ator se passa por suporte ou usuário para redefinir MFA/senha. | Script de validação forte, auditoria e supervisão de exceções. |
| [ENC-D13-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L783)<br>**Pretexting** | História fabricada induz acesso ou compartilhamento de dados. | Princípio need-to-know, confirmação de identidade e registro de solicitações. |
| [ENC-D13-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L784)<br>**Baiting / malicious removable media** | Mídia/arquivo atraente induz execução de malware. | Controle de USB, EDR e política de execução. |
| [ENC-D13-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L785)<br>**Watering-hole compromise** | Site frequentemente visitado pela organização é comprometido. | Proteção de navegador, patching e filtro de navegação. |
| [ENC-D13-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L786)<br>**Malvertising** | Anúncio apresenta conteúdo ou link malicioso. | Navegação protegida, filtros e atualizações. |
| [ENC-D13-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L787)<br>**OAuth app phishing** | App malicioso obtém consentimento amplo sem roubar senha. | Controles de OAuth grants, revisão de apps e restrição de scopes. |
| [ENC-D13-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L788)<br>**Search engine poisoning** | Resultado de busca fraudulento direciona a download/login malicioso. | URLs oficiais, proteção endpoint e validação de assinaturas de software. |
| [ENC-D13-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L789)<br>**Fraudulent support contact** | Falso canal de suporte solicita acesso remoto ou pagamento. | Diretório oficial de suporte, treinamento e confirmação por segundo canal. |
| [ENC-D13-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L790)<br>**Conversation spoofing** | Mensagem é inserida em thread legítima ou simula interlocutor. | Verificação de remetente, autenticidade e processos para pedidos sensíveis. |
| [ENC-D13-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L791)<br>**Social engineering via collaboration tools** | Chat corporativo é usado para solicitar token, código ou ação de alto risco. | MFA, política de approval e orientação de verificação. |
| [ENC-D13-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L792)<br>**Physical tailgating** | Pessoa sem autorização entra em área restrita seguindo usuário. | Controle de acesso físico e treinamento. |

</details>

<details>
<summary><strong>ENC-D14 — Aplicações mobile, desktop e dispositivos clientes (21 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D14-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L798)<br>**Mobile insecure storage** | Tokens e PII ficam em arquivos/Preferences sem proteção. | Keychain/Keystore, minimização e política de backup. |
| [ENC-D14-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L799)<br>**Mobile hardcoded secret** | Chave de API privada é incorporada ao APK/IPA e extraível. | Evitar segredo privado no cliente, proxy backend e controle de escopos. |
| [ENC-D14-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L800)<br>**Mobile certificate validation bypass** | App aceita TLS inválido ou ignora hostname. | Trust management correto e testes de falha segura. |
| [ENC-D14-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L801)<br>**Insecure deep links** | Links internos permitem abrir funções ou parâmetros privilegiados. | Validar origem/destino, estado e autorização server-side. |
| [ENC-D14-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L802)<br>**Android exported component abuse** | Activity/receiver/service exportado aceita chamadas sem proteção. | `exported=false` por padrão e permissões explícitas. |
| [ENC-D14-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L803)<br>**iOS URL scheme hijacking** | Scheme customizado pode ser registrado por app adversário. | Universal Links/Associated Domains e validação do fluxo. |
| [ENC-D14-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L804)<br>**WebView JS bridge abuse** | Página não confiável acessa bridge com recursos privilegiados. | Limitar conteúdo, remover bridges desnecessárias e validar origem. |
| [ENC-D14-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L805)<br>**Clipboard leakage** | Senhas/tokens expostos na área de transferência podem ser capturados. | Evitar cópia de segredos, redaction e autoclearing quando adequado. |
| [ENC-D14-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L806)<br>**Screenshot / screen overlay** | Dados sensíveis aparecem em capturas ou sobreposição maliciosa. | Redução de dados, controles de plataforma onde disponíveis, MFA. |
| [ENC-D14-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L807)<br>**Mobile reverse engineering** | Código no pacote revela lógica e chaves, burlando controles locais. | Nunca confiar em lógica client-side, proteção do servidor e hardening. |
| [ENC-D14-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L808)<br>**App tampering / repackaging** | App modificado distribui código adulterado e simula produto oficial. | Assinaturas, distribuição verificada, attestation como sinal adicional. |
| [ENC-D14-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L809)<br>**Root/jailbreak environment abuse** | Ambiente comprometido permite inspeção/manipulação local ampliada. | Assumir cliente potencialmente hostil e reforçar verificações server-side. |
| [ENC-D14-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L810)<br>**Intent injection** | Dados de Intent não confiável acionam fluxo inadequado. | Validação dos extras e permission checks. |
| [ENC-D14-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L811)<br>**Mobile insecure backup** | Backups de sistema contêm dados e segredos que não deveriam ser exportados. | Configurar exclusões de backup e secure storage. |
| [ENC-D14-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L812)<br>**Push notification sensitive leakage** | Dados privados são exibidos em notificações/bloqueio de tela. | Conteúdo mínimo, configuração de privacidade e autorização. |
| [ENC-D14-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L813)<br>**Desktop auto-update compromise** | Atualizador aceita binário não assinado ou de canal inseguro. | Assinatura, TLS, canal confiável e rollback seguro. |
| [ENC-D14-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L814)<br>**Electron insecure nodeIntegration** | Conteúdo remoto obtém acesso a APIs nativas. | `contextIsolation`, sandbox, Node integration desabilitada e IPC limitado. |
| [ENC-D14-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L815)<br>**Electron IPC privilege bypass** | Renderer não confiável envia mensagens administrativas ao processo principal. | Autorização por canal/mensagem, validação de payload e origem. |
| [ENC-D14-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L816)<br>**Native app DLL/plugin loading** | Extensão ou biblioteca de diretório indevido é carregada. | Assinatura, paths confiáveis e controle de plugins. |
| [ENC-D14-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L817)<br>**Insecure local API** | Aplicação desktop expõe endpoint localhost sem controle de origem e auth. | Autenticação, CSRF/origin checks e acesso limitado. |
| [ENC-D14-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L818)<br>**MDM misconfiguration** | Dispositivos corporativos perdem gestão, criptografia ou compliance. | Políticas MDM, postura de dispositivo e inventário. |

</details>

<details>
<summary><strong>ENC-D15 — IoT, dispositivos, firmware e OT/ICS (12 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D15-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L824)<br>**IoT default credentials** | Dispositivo mantém login de fábrica reutilizado em milhares de unidades. | Credenciais únicas por dispositivo, onboarding seguro. |
| [ENC-D15-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L825)<br>**Insecure firmware update** | Atualização não é assinada ou validada corretamente. | Secure Boot, assinaturas de firmware e rollback controlado. |
| [ENC-D15-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L826)<br>**Unencrypted telemetry** | Sensores enviam dados/controle em canal sem autenticidade. | TLS/mTLS ou protocolos apropriados e identidade por dispositivo. |
| [ENC-D15-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L827)<br>**Device cloning** | Identidade do dispositivo é copiável entre unidades. | Chaves em secure element/TPM e provisionamento único. |
| [ENC-D15-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L828)<br>**Insecure exposed management service** | Telnet, painel ou API de configuração fica acessível publicamente. | Rede isolada, desabilitar serviços e gestão via canal protegido. |
| [ENC-D15-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L829)<br>**Firmware secret extraction** | Chaves comuns incorporadas ao firmware são extraídas. | Segredos por unidade, secure storage e rotação. |
| [ENC-D15-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L830)<br>**Replay of device command** | Comando legítimo repetido provoca ação não autorizada. | Nonce, sequência, timestamp e autenticação. |
| [ENC-D15-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L831)<br>**Sensor/data spoofing** | Dados falsos provocam decisão operacional errada. | Integridade/autenticidade, validação cruzada e detecção de anomalia. |
| [ENC-D15-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L832)<br>**OT lateral movement** | Rede corporativa comprometida alcança controles industriais. | Segmentação forte IT/OT, acesso mediado e monitoramento. |
| [ENC-D15-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L833)<br>**Safety system bypass** | Controles de segurança física/operacional são desabilitados. | Controles independentes, mudança aprovada e validação operacional. |
| [ENC-D15-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L834)<br>**Insecure industrial protocol** | Protocolo legado sem autenticação permite comandos indevidos. | Gateway seguro, segregação e compensação operacional. |
| [ENC-D15-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L835)<br>**Device fleet botnet recruitment** | Dispositivos vulneráveis tornam-se nós de ataques distribuídos. | Patch OTA, credenciais únicas, bloqueio de portas e telemetria. |

</details>

<details>
<summary><strong>ENC-D16 — IA generativa, LLM, RAG, agentes, ferramentas e MCP (33 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D16-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L843)<br>**Direct prompt injection** | Usuário tenta substituir objetivos/instruções em interface de LLM. | Separação de instruções/dados, validação de ferramentas e testes adversariais. |
| [ENC-D16-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L844)<br>**Indirect prompt injection** | Página, PDF, e-mail ou resultado de ferramenta contém comandos destinados ao agente. | Marcação de fonte não confiável, controle de ações e checagem externa ao modelo. |
| [ENC-D16-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L845)<br>**Tool output laundering** | Resposta de ferramenta é tratada como instrução autoritativa. | Classificação de origem e validação semântica/estrutural no orquestrador. |
| [ENC-D16-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L846)<br>**Retrieval-augmented injection** | Documento recuperado em RAG desvia comportamento do modelo. | Fontes confiáveis, filtros, metadados de proveniência, políticas fora do prompt. |
| [ENC-D16-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L847)<br>**RAG cross-tenant leakage** | Busca vetorial retorna documentos de outro cliente/usuário. | Filtro de autorização no mecanismo de retrieval e no documento final. |
| [ENC-D16-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L848)<br>**Embedding/vector store poisoning** | Dados artificiais contaminam índice e resultados de recuperação. | Curadoria de ingestão, proveniência, aprovação e reindexação auditável. |
| [ENC-D16-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L849)<br>**Training-data poisoning** | Dados de treino manipulados induzem comportamento indevido. | Proveniência, validação de datasets, avaliação e isolamento do pipeline. |
| [ENC-D16-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L850)<br>**Model supply-chain compromise** | Modelo/pesos/adapters ou conversores são manipulados. | Artefatos assinados, revisão de origem, scanning e sandbox. |
| [ENC-D16-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L851)<br>**Sensitive information disclosure** | Resposta revela segredos, PII ou dados conectados sem permissão. | Redação, políticas de acesso e filtros antes da recuperação/ferramenta. |
| [ENC-D16-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L852)<br>**System prompt extraction** | Ator tenta obter instruções internas ou informações embutidas. | Não guardar segredos em prompts, restringir ferramentas e outputs. |
| [ENC-D16-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L853)<br>**Excessive agency** | Agente tem capacidade ampla de enviar, apagar, pagar ou configurar sem controle. | Least privilege, ações permitidas, limites e aprovação humana para alto impacto. |
| [ENC-D16-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L854)<br>**Agent goal hijacking** | Contexto adversarial modifica metas de execução do agente. | Objetivo assinado/estável fora do modelo e avaliação de cada ação. |
| [ENC-D16-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L855)<br>**Tool misuse** | Ferramenta legítima é invocada com objetivo ou parâmetros impróprios. | Validação de argumentos, escopo, autorização e auditoria por ferramenta. |
| [ENC-D16-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L856)<br>**MCP tool poisoning** | Descrição/resultado de ferramenta MCP contém instruções enganosas. | Registrar servidores confiáveis, revisar schemas e não confiar em descrições como política. |
| [ENC-D16-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L857)<br>**MCP server impersonation** | Servidor de ferramenta falso se apresenta como integração legítima. | Autenticação do servidor, identidade verificável e allowlist de conectores. |
| [ENC-D16-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L858)<br>**Tool schema spoofing** | Modelo recebe definição adulterada de ferramenta e concede poder indevido. | Schemas versionados/assinados, validação no executor e change control. |
| [ENC-D16-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L859)<br>**Cross-tool exfiltration** | Agente lê dado sensível em uma ferramenta e envia via outra. | Políticas de fluxo de dados, escopos separados e aprovação para saída externa. |
| [ENC-D16-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L860)<br>**Agent identity and privilege abuse** | Agente usa credencial do usuário para operação não autorizada. | Consentimento por ação/escopo, identidade delegada curta e aprovação contextual. |
| [ENC-D16-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L861)<br>**Memory poisoning** | Texto malicioso é registrado como memória persistente e influencia ações futuras. | Revisão da origem, distinção dados/instruções, TTL e edição/auditoria de memória. |
| [ENC-D16-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L862)<br>**Context poisoning** | Histórico/contexto é contaminado para alterar decisões e classificações. | Proveniência de mensagens, integridade, limites e verificação independente. |
| [ENC-D16-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L863)<br>**Multi-agent trust confusion** | Agente secundário confia irrestritamente na saída de outro. | Credenciais e contexto por agente, autenticação interagente e contratos. |
| [ENC-D16-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L864)<br>**Unbounded token/cost consumption** | Prompts, loops e chamadas de ferramenta consomem orçamento descontrolado. | Quotas por usuário/tarefa, limite de iterações/tokens e circuit breaker. |
| [ENC-D16-S023](security-auditor/references/encyclopedia-v1.0.md?plain=1#L865)<br>**Output handling injection** | LLM produz HTML, SQL ou shell que aplicação executa sem validação. | Tratar saída do modelo como não confiável e proteger sinks tradicionais. |
| [ENC-D16-S024](security-auditor/references/encyclopedia-v1.0.md?plain=1#L866)<br>**Hallucination as authoritative action** | Informação incorreta induz pagamento, alteração ou decisão sensível. | Validação com fonte primária, supervisão e limites de autonomia. |
| [ENC-D16-S025](security-auditor/references/encyclopedia-v1.0.md?plain=1#L867)<br>**Unsafe code generation** | Código sugerido introduz segredos, execuções inseguras ou falhas de auth. | Revisão humana, SAST/SCA, testes de segurança e templates seguros. |
| [ENC-D16-S026](security-auditor/references/encyclopedia-v1.0.md?plain=1#L868)<br>**Model extraction** | Consultas revelam comportamento/modelo proprietário e custo operacional. | Rate limit, termos de uso, detecção de padrões e segurança de API. |
| [ENC-D16-S027](security-auditor/references/encyclopedia-v1.0.md?plain=1#L869)<br>**Model inversion / membership inference** | Saídas revelam informação sobre dados de treinamento em certos cenários. | Privacidade de treinamento, avaliação e exposição mínima. |
| [ENC-D16-S028](security-auditor/references/encyclopedia-v1.0.md?plain=1#L870)<br>**Unsafe model tool execution** | Agente executa código sem isolamento e acessa dados/host. | Sandbox efêmero, sem root, rede restrita, FS mínimo e orçamento. |
| [ENC-D16-S029](security-auditor/references/encyclopedia-v1.0.md?plain=1#L871)<br>**HITL approval manipulation** | Conteúdo externo fabrica ou influencia aprovação humana para ação perigosa. | Interface mostra ação exata, origem confiável e confirmação fora do conteúdo. |
| [ENC-D16-S030](security-auditor/references/encyclopedia-v1.0.md?plain=1#L872)<br>**Browser-agent web prompt injection** | Página visitada instrui agente a mudar objetivos, enviar dados ou clicar. | Limitar navegação e ferramentas, autorização por ação, egress e auditoria. |
| [ENC-D16-S031](security-auditor/references/encyclopedia-v1.0.md?plain=1#L873)<br>**AI-generated phishing/deepfakes** | Automação torna fraude e impersonação mais convincentes. | Processos de aprovação independentes, FIDO2 e verificação de identidade. |
| [ENC-D16-S032](security-auditor/references/encyclopedia-v1.0.md?plain=1#L874)<br>**Tool-result provenance loss** | Resposta perde referência a origem e vira afirmação confiável. | Citações verificáveis, metadados de trust level e checagem de fontes. |
| [ENC-D16-S033](security-auditor/references/encyclopedia-v1.0.md?plain=1#L875)<br>**Automated agent loop/recursion** | Agente invoca ferramentas ou outros agentes indefinidamente. | Limites de profundidade, tempo, ações, orçamento e watchdog. |

</details>

<details>
<summary><strong>ENC-D17 — Segurança física, disponibilidade operacional e fator humano (10 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D17-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L881)<br>**Theft of unlocked device** | Equipamento desbloqueado dá acesso a sessão e arquivos. | Bloqueio automático, FDE, autenticação e MDM. |
| [ENC-D17-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L882)<br>**Theft of backup media** | Mídia de backup é perdida/roubada sem proteção. | Criptografia, inventário e cadeia de custódia. |
| [ENC-D17-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L883)<br>**Unauthorized data center access** | Ator sem autorização acessa hardware ou consoles. | Controle físico, registro, alarmes e segregação. |
| [ENC-D17-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L884)<br>**Shoulder surfing** | Senha/dados são observados durante digitação/consulta. | Privacidade de tela, MFA e conscientização. |
| [ENC-D17-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L885)<br>**Unauthorized USB peripherals** | Dispositivo USB malicioso se apresenta como teclado/rede. | Controle de periféricos, políticas e proteção endpoint. |
| [ENC-D17-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L886)<br>**Power/environmental outage** | Falhas de energia, climatização ou instalações interrompem serviços. | Redundância, UPS, monitoramento ambiental e recuperação. |
| [ENC-D17-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L887)<br>**Insider misuse** | Usuário legítimo usa privilégio para finalidade indevida. | Menor privilégio, trilhas, separação de funções e revisões. |
| [ENC-D17-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L888)<br>**Negligent data handling** | Compartilhamento indevido por erro humano expõe dados. | Classificação, DLP, UX segura e controles de compartilhamento. |
| [ENC-D17-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L889)<br>**Social trust exploitation** | Autoridade aparente induz quebra de procedimento de segurança. | Processo verificável, dupla aprovação e treinamento. |
| [ENC-D17-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L890)<br>**Vendor onsite access abuse** | Terceiro obtém acesso físico/lógico além de serviço contratado. | Acesso temporário supervisionado, escopo e logging. |

</details>

<details>
<summary><strong>ENC-D18 — Segurança de memória, compiladores e exploração binária (22 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D18-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L896)<br>**Stack buffer overflow** | Escrita além do espaço alocado na pilha pode corromper dados e controle. | Linguagens memory-safe, análise estática, bounds checks, ASLR, stack canaries. |
| [ENC-D18-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L897)<br>**Heap buffer overflow** | Escrita fora da área alocada no heap causa corrupção e eventual execução. | Memory-safe, sanitizers, allocators protegidos, fuzzing de parsers. |
| [ENC-D18-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L898)<br>**Out-of-bounds read** | Leitura indevida revela memória, segredos ou causa falhas. | Verificação de limites, ASan/UBSan e testes de entrada. |
| [ENC-D18-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L899)<br>**Out-of-bounds write** | Escrita indevida altera estruturas internas e controle do processo. | Bounds checking, revisão de C/C++, fuzzing e hardening de compilador. |
| [ENC-D18-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L900)<br>**Use-after-free (UAF)** | Ponteiro aponta para memória liberada e depois reutilizada. | Ownership/borrowing, sanitizers, fuzzing e atualização de componentes. |
| [ENC-D18-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L901)<br>**Double free** | Memória é liberada duas vezes, corrompendo heap ou causando DoS. | RAII/ownership, sanitizers, APIs de gerenciamento seguro de memória. |
| [ENC-D18-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L902)<br>**Dangling pointer** | Referência persistente aponta para objeto destruído. | Linguagens memory-safe, lifetime tracking e testes. |
| [ENC-D18-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L903)<br>**Integer overflow/underflow** | Aritmética transborda e produz alocação/checagem incorreta. | Inteiros checados, validação de limites e sanitizers. |
| [ENC-D18-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L904)<br>**Signedness conversion** | Conversão sinalizado/não sinalizado altera limites de tamanho e índices. | Tipos corretos, checagens explícitas e warnings como erro. |
| [ENC-D18-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L905)<br>**Type confusion** | Objeto é interpretado como tipo incompatível e pode violar memória. | Verificação de tipos, runtime patches e sandbox. |
| [ENC-D18-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L906)<br>**Format string injection** | Formatação controlada interpreta marcadores de memória/comando. | Strings de formato constantes e APIs seguras. |
| [ENC-D18-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L907)<br>**NULL pointer dereference** | Uso de ponteiro nulo provoca crash ou comportamento indevido. | Checagens, programação defensiva e testes de estado. |
| [ENC-D18-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L908)<br>**Race condition de memória** | Threads acessam estado compartilhado sem sincronização correta. | Locks, atomics, modelos de concorrência seguros e race detectors. |
| [ENC-D18-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L909)<br>**Return-Oriented Programming (ROP)** | Cadeias de instruções existentes podem ser usadas após corrupção de memória. | Memory safety, DEP/NX, ASLR, CFI e correções na falha raiz. |
| [ENC-D18-S015](security-auditor/references/encyclopedia-v1.0.md?plain=1#L910)<br>**JIT spraying** | Código gerado dinamicamente amplia regiões executáveis controláveis. | W^X, proteção do JIT, sandbox e atualizações. |
| [ENC-D18-S016](security-auditor/references/encyclopedia-v1.0.md?plain=1#L911)<br>**Speculative execution side channels** | Efeitos microarquiteturais revelam dados em determinados processadores/cenários. | Patches de firmware/SO, isolamento e mitigações de fabricante. |
| [ENC-D18-S017](security-auditor/references/encyclopedia-v1.0.md?plain=1#L912)<br>**Cache-timing side channel** | Variação de cache pode revelar operações secretas. | Implementações constant-time, isolamento e bibliotecas criptográficas auditadas. |
| [ENC-D18-S018](security-auditor/references/encyclopedia-v1.0.md?plain=1#L913)<br>**Rowhammer / disturbance errors** | Alterações físicas em memória podem afetar bits adjacentes sob condições específicas. | Mitigações de hardware, ECC quando aplicável e atualização de plataforma. |
| [ENC-D18-S019](security-auditor/references/encyclopedia-v1.0.md?plain=1#L914)<br>**DMA / malicious peripheral** | Periférico com acesso direto à memória pode contornar controles tradicionais. | IOMMU, política de portas, Kernel DMA Protection e controle físico. |
| [ENC-D18-S020](security-auditor/references/encyclopedia-v1.0.md?plain=1#L915)<br>**Malicious compiler/build toolchain** | Compilador ou linker adulterado injeta alteração invisível ao código fonte. | Toolchain verificada, builds reprodutíveis, assinaturas e proveniência. |
| [ENC-D18-S021](security-auditor/references/encyclopedia-v1.0.md?plain=1#L916)<br>**ABI/FFI boundary misuse** | Conversão entre linguagens nativas e seguras introduz UAF/OOB. | Revisar código unsafe, encapsular FFI e fuzzing de fronteiras. |
| [ENC-D18-S022](security-auditor/references/encyclopedia-v1.0.md?plain=1#L917)<br>**GPU/accelerator memory isolation** | Falhas no driver/runtime expõem memória de outros processos/tenants. | Isolamento, patch de drivers e gestão de workloads sensíveis. |

</details>

<details>
<summary><strong>ENC-D19 — Redes sem fio, proximidade, navegação e periféricos (14 cenários)</strong></summary>

| ID e cenário | Precondição, fraqueza ou impacto a investigar | Defesa ou validação proposta |
| --- | --- | --- |
| [ENC-D19-S001](security-auditor/references/encyclopedia-v1.0.md?plain=1#L923)<br>**Wi-Fi deauthentication/disassociation abuse** | Quadros de gestão desprotegidos permitem desconexões e indução de reconexão. | Protected Management Frames (802.11w/PMF), WPA3 e monitoramento. |
| [ENC-D19-S002](security-auditor/references/encyclopedia-v1.0.md?plain=1#L924)<br>**Wi-Fi weak passphrase attack** | Chave compartilhada fraca pode ser descoberta por tentativas offline. | WPA3/802.1X, senha forte e rotação. |
| [ENC-D19-S003](security-auditor/references/encyclopedia-v1.0.md?plain=1#L925)<br>**Wireless rogue access point** | Ponto de acesso não autorizado captura dispositivos ou expõe rede. | WIDS/WIPS, 802.1X e inventário de pontos. |
| [ENC-D19-S004](security-auditor/references/encyclopedia-v1.0.md?plain=1#L926)<br>**Bluetooth/BLE spoofing** | Dispositivo adversário imita periférico autorizado. | Pairing autenticado, bonding correto e identidade por dispositivo. |
| [ENC-D19-S005](security-auditor/references/encyclopedia-v1.0.md?plain=1#L927)<br>**BLE weak pairing** | Métodos sem confirmação forte permitem interposição em cenários aplicáveis. | Escolher modo de pareamento mais forte suportado e criptografia. |
| [ENC-D19-S006](security-auditor/references/encyclopedia-v1.0.md?plain=1#L928)<br>**Bluetooth service exposure** | Serviços de depuração/controle ficam acessíveis por rádio. | Desativar perfis desnecessários, autenticar e atualizar firmware. |
| [ENC-D19-S007](security-auditor/references/encyclopedia-v1.0.md?plain=1#L929)<br>**RFID/NFC cloning** | Credencial de proximidade fraca pode ser copiada. | Credenciais criptográficas com desafio-resposta e revogação. |
| [ENC-D19-S008](security-auditor/references/encyclopedia-v1.0.md?plain=1#L930)<br>**NFC relay attack** | Mensagens de proximidade são retransmitidas em outro local. | Controles de transação, supervisão de risco e protocolos resistentes quando disponíveis. |
| [ENC-D19-S009](security-auditor/references/encyclopedia-v1.0.md?plain=1#L931)<br>**GPS/GNSS spoofing** | Sinais falsos alteram percepção de posição/tempo. | Verificação de integridade multi-sensor e alarmes de anomalia. |
| [ENC-D19-S010](security-auditor/references/encyclopedia-v1.0.md?plain=1#L932)<br>**GPS/GNSS jamming** | Interferência impede recepção de sinais de navegação. | Fontes redundantes de posicionamento/tempo e monitoramento de interferência. |
| [ENC-D19-S011](security-auditor/references/encyclopedia-v1.0.md?plain=1#L933)<br>**CAN bus injection** | Mensagens veiculares não autenticadas podem alterar comportamento dos controladores. | Segmentação, gateways, autenticidade das mensagens e safety design. |
| [ENC-D19-S012](security-auditor/references/encyclopedia-v1.0.md?plain=1#L934)<br>**Industrial wireless command spoofing** | Comando de rádio sem autenticação pode alterar dispositivos OT. | Autenticação criptográfica, segmentação e monitoração física. |
| [ENC-D19-S013](security-auditor/references/encyclopedia-v1.0.md?plain=1#L935)<br>**Smart lock replay** | Mensagem de abertura é reutilizada sem mecanismo de frescor. | Nonce/contador, challenge-response e armazenamento protegido de chaves. |
| [ENC-D19-S014](security-auditor/references/encyclopedia-v1.0.md?plain=1#L936)<br>**Side-channel via sensors** | Sensores de movimento, luz ou som expõem indiretamente dados de usuário. | Permissões mínimas e restrição de acesso a sensores. |

</details>


<a id="controles"></a>

## Controles de segurança

O catálogo não olha apenas para padrões inseguros. Ele também orienta a revisão dos controles
que deveriam proteger cada fronteira de confiança. Cada controle recebe aplicabilidade,
evidências e um dos estados abaixo:

| Estado | Interpretação |
| --- | --- |
| `IMPLEMENTED` | Existe evidência atual de implementação no escopo verificado. |
| `PARTIALLY_IMPLEMENTED` | A proteção existe, mas não cobre todo o caminho ou superfície. |
| `NOT_IMPLEMENTED` | O controle aplicável não está implementado no escopo examinado. |
| `MISCONFIGURED` | O controle existe com configuração inadequada. |
| `NOT_APPLICABLE` | Há justificativa e evidência para a exclusão naquele contexto. |
| `NOT_VERIFIED` | Faltam acesso, informação, ferramenta ou teste para uma conclusão. |

| Família | Quantidade | Foco |
| --- | ---: | --- |
| `GOV` | 12 | Governança e desenvolvimento seguro |
| `IAM` | 18 | Identidade, autenticação e autorização |
| `APP` | 26 | Entrada, saída e aplicação |
| `API` | 14 | APIs, serviços e integridade |
| `DAT` | 14 | Dados, criptografia e privacidade |
| `NET` | 24 | Rede, cloud e execução |
| `SDLC` | 16 | Supply chain, CI/CD e testes |
| `OPS` | 12 | Operação, detecção e resposta |

<details>
<summary><strong>Consultar os 136 controles e seus critérios de revisão</strong></summary>

### GOV — Governança e desenvolvimento seguro

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [GOV-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L156) | **Inventário de ativos e dados** | Identificar aplicações, domínios, APIs, ambientes, repositórios, bases, proprietários e classificação da informação. |
| [GOV-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L157) | **Modelagem de ameaças STRIDE** | Mapear ativos, fluxos, fronteiras de confiança, ameaças, controles e risco residual antes de funcionalidades críticas. |
| [GOV-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L158) | **Secure by Design / Secure by Default** | Negar por padrão, eliminar privilégios excessivos e reduzir opções perigosas na configuração inicial. |
| [GOV-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L159) | **Critérios de aceite de segurança** | Traduzir riscos em requisitos verificáveis ligados a tickets, ASVS e testes automatizados. |
| [GOV-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L160) | **Políticas de exceção e dívida técnica** | Registrar exceção, prazo, owner, controles compensatórios e aceitação formal do risco. |
| [GOV-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L161) | **Revisão de arquitetura e código** | Requerer revisão independente para autenticação, pagamentos, isolamento multi-tenant, criptografia e administração. |
| [GOV-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L162) | **Separação de deveres** | Distanciar aprovação, desenvolvimento, deploy, administração de produção e acesso a dados sensíveis. |
| [GOV-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L163) | **Princípio de acesso mínimo** | Permissões just-in-time, just-enough e revisões periódicas; evitar credenciais universais. |
| [GOV-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L164) | **Inventário de terceiros e fornecedores** | Avaliar integrações, contratos, escopos de dados, exposição, SLA de patches e dependências críticas. |
| [GOV-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L165) | **Gestão de vulnerabilidades** | Deduplicar findings, priorizar por exposição, criticidade, KEV/EPSS, impacto e contexto de negócio. |
| [GOV-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L166) | **Política de divulgação coordenada** | Disponibilizar canal de reporte e triagem; `security.txt` quando aplicável. |
| [GOV-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L167) | **Exercícios tabletop e restauração** | Ensaiar cenários de incidentes, indisponibilidade, ransomware e vazamentos. |

### IAM — Identidade, autenticação e autorização

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [IAM-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L173) | **Passkeys/WebAuthn** | Validar origem/RP ID, assinatura, challenge, registro e revogação. |
| [IAM-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L174) | **MFA resistente a phishing** | Privilegiar chaves FIDO2 para admin, acesso remoto e contas de alto risco. |
| [IAM-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L175) | **Hash de senha adaptativo** | Argon2id/scrypt/PBKDF2/bcrypt conforme contexto, sal individual e configuração calibrada. |
| [IAM-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L176) | **Anti-enumeração de contas** | Respostas e tempos equivalentes em login/recuperação, sem vazamento de registro. |
| [IAM-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L177) | **Rate limit e proteção contra brute force** | Aplicar limites proporcionais a IP, usuário, dispositivo, tenant e operação. |
| [IAM-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L178) | **Sessão segura** | ID aleatório, rotação, expiração por inatividade/absoluta e revogação. |
| [IAM-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L179) | **Cookie HttpOnly/Secure/SameSite** | Escopo mínimo, prefixo `__Host-` quando possível, TLS e anti-CSRF. |
| [IAM-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L180) | **JWT seguro** | Algoritmos permitidos, chave confiável, claims verificados, ciclo de vida, revogação. |
| [IAM-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L181) | **Refresh token rotation** | Detectar reuse, revogar família, guardar credencial protegida no contexto correto. |
| [IAM-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L182) | **OAuth/OIDC robusto** | Code+PKCE, exact redirect URI, validação de emissor, fluxo e tokens. |
| [IAM-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L183) | **Autorização por objeto** | Verificar dono, tenant, papel e ação em cada recurso, não só na rota. |
| [IAM-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L184) | **Autorização por propriedade** | Controlar leitura/alteração de atributos sensíveis e evitar mass assignment. |
| [IAM-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L185) | **RBAC/ABAC/ReBAC** | Escolher modelo apropriado, centralizar políticas e testar combinações negativas. |
| [IAM-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L186) | **Isolamento multi-tenant** | `tenant_id` de contexto autenticado, escopo no backend, RLS e testes cruzados. |
| [IAM-15](security-auditor/references/encyclopedia-v1.0.md?plain=1#L187) | **Menor privilégio de máquina** | IAM para workload, roles estreitas, credenciais efêmeras, PAM/JIT. |
| [IAM-16](security-auditor/references/encyclopedia-v1.0.md?plain=1#L188) | **Reautenticação de operações críticas** | Exigir step-up adequado para transferência, mudança de e-mail, segredos e permissões. |
| [IAM-17](security-auditor/references/encyclopedia-v1.0.md?plain=1#L189) | **Ciclo de vida de identidade** | Provisionamento, revisão de acessos, desligamento, remoção de sessões e integração SCIM quando pertinente. |
| [IAM-18](security-auditor/references/encyclopedia-v1.0.md?plain=1#L190) | **Defesa contra sessão simultânea anômala** | Monitorar mudanças bruscas de contexto, aplicar verificação contextual e informar usuário. |

### APP — Entrada, saída e aplicação

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [APP-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L196) | **Validação de esquema no servidor** | Tipos, tamanho, formato, enumeração, semântica e limites de payload. |
| [APP-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L197) | **Consultas parametrizadas** | Queries preparadas/bind parameters; jamais concatenar entrada do usuário em SQL. |
| [APP-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L198) | **Output encoding contextual** | Escape em HTML, atributo, URL, JavaScript e CSS conforme o contexto de saída. |
| [APP-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L199) | **Sanitização de HTML** | Sanitizador maduro e allowlist para conteúdo rico realmente permitido; preferir saída textual. |
| [APP-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L200) | **CSP forte** | Usar nonces/hashes onde possível, `script-src` restritiva, `object-src 'none'`, `base-uri` e `frame-ancestors`. |
| [APP-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L201) | **Trusted Types** | Reduzir sinks DOM XSS em navegadores compatíveis e aplicações de alto risco. |
| [APP-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L202) | **Anti-CSRF** | Token sincronizador ou double-submit assinado, proteção de origem/Fetch Metadata. |
| [APP-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L203) | **TLS/HSTS** | HTTPS e TLS atuais; HSTS após avaliar subdomínios e impactos operacionais. |
| [APP-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L204) | **Headers de segurança** | `nosniff`, `Referrer-Policy`, `Permissions-Policy`, CSP e política de cache contextual. |
| [APP-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L205) | **Proteção contra clickjacking** | `frame-ancestors`; `X-Frame-Options` apenas como compatibilidade. |
| [APP-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L206) | **CORS por origem confiável** | Evitar `*` com credenciais; não refletir `Origin` sem validação, nem tratar CORS como autenticação. |
| [APP-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L207) | **SSRF allowlist/egress** | Validar destino DNS/IP na conexão, restringir protocolos, redirects e acesso a metadados de cloud. |
| [APP-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L208) | **Proteção de arquivos e paths** | IDs indiretos, canonicalização controlada, sandbox e restrição de diretórios permitidos. |
| [APP-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L209) | **Upload seguro** | Tipo real, tamanho, extensão, antivírus quando pertinente, renomeação, armazenamento isolado. |
| [APP-15](security-auditor/references/encyclopedia-v1.0.md?plain=1#L210) | **Limites de decompression/processamento** | Bloquear zip bombs, PDF/arquivo patológico, parsers recursivos, volume excessivo. |
| [APP-16](security-auditor/references/encyclopedia-v1.0.md?plain=1#L211) | **XML seguro** | Desabilitar DTD/entities externas e recursos não requeridos; evitar XXE/XSLT inseguro. |
| [APP-17](security-auditor/references/encyclopedia-v1.0.md?plain=1#L212) | **Serialização segura** | Não desserializar objetos executáveis de origem não confiável; limitar modelos e tipos. |
| [APP-18](security-auditor/references/encyclopedia-v1.0.md?plain=1#L213) | **ReDoS** | Regex de complexidade controlada, limites de input, timeout e bibliotecas resilientes. |
| [APP-19](security-auditor/references/encyclopedia-v1.0.md?plain=1#L214) | **Evitar execução de shell** | Usar APIs nativas; caso inevitável, argumentos separados, allowlist e sandbox. |
| [APP-20](security-auditor/references/encyclopedia-v1.0.md?plain=1#L215) | **Tratamento seguro de erros** | Respostas genéricas, logging interno estruturado; sem stack traces públicos. |
| [APP-21](security-auditor/references/encyclopedia-v1.0.md?plain=1#L216) | **Limites transacionais e idempotência** | Garantir atomicidade, bloqueios necessários e idempotency keys em efeitos financeiros. |
| [APP-22](security-auditor/references/encyclopedia-v1.0.md?plain=1#L217) | **Processamento de webhooks** | Assinatura/HMAC, janela temporal, replay protection, controle de eventos e origem. |
| [APP-23](security-auditor/references/encyclopedia-v1.0.md?plain=1#L218) | **Proteção de cache** | Chaves com tenant/usuário, respostas sensíveis `private/no-store`, controle de variantes. |
| [APP-24](security-auditor/references/encyclopedia-v1.0.md?plain=1#L219) | **Sanitização de CSV/fórmulas** | Neutralizar células que possam ser interpretadas como fórmulas em planilhas. |
| [APP-25](security-auditor/references/encyclopedia-v1.0.md?plain=1#L220) | **Redirecionamentos permitidos** | Destinos fixos ou allowlist; evitar open redirect e validação por prefixo frágil. |
| [APP-26](security-auditor/references/encyclopedia-v1.0.md?plain=1#L221) | **Normalização consistente** | Evitar interpretações divergentes entre CDN, proxy, framework, parser e backend. |

### API — APIs, serviços e integridade

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [API-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L227) | **OpenAPI/JSON Schema** | Contratos completos para parâmetros, corpos, respostas e versionamento. |
| [API-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L228) | **Inventário de endpoints** | Catalogar ambientes, versões, APIs legadas, shadow APIs, owners e exposição. |
| [API-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L229) | **Gateway com defesa em profundidade** | AuthN e quotas na borda **e** checagem real de autorização nos serviços. |
| [API-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L230) | **Quotas por custo** | Controlar tempo, memória, chamadas externas, linhas, operações de DB e payload. |
| [API-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L231) | **Defesa de GraphQL** | Limites de depth/complexity, aliases, batching, persistência de queries quando apropriado. |
| [API-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L232) | **Segurança gRPC** | mTLS quando aplicável, identidade, limites de mensagens, autorização por método. |
| [API-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L233) | **Segurança de WebSocket** | Checar `Origin`, autenticação, autorização por mensagem, tamanho e ciclo de conexão. |
| [API-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L234) | **Webhook trust** | Verificação criptográfica, timestamp, deduplicação e segredos rotativos. |
| [API-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L235) | **Autorização de campo** | Não confiar em atributos enviados por cliente; DTOs com allowlist de propriedades. |
| [API-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L236) | **Auditoria de mudanças** | Registrar quem, o quê, quando, origem, antes/depois pertinente e integridade. |
| [API-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L237) | **Controle de replays** | Nonce, timestamp, deduplicação, assinatura e transação conforme protocolo. |
| [API-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L238) | **Saída mínima** | Reduzir DTOs, paginar, mascarar PII e evitar exposição de metadados internos. |
| [API-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L239) | **Contratos com terceiros** | Validar respostas externas antes de inserir em banco, exibir ou usar como confiança. |
| [API-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L240) | **Consistência de validação** | Revalidar após deserialização, filas, filas de eventos, caches e boundaries. |

### DAT — Dados, criptografia e privacidade

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [DAT-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L246) | **Criptografia em trânsito** | TLS adequado nas conexões cliente, serviço, banco e message broker. |
| [DAT-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L247) | **Criptografia em repouso** | Proteção de volumes, objetos, backups e campos de alto risco quando justificável. |
| [DAT-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L248) | **Algoritmos modernos** | AEAD como AES-GCM/ChaCha20-Poly1305 quando aplicável; evitar modos inseguros. |
| [DAT-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L249) | **Gestão de chaves** | KMS/HSM, segregação, rotação, revogação, versionamento e controle de acesso. |
| [DAT-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L250) | **Geração aleatória segura** | CSPRNG para tokens, nonces, sessões e chaves; proibir IDs previsíveis como credenciais. |
| [DAT-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L251) | **Segredos fora do código** | Secret manager, variáveis protegidas e scanning; cuidado com leaks por imagens e logs. |
| [DAT-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L252) | **Minimização dos dados** | Coletar só o necessário; reter pelo prazo devido; mascarar em teste/observabilidade. |
| [DAT-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L253) | **Isolamento de tenants** | Linhas/colunas/bancos/contas isolados conforme risco; RLS como defesa adicional. |
| [DAT-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L254) | **Backups resilientes** | Criptografia, acesso mínimo, cópia imutável/offline e teste periódico de restauração. |
| [DAT-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L255) | **Retenção e descarte** | Política de lifecycle, deleção verificável e classificação de dados. |
| [DAT-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L256) | **Prevenção de exportação indevida** | Aprovação, quotas, alertas, DLP e auditoria de acesso maciço. |
| [DAT-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L257) | **Tokenização/pseudonimização** | Reduzir exposição de identificadores, avaliar reversibilidade e segregação. |
| [DAT-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L258) | **Integridade e assinatura** | Assinar artefatos/objetos quando necessário; comparar hash com origem confiável. |
| [DAT-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L259) | **Proteção de dados em logs** | Redação de PII/segredos, retenção, acesso e proteção contra adulteração. |

### NET — Rede, cloud e execução

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [NET-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L265) | **Proteção volumétrica DDoS** | Provedor de mitigação L3/L4, capacidade upstream e procedimentos de escalonamento. |
| [NET-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L266) | **Proteção DDoS na aplicação** | CDN/WAF, challenge adaptativo, cache, proteção do origin, limites por rota e custo. |
| [NET-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L267) | **Rate limiting distribuído** | Limites corretos em multi-instância, Redis/gateway quando apropriado e chave de identidade confiável. |
| [NET-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L268) | **Circuit breaker e backpressure** | Impedir cascatas de falhas e filas infinitas, definir timeouts e budgets. |
| [NET-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L269) | **Proteção de origin** | Firewall/ACL para aceitar tráfego só do proxy legítimo; validar headers de IP de origem. |
| [NET-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L270) | **Segmentação de rede** | Privado por padrão, portas mínimas, regras de entrada/saída e isolamento entre tiers. |
| [NET-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L271) | **Egress filtering** | Restringir tráfego externo de workloads, SSRF e canais de exfiltração. |
| [NET-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L272) | **WAF / WAAP** | Regras gerenciadas e customizadas, observabilidade e teste de falsos positivos. |
| [NET-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L273) | **IDS/IPS e NDR** | Detecção de comportamento de rede anômalo; correlação com app e hosts. |
| [NET-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L274) | **DNS seguro** | Controles de alteração, DNSSEC quando apropriado, inventário, CAA e monitoramento. |
| [NET-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L275) | **Proteção contra takeover** | Remover DNS pendente e verificar posse de subdomínios e buckets vinculados. |
| [NET-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L276) | **Hardening do sistema** | Patches, desativar serviços, usuários não privilegiados, firewall, segurança de SSH. |
| [NET-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L277) | **Gestão de certificados** | Automação de renovação, validação de cadeia, validade e chaves privadas. |
| [NET-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L278) | **IAM de cloud mínimo** | Evitar permissões globais, separar contas e regiões e fiscalizar federação/roles. |
| [NET-15](security-auditor/references/encyclopedia-v1.0.md?plain=1#L279) | **CSPM/IaC scanning** | Detectar buckets públicos, security groups amplos, IAM, logging e criptografia. |
| [NET-16](security-auditor/references/encyclopedia-v1.0.md?plain=1#L280) | **Imagens/containers mínimos** | Imagens oficiais e fixadas, atualização, scanning, usuário non-root e sistemas read-only. |
| [NET-17](security-auditor/references/encyclopedia-v1.0.md?plain=1#L281) | **Sandbox / isolamento** | Seccomp, AppArmor/SELinux, namespaces, capacidades mínimas, limites de recursos. |
| [NET-18](security-auditor/references/encyclopedia-v1.0.md?plain=1#L282) | **Kubernetes RBAC e policies** | Service accounts mínimas, admission policies, network policies, Pod Security, quotas. |
| [NET-19](security-auditor/references/encyclopedia-v1.0.md?plain=1#L283) | **Secrets em runtime** | Não embutir em image layers nem expor via logs, endpoints de debug ou env dumps. |
| [NET-20](security-auditor/references/encyclopedia-v1.0.md?plain=1#L284) | **Metadata service hardening** | AWS IMDSv2, restrição de acesso a metadados, egress e identities de escopo mínimo. |
| [NET-21](security-auditor/references/encyclopedia-v1.0.md?plain=1#L285) | **Proteção de infraestrutura como código** | Revisão, planos aprovados, secrets protegidos, estados remotos criptografados. |
| [NET-22](security-auditor/references/encyclopedia-v1.0.md?plain=1#L286) | **Resiliência e contingência** | Regiões/zones redundantes quando necessário, testes de failover e RTO/RPO definidos. |
| [NET-23](security-auditor/references/encyclopedia-v1.0.md?plain=1#L287) | **Endpoint/EDR** | Proteção de estações, servidores e workloads, telemetria e contenção. |
| [NET-24](security-auditor/references/encyclopedia-v1.0.md?plain=1#L288) | **Zero Trust contextual** | Autenticar e autorizar cada acesso relevante, limitar confiança em rede interna. |

### SDLC — Supply chain, CI/CD e testes

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [SDLC-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L294) | **SAST** | Detectar padrões de fluxo perigoso no código; validar findings manualmente. |
| [SDLC-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L295) | **SCA e SBOM** | Inventariar dependências diretas/transitivas, licenças, versões e vulnerabilidades. |
| [SDLC-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L296) | **Secrets scanning** | Examinar código, histórico, artefatos e pipelines, com revogação após vazamento. |
| [SDLC-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L297) | **DAST autorizado** | Testes dinâmicos controlados em ambientes autorizados com taxa e escopo limitados. |
| [SDLC-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L298) | **Fuzzing de parsers** | Entradas malformadas em ambiente isolado, com limites e monitoramento. |
| [SDLC-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L299) | **IaC e container scanning** | Analisar Terraform, Kubernetes, Dockerfiles e imagens quanto a hardening e CVEs. |
| [SDLC-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L300) | **Lockfiles e versões fixas** | Controlar resolução de dependências e builds reproduzíveis onde possível. |
| [SDLC-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L301) | **Proteção de branch e revisão** | Aprovações, checks obrigatórios, Code Owners e política contra bypass. |
| [SDLC-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L302) | **OIDC para pipeline** | Trocar segredos long-lived por identidades de workload e tokens de vida curta. |
| [SDLC-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L303) | **Assinatura/proveniência de build** | Assinar artefatos, verificar attestation e cadeia de build segundo SLSA quando aplicável. |
| [SDLC-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L304) | **Isolamento de runners** | Separar contexto não confiável, PRs externos e produção; não compartilhar secrets. |
| [SDLC-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L305) | **Governança de pacotes** | Registry confiável, revisão de novos pacotes, nomes e integridade. |
| [SDLC-13](security-auditor/references/encyclopedia-v1.0.md?plain=1#L306) | **Releases progressivos** | Canary/blue-green, health checks, rollback e teste de segurança pós-deploy. |
| [SDLC-14](security-auditor/references/encyclopedia-v1.0.md?plain=1#L307) | **Testes de autorização** | Matriz usuário × tenant × recurso × ação com cenários negativos. |
| [SDLC-15](security-auditor/references/encyclopedia-v1.0.md?plain=1#L308) | **Testes regressivos de segurança** | Cada achado corrigido deve gerar teste que falhe na versão vulnerável. |
| [SDLC-16](security-auditor/references/encyclopedia-v1.0.md?plain=1#L309) | **Artefatos de evidência** | Repositório, commit, arquivo/linha, regra, impacto, reprodução não destrutiva e fix. |

### OPS — Operação, detecção e resposta

| ID | Controle | Critério de revisão |
| --- | --- | --- |
| [OPS-01](security-auditor/references/encyclopedia-v1.0.md?plain=1#L315) | **Logs estruturados** | Identidade, resultado, recurso, correlation ID, timestamp confiável; sem segredos. |
| [OPS-02](security-auditor/references/encyclopedia-v1.0.md?plain=1#L316) | **Auditoria de segurança** | Sucessos e falhas de autenticação, autorização, administração, exportações e segredos. |
| [OPS-03](security-auditor/references/encyclopedia-v1.0.md?plain=1#L317) | **Centralização e integridade** | SIEM/log pipeline protegido, retenção adequada, restrições de acesso e imutabilidade conforme risco. |
| [OPS-04](security-auditor/references/encyclopedia-v1.0.md?plain=1#L318) | **Alertas acionáveis** | Detectar credential stuffing, mudanças de papel, exfiltração, picos de erros e tráfego. |
| [OPS-05](security-auditor/references/encyclopedia-v1.0.md?plain=1#L319) | **Métricas RED/USE e SLO** | Avaliar taxa, erros, latência, recursos e degradações atípicas. |
| [OPS-06](security-auditor/references/encyclopedia-v1.0.md?plain=1#L320) | **Playbooks de incidente** | Contenção, triagem, preservação de evidências, comunicação, recuperação e lições aprendidas. |
| [OPS-07](security-auditor/references/encyclopedia-v1.0.md?plain=1#L321) | **Rotação e revogação emergencial** | Capacidade comprovada de invalidar tokens, chaves, contas e integrações comprometidas. |
| [OPS-08](security-auditor/references/encyclopedia-v1.0.md?plain=1#L322) | **Threat hunting autorizado** | Investigar hipóteses baseadas em ATT&amp;CK e detecções, respeitando privacidade. |
| [OPS-09](security-auditor/references/encyclopedia-v1.0.md?plain=1#L323) | **Testes de backup/restore** | Verificar integridade, tempo de recuperação e chaves de descriptografia. |
| [OPS-10](security-auditor/references/encyclopedia-v1.0.md?plain=1#L324) | **Monitoramento de KEV** | Priorizar correções de falhas exploradas, especialmente serviços expostos. |
| [OPS-11](security-auditor/references/encyclopedia-v1.0.md?plain=1#L325) | **Observabilidade de anti-abuso** | Detectar scraping, bots, enumeração, criação massiva de contas e fraudes. |
| [OPS-12](security-auditor/references/encyclopedia-v1.0.md?plain=1#L326) | **Segurança dos próprios logs** | Prevenir log injection, saturação, vazamento e adulteração das trilhas. |


</details>

Um controle pode depender de uma ação do responsável pelo ambiente. A skill não deve adicionar
todos os controles a todo projeto nem tratar a instalação de uma biblioteca como prova de proteção.

<a id="correcoes"></a>

## Correções e implementações possíveis

O quadro abaixo exemplifica mudanças que o agente pode preparar e, quando forem locais e
estiverem no escopo aprovado, implementar. A decisão depende do fluxo real do projeto. O catálogo
completo acima também inclui medidas operacionais e de infraestrutura que exigem atuação externa.

| Problema validado | Mudança que pode ser proposta | Verificação esperada |
| --- | --- | --- |
| SQL injection | Substituir concatenação por parâmetros e restringir a montagem da consulta. | Entrada maliciosa tratada como dado e consulta legítima preservada. |
| NoSQL/operator injection | Validar tipos e esquemas; rejeitar operadores que o cliente não pode fornecer. | Objetos inesperados não alteram filtros nem retornam registros extras. |
| XSS e conteúdo HTML indevido | Encoding no contexto de saída, saída textual e sanitizador quando HTML rico for necessário. | Conteúdo controlado pelo usuário não executa script e o conteúdo permitido funciona. |
| Autorização por objeto ausente | Vincular a busca ao principal/tenant e verificar a ação no servidor. | Usuário A não acessa nem altera o recurso de B. |
| Mass assignment | Introduzir DTO ou allowlist para propriedades que o cliente pode modificar. | Campos como papel, tenant e saldo não são alterados pelo corpo da requisição. |
| Sessão ou cookie frágil | Configurar flags, escopo, rotação e expiração conforme o contexto. | Fluxo legítimo preservado; cookie e invalidação de sessão verificados. |
| Validação de JWT incompleta | Permitir algoritmos definidos, conferir claims e usar chaves confiáveis. | Assinatura inválida, emissor/audiência errados e token expirado são rejeitados. |
| CSRF | Proteger operações autenticadas por credencial automática com token e validação apropriada de origem. | Mudança de estado sem a proteção necessária é rejeitada. |
| CORS permissivo | Restringir origens conhecidas e credenciais de forma compatível com a aplicação. | Origem não autorizada não recebe a permissão; integrações legítimas continuam funcionando. |
| SSRF | Restringir protocolos e destinos; validar o destino final e redirects; propor egress quando necessário. | Acesso a destinos privados/metadados bloqueado antes da conexão, usando mocks. |
| Path traversal | Restringir diretórios, normalização e resolução do caminho; usar identificadores indiretos. | Caminhos que escapam da área permitida são recusados. |
| Upload inseguro | Validar tipo real, tamanho e armazenamento; controlar nomes e acesso aos arquivos. | Arquivo proibido ou excessivo é rejeitado e não vira conteúdo executável. |
| Execução de shell ou desserialização perigosa | Usar APIs adequadas, argumentos separados e formatos/tipos permitidos. | Entrada não controla interpretação, argumentos privilegiados ou execução. |
| Webhook sem integridade | Verificar assinatura no corpo correto, timestamp e deduplicação do evento. | Assinatura inválida e replay são recusados sem duplicar efeitos. |
| Corridas e operações duplicadas | Aplicar atomicidade, idempotência e transições válidas no fluxo de negócio. | Repetição ou concorrência limitada não duplica cobrança nem viola invariantes. |
| Abuso de recursos | Definir limites de payload, tempo, custo, paginação, fan-out e concorrência. | Testes locais limitados confirmam o bloqueio sem gerar carga destrutiva. |
| Vazamento em logs ou erros | Redigir dados sensíveis e separar detalhes internos das respostas públicas. | Logs e respostas sanitizados, preservando a capacidade de diagnóstico. |
| Segredo no código | Remover a referência insegura, usar configuração protegida e orientar revogação pelo responsável. | A remoção é conferida; o achado de credencial exige evidência da revogação para encerramento. |
| Dependência vulnerável aplicável | Propor a versão mínima corrigida, atualizar pelo gerenciador e revisar o lockfile. | Advisory e alcançabilidade avaliados; testes e build executados. |
| Docker com privilégios excessivos | Propor usuário apropriado, capacidades mínimas e configuração de runtime compatível. | A aplicação funciona com os privilégios previstos e sem permissões desnecessárias. |
| Pipeline excessivamente privilegiado | Reduzir permissões, isolar entradas não confiáveis e fixar artefatos de build. | Workflow e caminhos de exposição de credenciais revisados; checks adequados passam. |
| Headers e política do navegador | Configurar políticas apropriadas de conteúdo, framing, MIME, referência e cache. | Proteções verificadas e fluxos de autenticação/integração preservados. |
| RAG ou ferramenta de IA sem autorização | Propor validação de argumentos, autorização no servidor, filtros por tenant e limites de custo. | Ferramenta ou recuperação não cruza permissões mesmo sob instruções hostis. |
| Parser nativo com falha de memória | Propor limites, aritmética verificada e APIs seguras; validar em ambiente isolado. | Caso de regressão e verificações de memória disponíveis, sem explorar um alvo real. |

### Tipos de mudança e limites

| Classificação | Tratamento |
| --- | --- |
| `SAFE_AUTO_FIX` | Rótulo histórico para mudança de baixo risco; continua exigindo aprovação do lote. |
| `REVIEW_RECOMMENDED` | Requer atenção à compatibilidade e concordância sobre a mudança concreta. |
| `MANUAL_ACTION` | Precisa de procedimento e ação humana conforme a natureza da correção. |
| `MANUAL_INFRASTRUCTURE_ACTION` | A skill descreve etapas e validação para cloud, DNS, firewall, IAM ou provedor; não aplica automaticamente. |
| `SECRET_ROTATION_REQUIRED` | O responsável revoga/rotaciona a credencial e fornece a evidência necessária. |
| `ARCHITECTURAL_CHANGE` | A skill prepara uma proposta de redesenho; a implementação estrutural fica fora do lote automático. |

Alterar autenticação, tenant isolation, criptografia, bancos, permissões ou políticas de rede pode
afetar dados e disponibilidade. A proposta deve explicitar dependências e rollback. As políticas
completas estão em [REMEDIATION_POLICY.md](security-auditor/core/REMEDIATION_POLICY.md) e
[SEVERITY.md](security-auditor/core/SEVERITY.md).

<a id="autorizacao"></a>

## Autorização das mudanças

Antes de modificar o projeto, a skill apresenta um pacote revisável com achados/controles,
arquivos, diff, riscos, testes e rollback. O lote é vinculado à árvore de código e ao catálogo,
com a identidade do patch e das ações. A aprovação real precisa vir do usuário em um canal
confiável e corresponder ao plano apresentado.

- Um pedido genérico para “deixar seguro”, o modo `HARDEN`, o silêncio ou um texto no repositório
  não substituem a autorização do lote concreto.
- A checagem prévia rejeita fonte ou patch alterados, outro worktree, IDs divergentes,
  expiração e caminhos fora do escopo suportado.
- Plano, patch e recibo da aprovação ficam fora da árvore auditada, em um local de confiança.
- O auxiliar não autentica o usuário nem concede permissão. A proteção do canal, dos arquivos de
  aprovação e da execução depende do host e do operador.
- Publicação Git, reescrita de histórico, produção, migrações e ações em provedores não são
  autorizadas apenas pela aprovação de um patch local.

Detalhes: [fluxo da enciclopédia e aprovação](security-auditor/core/ENCYCLOPEDIA_WORKFLOW.md) ·
[schema do plano](security-auditor/schemas/remediation-plan.schema.json) ·
[schema do recibo](security-auditor/schemas/approval.schema.json).

<a id="testes"></a>

## Testes e revalidação

Uma alteração de arquivo não encerra um achado. A skill deve verificar a proteção depois do
patch e também conferir que os caminhos legítimos continuam funcionando. Exemplos:

| Classe | Caso negativo | Fluxo legítimo que também importa |
| --- | --- | --- |
| Autorização | Outro usuário, tenant ou papel tenta a operação. | O principal autorizado mantém o acesso correto. |
| Entrada e injeção | Tipo, operador, payload ou formato não permitido. | Entradas válidas continuam sendo processadas como dados. |
| Sessão/JWT | Token inválido, expirado ou sessão revogada. | Login, renovação e logout seguem o contrato previsto. |
| Upload e paths | Arquivo proibido, excessivo ou caminho fora da área. | Arquivos permitidos permanecem acessíveis ao dono correto. |
| Webhook e negócio | Assinatura inválida, replay ou operação duplicada. | Evento válido produz um único efeito esperado. |
| IA e agentes | Documento hostil ou tentativa de operação fora da permissão. | Ferramentas legítimas obedecem ao usuário, tenant e orçamento. |

Para correções críticas e altas, a política exige regressão quando tecnicamente possível,
preferencialmente com um teste que falhe na versão vulnerável. O agente também seleciona os
comandos relevantes de lint, tipos, testes, integração e build do projeto e os scanners adequados
ao problema. Falhas anteriores e verificações indisponíveis precisam ser relatadas.

Testes que não rodaram não devem ser apresentados como aprovados. Cenários dinâmicos precisam
de autorização e ambiente controlado; o catálogo não autoriza DoS, phishing, uso de credenciais
encontradas ou exploração de serviços de terceiros.

A suíte deste repositório valida os auxiliares, contratos, cobertura e gate. Ela não é um benchmark
que prove a detecção automática de todos os cenários do catálogo.

<a id="resultados"></a>

## Relatórios e estado persistente

Quando a gravação estiver permitida, os resultados ficam no projeto analisado:

| Arquivo ou diretório | Finalidade |
| --- | --- |
| `security/SECURITY_AUDIT.md` | Visão geral, riscos, achados, cobertura e limitações. |
| `security/FINDINGS.md` | Evidências, impacto, causa, proposta, teste e verificação de cada achado. |
| `security/SECURITY_MATRIX.md` | Relação entre controle, estado, evidência e risco. |
| `security/ATTACK_SURFACE.md` e `security/THREAT_MODEL.md` | Superfícies, ativos e fronteiras de confiança. |
| `security/REMEDIATION_PLAN.md` | Lotes propostos, prioridades, dependências e ações externas. |
| `security/SECURITY_CHANGES.md` | Mudanças autorizadas, motivação e resultados observados. |
| `security/SECURITY_BASELINE.md` | Estado esperado para comparação em análises futuras. |
| `security/PRODUCTION_READINESS.md` | Avaliação de prontidão, bloqueios e evidências faltantes. |
| `.security/findings.json` e `.security/controls.json` | IDs persistentes, ciclo dos achados e controles. |
| `.security/architecture.json` | Componentes, fluxos e fronteiras descobertas. |
| `.security/baseline.json`, `.security/risk-register.json` e `.security/last-audit.json` | Política, riscos aceitos e contexto da auditoria. |
| `.security/encyclopedia-coverage.json` | Contabilidade da revisão dos 136 controles e 507 cenários. |

Com `--no-write`, a entrega acontece no chat. Evidências, relatórios e estado não devem armazenar
segredos nem dados pessoais desnecessários. Um número de cobertura ou uma pontuação não substitui
a avaliação dos riscos e dos controles críticos ainda não verificados.

<a id="scripts"></a>

## Scripts auxiliares e CI

Estes, sim, são comandos de terminal. Execute a partir de uma cópia de confiança da skill,
substituindo os caminhos do exemplo pelos locais reais do seu ambiente.

### Descoberta e cobertura

```bash
python security-auditor/scripts/encyclopedia.py profile --root /caminho/do/projeto
python security-auditor/scripts/encyclopedia.py validate-coverage --root /caminho/do/projeto --coverage /caminho/do/ledger.json
```

O perfil nasce com os itens não verificados. A validação de cobertura confere correspondência,
IDs, estados, evidências declaradas e referências a findings; não comprova que uma evidência é
verdadeira. Uma revisão completa pode encontrar vulnerabilidades ainda abertas.

### Plano e checagem da aprovação

```bash
python security-auditor/scripts/encyclopedia.py plan-digest --plan /local-confiavel/plano.json
python security-auditor/scripts/encyclopedia.py approval-check --root /caminho/do/projeto --plan /local-confiavel/plano.json --approval /local-confiavel/aprovacao.json --patch /local-confiavel/mudancas.patch
```

O recibo só pode ser registrado após o consentimento real. A checagem não cria autorização e não
aplica o patch. O fluxo completo e as restrições dos patches suportados estão no
[guia operacional](security-auditor/core/ENCYCLOPEDIA_WORKFLOW.md).

### Estado e gate

```bash
python security-auditor/scripts/security_auditor.py source-digest --root /caminho/do/projeto
python security-auditor/scripts/security_auditor.py validate --root /caminho/do/projeto
python security-auditor/scripts/security_auditor.py gate --root /caminho/do/projeto
```

O gate precisa de estado real e de uma política configurada; os templates iniciais ficam
incompletos até a auditoria. A nova baseline exige `requireEncyclopediaCoverage: true`.
Políticas anteriores podem ativar essa exigência por uma atualização revisada.

Os templates de [GitHub Actions](security-auditor/templates/ci/github-actions-security-gate.yml) e
[GitLab CI](security-auditor/templates/ci/gitlab-security-gate.yml) devem ser adaptados à stack e
carregar política e runtime de uma fonte protegida. O gate valida o estado e bloqueia resultados
incompletos/inconsistentes conforme o contrato; ele não executa todos os scanners.

Ferramentas de SAST, SCA, segredos, IaC, containers e DAST são selecionadas conforme o problema.
Sua presença, instalação e execução não são presumidas. Consulte o
[catálogo de ferramentas](security-auditor/catalog/tools/README.md) e as
[regras de execução](security-auditor/core/TOOL_EXECUTION.md).

### Verificar a própria skill

```bash
python -m unittest discover -s security-auditor/tests/unit -v
python security-auditor/scripts/build_encyclopedia.py
git diff --check
```

O importador verifica se o catálogo corresponde à enciclopédia original. A regeneração com
`--write` é uma operação de manutenção deliberada, não parte de uma auditoria consumidora.

<a id="contribuir"></a>

## Contribuição e comunidade

Há várias formas de participar: corrigir documentação, melhorar exemplos, revisar referências,
relatar falsos positivos, criar fixtures sintéticas, acrescentar testes de regressão, propor
controles e aprimorar scripts ou templates.

- [Relatar um bug](https://github.com/lucianumm/Security/issues/new?template=bug_report.yml).
- [Propor uma melhoria](https://github.com/lucianumm/Security/issues/new?template=feature_request.yml).
- [Revisar catálogo ou falso positivo](https://github.com/lucianumm/Security/issues/new?template=catalog_review.yml).
- [Tirar uma dúvida](https://github.com/lucianumm/Security/issues/new?template=question.yml).
- [Abrir um pull request](https://github.com/lucianumm/Security/compare) seguindo o template.
- Apoiar com o [QR Code ou Pix copia e cola](#apoie-o-projeto).

| Documento | O que você encontra |
| --- | --- |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Preparação da mudança, revisão do catálogo, testes e envio de PR. |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Padrões de convivência, relato reservado e responsabilidade de moderação. |
| [SUPPORT.md](SUPPORT.md) | Canais para dúvidas, bugs, sugestões e limites do suporte comunitário. |
| [SECURITY.md](SECURITY.md) | Escopo e canal privado para vulnerabilidades na própria skill. |
| [Template de PR](.github/PULL_REQUEST_TEMPLATE.md) | Problema, mudança, validação, impacto e conferência antes da revisão. |
| [Formulários de issues](.github/ISSUE_TEMPLATE/) | Pedidos organizados conforme o tipo de contribuição. |
| [LICENSE](LICENSE) | Texto integral da licença MIT. |

<a id="reporte"></a>

## Reporte privado de vulnerabilidades

Se encontrar uma falha na própria skill, nos scripts, schemas ou templates distribuídos, use
**[Report a vulnerability](https://github.com/lucianumm/Security/security/advisories/new)** na área
de segurança do GitHub. O formulário solicita componente, impacto, precondições e reprodução segura.

Não publique credenciais ou detalhes exploráveis em uma issue. Problemas de aplicações analisadas
pela skill devem ser enviados ao responsável pelo projeto afetado, pelo canal autorizado por ele.
Este repositório não concede permissão para testar sistemas de terceiros. Veja a
[Política de Segurança](SECURITY.md) antes do envio.

<a id="limites"></a>

## Limites e interpretação dos resultados

A skill depende da qualidade da análise do agente, do acesso aos arquivos e ambientes, dos
testes disponíveis e das informações atuais sobre as tecnologias utilizadas. Os cenários são
famílias de ameaças e referências defensivas; não equivalem a todas as técnicas, CVEs ou variantes
existentes.

Configurações de cloud, DNS, IdP, WAF, backups, controles humanos e sistemas fora do repositório
continuam não verificados até haver evidência suficiente. O código do aplicativo não comprova
sozinho esses controles. Um rate limiter não demonstra proteção contra DDoS volumétrico, e remover
uma credencial do código não prova sua revogação.

As edições usadas nos mapeamentos estão em
[`standards.lock.json`](security-auditor/references/standards.lock.json). Elas identificam as
referências adotadas, não garantem que os documentos ou advisories permaneçam os mais recentes.
Uma execução offline deve explicitar que a inteligência atual de vulnerabilidades não foi verificada.

Nenhum controle deve ser marcado como implementado por ausência de achados. Uma correção só deve
ser encerrada com verificação posterior. A auditoria não garante identificar todas as falhas,
certificar conformidade ou tornar o projeto 100% seguro.

<a id="licenca"></a>

## Licença

O projeto é disponibilizado sob a **[licença MIT](LICENSE)**. Ela permite usar, copiar, modificar e
redistribuir o material conforme seus termos, preservando o aviso de copyright e a licença. O
software é fornecido sem garantia. Referências e materiais externos permanecem sujeitos aos termos
dos respectivos titulares. Uma cópia da licença acompanha também a pasta portátil da skill.

## Créditos

Criado e mantido por **Lucianum**.

- **Instagram:** [@lucianum](https://www.instagram.com/lucianum/)
- **GitHub:** [@lucianumm](https://github.com/lucianumm)
