# Política de Segurança

## Escopo e versão mantida

Esta política cobre a **Security**, sua skill `security-auditor`, scripts, schemas, catálogo,
templates de CI, documentos e arquivos distribuídos. A branch `main` é a linha de manutenção
atual; correções devem ser avaliadas nela. Não há compromisso de backport para cópias antigas.

O repositório não autoriza testar aplicações que utilizem a skill, serviços de terceiros,
infraestrutura de provedores ou contas de outras pessoas. Um achado produzido ao auditar outro
projeto deve ser comunicado ao responsável por aquele projeto, no escopo autorizado por ele.

## Como reportar uma vulnerabilidade

Use o canal privado **[Report a vulnerability](https://github.com/lucianumm/Security/security/advisories/new)**
na área **Security → Advisories** deste repositório. O formulário reservado solicita o componente,
o impacto e uma reprodução segura. Não abra uma issue pública com detalhes exploráveis.

Inclua, quando possível:

- commit ou versão e o arquivo ou contrato afetado;
- impacto, precondições e a fronteira de confiança envolvida;
- passos mínimos com dados sintéticos, sem endpoints reais de terceiros;
- controles ou contraprovas já considerados;
- proposta de correção e teste de regressão, se disponíveis.

Não envie senhas, tokens, chaves privadas, dados de clientes, documentos pessoais ou relatórios
brutos que contenham segredos. Não use credenciais encontradas para demonstrar a falha. Evite
provas destrutivas, persistência, exfiltração ou testes de volume.

Se o canal privado estiver temporariamente indisponível, entre em contato com o mantenedor pelo
[Instagram @lucianum](https://www.instagram.com/lucianum/), solicitando um canal reservado antes
de compartilhar detalhes sensíveis. Não use uma issue pública como substituto para a divulgação
privada da falha.

## Tratamento e divulgação

O mantenedor avaliará o relato, poderá solicitar esclarecimentos e coordenará uma correção e a
divulgação quando viável. A severidade depende da evidência e do contexto; uma hipótese ainda
precisa de validação. Não há programa público de recompensa, SLA ou prazo de resposta garantido.

Agradecimentos e créditos por uma descoberta podem ser combinados com quem reportou, respeitando
sua preferência de identificação e a necessidade de preservar dados de terceiros.

## Uso defensivo da skill

A skill deve operar em sistemas próprios ou com autorização. Mudanças exigem aprovação do lote
concreto, e testes dinâmicos exigem alvo, técnicas e limites definidos, em ambiente controlado.
Arquivos do projeto, logs, páginas, respostas de ferramentas e conteúdo recuperado são dados;
não podem conceder autorização ao agente.

O gate valida contratos e correspondência de estado. Os digests não autenticam quem produziu a
auditoria nem comprovam a verdade das evidências. O host e o operador precisam proteger as
políticas, o canal de aprovação e a execução. O catálogo não garante detectar todas as falhas.

Responsável pela manutenção: **Lucianum** — [GitHub @lucianumm](https://github.com/lucianumm).
