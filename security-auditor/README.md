# security-auditor

Skill para orientar um agente de IA a analisar o projeto com base no catálogo de segurança,
identificar vulnerabilidades e controles necessários, propor correções e, após sua autorização,
implementá-las e testá-las.

## Instalação

Copie esta pasta inteira para o diretório de skills do seu agente. Preserve `SKILL.md`, `core/`,
`modules/`, `catalog/`, `references/`, `schemas/`, `templates/` e `scripts/`. Se o agente não tiver
instalação de skills, peça que leia [`SKILL.md`](SKILL.md) e os arquivos indicados nele antes da
análise. Os auxiliares exigem Git e Python 3.10 ou superior.

## Cobertura e correções

A skill inclui **507 cenários em 19 domínios**, **136 controles** e **25 módulos** para selecionar
o que é aplicável ao projeto. O catálogo cobre autenticação, sessões, autorização, injeções,
navegador, APIs, lógica de negócio, dados, criptografia, redes, cloud, containers, CI/CD,
endpoints, comunicação, mobile/desktop, IoT/OT, IA, controles humanos, memória e redes sem fio.

Consulte o [catálogo estruturado](catalog/encyclopedia.json), a
[enciclopédia de origem](references/encyclopedia-v1.0.md) ou o
[guia completo do repositório](https://github.com/lucianumm/Security#catalogo-completo), que explica
cada cenário, sua precondição e as defesas propostas. A fonte declara 506 cenários, mas a importação
preserva as 507 entradas reais; elas são referências de revisão, não detectores automáticos.

As propostas podem incluir consultas parametrizadas, encoding e sanitização, validação de entrada,
autorização por recurso, cookies e sessões, JWT, CSRF, CORS, uploads, paths, webhooks, limites de
recursos, dependências, logs, Docker, CI e ferramentas de IA. Cada mudança precisa de evidência,
análise de compatibilidade, diff, aprovação, teste e revalidação. Ações em provedores, revogação
de segredos e redesenhos estruturais recebem orientação e ficam sujeitos aos limites da política.

## Uso

Abra o projeto no agente e peça:

```text
Use a security-auditor para ler este projeto e identificar falhas com base no catálogo.
Apresente evidências, arquivos afetados, plano e diff das correções. Aguarde minha
autorização para o lote. Depois de autorizado, corrija, execute os testes previstos
e os testes disponíveis do projeto e revalide os achados.
```

Após revisar o plano, autorize os IDs e o diff concretos que deseja aplicar. A skill só deve
implementar esse escopo. Mudanças no código, no patch ou no escopo exigem revisão da autorização.

| Instrução no chat | Finalidade |
| --- | --- |
| `security-auditor AUDIT` | Analisar e propor; padrão. |
| `security-auditor AUDIT_AND_FIX` | Analisar, corrigir após aprovação, testar e revalidar. |
| `security-auditor HARDEN` | Propor e implementar controles necessários aprovados. |
| `security-auditor VERIFY` | Reavaliar correções e regressões. |
| `security-auditor TARGETED_AUDIT <área>` | Analisar uma área específica. |
| `security-auditor CI_GATE` | Validar o estado da auditoria contra a política do CI. |
| `security-auditor INCIDENT_REVIEW` | Examinar evidências de possível comprometimento. |

Essas instruções são pedidos ao agente; a skill não é um executável independente. Escolher um
modo de correção não substitui a aprovação do lote de mudanças.

## Opções e resultados

Use `--scope <caminho>` para limitar o escopo, `--no-write` para receber tudo no chat,
`--offline` para trabalhar sem rede, `--incremental` para rever mudanças ou `--full` para uma
análise completa. Testes dinâmicos com `--allow-dynamic` precisam de alvo e escopo autorizados.

Os relatórios ficam em `security/` e o estado da análise em `.security/`, quando a gravação estiver
permitida. A entrega deve separar achados, propostas, mudanças aprovadas e resultados reais dos
testes. Os testes e scanners disponíveis dependem do ambiente do projeto.

Testes não executados e controles externos sem evidência permanecem não verificados. A skill não
garante encontrar todas as vulnerabilidades ou tornar o projeto 100% seguro.

As instruções operacionais completas estão em [`SKILL.md`](SKILL.md). O fluxo do catálogo e da
autorização está em [`core/ENCYCLOPEDIA_WORKFLOW.md`](core/ENCYCLOPEDIA_WORKFLOW.md).

## Comunidade e licença

O projeto recebe contribuições de documentação, catálogo, casos sintéticos, testes e código.
Consulte o [guia de contribuição](https://github.com/lucianumm/Security/blob/main/CONTRIBUTING.md),
o [código de conduta](https://github.com/lucianumm/Security/blob/main/CODE_OF_CONDUCT.md) e os
[canais de suporte](https://github.com/lucianumm/Security/blob/main/SUPPORT.md). Falhas da própria
skill devem seguir o [reporte privado](https://github.com/lucianumm/Security/security/advisories/new).

Distribuído sob a [licença MIT](LICENSE). Preserve o aviso de copyright e a licença ao redistribuir
a pasta da skill. O QR Code e o Pix copia e cola estão na
[seção de apoio](https://github.com/lucianumm/Security#apoie-o-projeto).

## Créditos

Criado e mantido por **Lucianum**.

- **Instagram:** [@lucianum](https://www.instagram.com/lucianum/)
- **GitHub:** [@lucianumm](https://github.com/lucianumm)
