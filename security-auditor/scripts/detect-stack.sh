#!/bin/sh
# detect-stack.sh — read-only technology detection for security-auditor.
#
# Prints the signals found in a repository and the audit modules they imply, so the skill loads
# only what is relevant (progressive disclosure, SKILL.md section 4).
#
# Usage: sh detect-stack.sh [path]   (default: current directory)
# Read-only: creates nothing, modifies nothing, contacts nothing.

set -u

ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || { echo "detect-stack: cannot enter '$ROOT'" >&2; exit 2; }

MODULES=""
add_module() {
  case " $MODULES " in
    *" $1 "*) : ;;
    *) MODULES="$MODULES $1" ;;
  esac
}

have_file() { [ -e "$1" ]; }
have_glob() {
  [ -n "$(find . \( -type d \( -name .git -o -name node_modules -o -name vendor -o -name .venv -o -name venv -o -name dist -o -name build -o -name .next -o -name target -o -name .terraform \) -prune \) -o -type f -name "$1" -print -quit 2>/dev/null)" ]
}
has_package_signal() {
  [ -n "$(find . \( -type d \( -name .git -o -name node_modules -o -name vendor -o -name dist -o -name build \) -prune \) -o -type f -name package.json -exec grep -qiE "$1" {} \; -print -quit 2>/dev/null)" ]
}
has_python_signal() {
  [ -n "$(find . \( -type d \( -name .git -o -name node_modules -o -name vendor -o -name .venv -o -name venv \) -prune \) -o -type f \( -name requirements.txt -o -name pyproject.toml -o -name Pipfile \) -exec grep -qiE "$1" {} \; -print -quit 2>/dev/null)" ]
}
has_composer_signal() {
  [ -n "$(find . \( -type d \( -name .git -o -name node_modules -o -name vendor \) -prune \) -o -type f -name composer.json -exec grep -qiE "$1" {} \; -print -quit 2>/dev/null)" ]
}
have_dir()  { [ -d "$1" ]; }
report()    { printf '  %-28s %s\n' "$1" "$2"; }
is_git_repo() { git rev-parse --is-inside-work-tree >/dev/null 2>&1; }

echo "security-auditor :: stack detection"
echo "root: $(pwd)"
echo

echo "[repository]"
if is_git_repo; then
  report "git" "yes (branch: $(git branch --show-current 2>/dev/null || echo unknown))"
  report "uncommitted changes" "$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') file(s)"
else
  report "git" "no"
fi
report "prior audit state" "$( [ -d .security ] && echo 'present (.security/)' || echo 'none' )"
report "prior reports" "$( [ -d security ] && echo 'present (security/)' || echo 'none' )"
echo

echo "[languages and package managers]"
have_glob package.json        && { report "node" "package.json/workspaces"; add_module supply-chain; }
have_file pnpm-lock.yaml      && report "lockfile" "pnpm-lock.yaml"
have_file yarn.lock           && report "lockfile" "yarn.lock"
have_file package-lock.json   && report "lockfile" "package-lock.json"
have_file bun.lockb           && report "lockfile" "bun.lockb"
{ have_glob requirements.txt || have_glob pyproject.toml || have_glob Pipfile; } \
                              && { report "python" "requirements/pyproject/Pipfile"; add_module supply-chain; }
have_glob composer.json       && { report "php" "composer.json"; add_module supply-chain; }
have_glob go.mod              && { report "go" "go.mod"; add_module supply-chain; }
have_glob Cargo.toml          && { report "rust" "Cargo.toml"; add_module supply-chain; }
have_glob Gemfile             && { report "ruby" "Gemfile"; add_module supply-chain; }
{ have_glob pom.xml || have_glob 'build.gradle*'; } \
                              && { report "jvm" "maven/gradle"; add_module supply-chain; }
{ have_glob '*.csproj' || have_glob '*.sln' || have_glob '*.slnx'; } \
                              && { report "dotnet" "project/solution manifest"; add_module supply-chain; }
have_file go.work             && report "go workspace" "go.work"
echo

