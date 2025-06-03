#!/bin/bash
# ─────────────────────────────────────────────
# Atalho robusto para organizar cursos (v3.2)
# Suporte total a caminhos com espaços e acentos
# ─────────────────────────────────────────────

echo "📁 Digite o caminho da pasta com os arquivos:"
read -r PASTA

echo "Deseja usar REGEX personalizada? (s/n)"
read -r USAR_REGEX

if [[ "$USAR_REGEX" == "s" ]]; then
  echo "Digite a regex personalizada (ex: ^(\\d+), M[oó]dulo_(\\d+), etc):"
  read -r REGEX
else
  REGEX=""
fi

echo "Filtrar por extensão? (ex: mp4, pdf, zip). Deixe em branco para todos:"
read -r EXTENSAO

echo "Deseja mover para outra pasta? (ex: /home/user/Organizados). Deixe em branco para manter no mesmo local:"
read -r DESTINO

echo "Simular organização sem mover arquivos? (s/n)"
read -r SIMULAR

echo "Deseja gerar logs? (s/n)"
read -r LOGAR

# Flags sem aspas internas
FLAGS=()
[[ -n "$DESTINO" ]] && FLAGS+=("--move-para=$DESTINO")
[[ "$SIMULAR" == "s" ]] && FLAGS+=("--dry-run")
[[ "$LOGAR" == "n" ]] && FLAGS+=("--no-log")

# Executa com todos os parâmetros entre aspas
python3 "$(dirname "$0")/organiza_cursos_telegram_v3.2.py" "$PASTA" "$USAR_REGEX" "$REGEX" "$EXTENSAO" "${FLAGS[@]}"
