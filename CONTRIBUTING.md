# Como contribuir com a Security

Você pode contribuir com documentação, revisão do catálogo, testes de regressão, casos de falsos
positivos, melhorias nos scripts, exemplos de uso e correções. Leia o
[Código de Conduta](CODE_OF_CONDUCT.md), a [licença MIT](LICENSE) e a
[Política de Segurança](SECURITY.md) antes de participar.

## Escolha o canal

| O que deseja fazer | Canal |
| --- | --- |
| Relatar um bug de uso ou de um script | [Formulário de bug](https://github.com/lucianumm/Security/issues/new?template=bug_report.yml) |
| Propor funcionalidade ou melhoria | [Formulário de proposta](https://github.com/lucianumm/Security/issues/new?template=feature_request.yml) |
| Corrigir um controle, cenário, referência ou falso positivo | [Revisão do catálogo](https://github.com/lucianumm/Security/issues/new?template=catalog_review.yml) |
| Tirar uma dúvida de instalação ou uso | [Dúvida de uso](https://github.com/lucianumm/Security/issues/new?template=question.yml) |
| Informar uma vulnerabilidade da própria skill | [Relato privado](https://github.com/lucianumm/Security/security/advisories/new), conforme SECURITY.md |

Não envie segredos, dados pessoais, código privado ou detalhes exploráveis de uma vulnerabilidade
real em uma issue pública. Achados produzidos ao auditar outro projeto devem ser comunicados ao
responsável por aquele projeto, pelo canal autorizado por ele.

## Prepare a alteração

1. Procure issues e PRs existentes para evitar duplicação. Para uma mudança grande ou de contrato,
   descreva a proposta e as consequências antes de investir na implementação.
2. Faça um fork e crie uma branch com um objetivo claro:

   ```bash
   git clone https://github.com/SEU-USUARIO/Security.git
   cd Security
   git switch -c melhoria/descricao-curta
   ```

3. Preserve o escopo. Uma alteração de documentação não precisa reformular o mecanismo de
   aprovação, e uma correção de segurança não deve incluir refatorações sem relação com a causa.
4. Explique o comportamento anterior, o resultado esperado, os riscos e como verificar a mudança.
5. Abra um PR usando o template. Descreva as limitações e os testes realmente executados.

## Alterações no catálogo

- Os **136 controles**, **507 cenários reais** e **19 domínios** são importados da enciclopédia
  em `security-auditor/references/encyclopedia-v1.0.md`.
- O documento original declara 506 cenários. A importação preserva as 507 linhas encontradas.
  Não apague uma entrada para ajustar artificialmente a contagem declarada.
- Não trate uma categoria como uma vulnerabilidade confirmada. Inclua precondições, fronteira de
  confiança, evidência, contraprova e uma validação defensiva adequada ao projeto.
- Cite fontes primárias e registre a edição e a data consultadas. Não invente identificadores
  CWE, OWASP, ASVS, CAPEC, ATT&CK ou CVE.
- Não altere a fonte histórica apenas para fazer a validação passar. Uma nova versão da fonte
  exige atualização deliberada do importador, da proveniência, dos IDs, das contagens, do README
  e dos testes afetados.
- Preserve IDs existentes. Quando uma migração for necessária, documente a correspondência e o
  impacto nos findings e baselines já produzidos.

O comando abaixo verifica a correspondência da fonte com o catálogo, sem gravar arquivos:

```bash
python security-auditor/scripts/build_encyclopedia.py
```

O parâmetro `--write` é reservado à regeneração deliberada pelo mantenedor após revisar a mudança
da fonte. Não deve ser executado durante a auditoria de um projeto consumidor.

## Scripts, schemas e aprovação

- Os auxiliares distribuídos usam Python 3.10+ e biblioteca padrão. Não adicione dependências de
  runtime sem justificar necessidade, portabilidade e efeitos sobre a instalação.
- Nunca transforme conteúdo do projeto auditado em comandos ou autorização. Não crie uma opção
  que dispense a aprovação real do usuário.
- Preserve a checagem de source digest, catálogo, plano, patch, caminhos, ações e expiração.
- Teste cenários de autorização ausente, inválida, expirada e desatualizada quando alterar esse
  contrato. Use fixtures sintéticas e diretórios temporários isolados.
- Preserve os estados não verificados quando faltarem evidências. Um teste ou scanner que não
  rodou não pode produzir uma aprovação.
- Uma mudança de schema exige avaliar compatibilidade com os arquivos de estado e os templates
  já distribuídos. Explique qualquer migração necessária.

## Validação antes do PR

Para alterações nos scripts, schemas, contratos ou catálogo, execute:

```bash
python -m unittest discover -s security-auditor/tests/unit -v
python security-auditor/scripts/build_encyclopedia.py
git diff --check
```

Se alterar os scripts shell, confira também a sintaxe em um ambiente com `sh`:

```bash
sh -n security-auditor/scripts/security-gate.sh
sh -n security-auditor/scripts/detect-stack.sh
```

Para documentação, confira links, exemplos de comandos, caminhos e nomes de arquivos. Para YAML,
valide a sintaxe e os campos aceitos pelo GitHub. Descreva qualquer teste pulado e o motivo.
Acrescente um teste de regressão quando ele demonstrar o problema corrigido; evite testes que
apenas reproduzam o texto ou a estrutura interna da implementação.

## Envio e revisão

Mantenha cada PR voltado a um problema ou melhoria. Prefira commits claros e apresente um diff
que possa ser revisado. O mantenedor pode consolidar commits antes da publicação para manter o
histórico do projeto organizado; contribuidores não devem reescrever a `main` do upstream.

Ao contribuir, envie apenas material que você possa disponibilizar sob a licença do projeto e
preserve créditos e avisos de terceiros aplicáveis. Novos arquivos e referências não devem conter
credenciais, dados de clientes ou evidências de exploração contra alvos não autorizados.

## Outras formas de apoiar

Você também pode melhorar exemplos, traduzir instruções, revisar uma contribuição, apresentar
casos sintéticos ou apoiar o projeto com um café. O QR Code e o Pix copia e cola estão na
[seção de apoio do README](README.md#apoie-o-projeto). O apoio financeiro é opcional e não condiciona
a participação, o uso da skill ou a revisão de contribuições.