echo "[frameworks and app shape]"
has_package_signal '"next"' && report "framework" "Next.js"
has_package_signal '"nuxt"' && report "framework" "Nuxt"
has_package_signal '"@angular/core"' && report "framework" "Angular"
has_package_signal '"svelte"' && report "framework" "Svelte"
has_package_signal '"vue"' && report "framework" "Vue"
has_package_signal '"react"' && report "framework" "React"
has_package_signal '"express"|"fastify"|"@nestjs/core"|"koa"|"hono"' && report "server" "Node HTTP framework"
has_package_signal '"graphql"|"@apollo' && report "api" "GraphQL"
has_package_signal '"socket.io"|"ws"' && report "api" "WebSocket"
has_package_signal '"prisma"|"typeorm"|"sequelize"|"drizzle-orm"|"mongoose"|"knex"' && report "orm" "present"
has_package_signal '"openai"|"@anthropic-ai/sdk"|"@ai-sdk|"langchain"' && { report "ai" "LLM SDK"; add_module ai-security; }
has_package_signal '"stripe"|"@paypal|"mercadopago"|"braintree"|"adyen"' && { report "payments" "provider SDK"; add_module payments; }
has_package_signal '"multer"|"formidable"|"busboy"|"@aws-sdk/client-s3"|"firebase' && { report "files" "upload/storage SDK"; add_module uploads; }
has_python_signal 'django' && report "framework" "Django signal"
has_python_signal 'flask' && report "framework" "Flask signal"
has_python_signal 'fastapi' && report "framework" "FastAPI signal"
has_composer_signal 'laravel/framework' && report "framework" "Laravel signal"
has_composer_signal 'symfony/' && report "framework" "Symfony signal"
{ have_glob 'schema.graphql' || have_glob '*.graphql'; } && report "api" "GraphQL schema file"
{ have_glob 'openapi.yaml' || have_glob 'openapi.json' || have_glob 'swagger.yaml' || have_glob 'swagger.json'; } && report "api" "OpenAPI/Swagger schema"
have_dir prisma             && report "orm" "Prisma (prisma/)"
{ have_dir migrations || have_dir db/migrate || have_dir alembic; } && report "database" "migrations present"
echo

echo "[infrastructure]"
have_glob 'Dockerfile*'          && { report "docker" "Dockerfile"; add_module docker; }
have_glob 'docker-compose*.y*ml' && { report "docker" "compose"; add_module docker; }
{ have_dir k8s || have_dir charts || have_dir helm || have_dir manifests; } && { report "kubernetes" "manifests/charts"; add_module kubernetes; }
{ have_dir terraform || have_dir infra || have_dir pulumi || have_dir cdk || have_glob '*.tf' || have_glob 'template*.yaml'; } && { report "iac" "present"; add_module cloud; }
{ have_glob 'nginx*.conf' || have_file Caddyfile || have_file .htaccess; } && { report "proxy" "reverse proxy config"; add_module nginx; }
{ have_file vercel.json || have_file netlify.toml || have_file wrangler.toml || have_file serverless.yml || have_file serverless.yaml; } && { report "platform" "serverless/edge"; add_module cloud; }
echo

echo "[ci/cd]"
have_dir .github/workflows     && { report "ci" "GitHub Actions"; add_module ci-cd; }
have_file .gitlab-ci.yml       && { report "ci" "GitLab CI"; add_module ci-cd; }
have_file bitbucket-pipelines.yml && { report "ci" "Bitbucket"; add_module ci-cd; }
have_file Jenkinsfile          && { report "ci" "Jenkins"; add_module ci-cd; }
echo

echo "[monorepo]"
{ have_file pnpm-workspace.yaml || have_file turbo.json || have_file nx.json || have_file lerna.json; } \
  && report "workspaces" "monorepo tooling detected"
for d in apps packages services; do
  [ -d "$d" ] && report "$d/" "$(find "$d" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ') package(s)"
done
echo

echo "[environment files present (names only — never read values aloud)]"
find . -maxdepth 3 \( -type d \( -name .git -o -name node_modules -o -name vendor -o -name .venv -o -name venv -o -name dist -o -name build \) -prune \) -o -type f -name '.env*' -print 2>/dev/null | sed 's/^/  /'
if is_git_repo; then
  # .env.example / .env.sample / .env.template are meant to be tracked — not a signal.
  tracked_env=$(git ls-files 2>/dev/null \
    | grep -E '(^|/)\.env|\.(pem|key|p12|pfx|jks)$|(^|/)id_rsa|credentials\.json$|\.tfstate$' \
    | grep -vE '\.(example|sample|template|dist)$' \
    | head -5)
  [ -n "$tracked_env" ] && { echo "  !! TRACKED IN GIT (investigate — modules/secrets.md):"; echo "$tracked_env" | sed 's/^/     /'; }
fi
echo

echo "[always-load modules]"
echo "  authentication authorization sessions secrets logging business-logic api backend frontend"
echo
echo "[additional modules implied by detection]"
echo " ${MODULES:- (none)}"
echo
echo "Note: this script reports signals only. Confirm each one by reading the code before"
echo "loading a module or recording a control status (core/EVIDENCE_RULES.md)."
