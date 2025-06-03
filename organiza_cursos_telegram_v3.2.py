"""
======================================================================================
VERSÃO 3.2 — Organização Final com CLI Avançado e Segurança de Arquivos

======================================================================================
📦 O QUE FAZ ESSE SCRIPT:

Organiza automaticamente arquivos de vídeo e documentos misturados em uma pasta,
detectando padrões nos nomes para separá-los em subpastas organizadas por módulo, aula ou capítulo.

Agora o script está 100% automatizado e interativo com recursos avançados:

✅ Identificação inteligente de prefixos com padrões prontos OU regex customizado  
✅ Filtro por extensão: organize apenas arquivos `.mp4`, `.pdf`, `.zip`, etc  
✅ Suporte a execução automática via terminal com múltiplos argumentos  
✅ Flag `--dry-run`: simula a organização sem mover arquivos  
✅ Flag `--move-para=PASTA`: organiza os arquivos em uma pasta externa definida  
✅ Flag `--no-log`: desativa geração dos arquivos `movimentos.log` e `movimentos.csv`  
✅ Proteção contra sobrescrita: arquivos duplicados recebem sufixo automático (`_1`, `_2`...)  
✅ Exportação para `.csv` com coluna de arquivo, prefixo e pasta de destino  
✅ Ajuda interativa com `--help` explicando sintaxe e exemplos

======================================================================================
🧠 FLUXO DO SCRIPT:

1. Define o caminho da pasta base (via terminal ou input)
2. Pergunta se deseja usar uma regra personalizada (regex)
   - Se SIM: recebe regex custom (ex: `^(\\d+)`)
   - Se NÃO: aplica padrões internos pré-definidos
3. Analisa todos os arquivos válidos na pasta
4. Mostra os prefixos detectados (ex: `01`, `MÓDULO_2`, etc)
5. Você escolhe os prefixos que deseja organizar (ou todos)
6. Move os arquivos para subpastas correspondentes
7. Gera log em `.log` e `.csv` (opcional)

======================================================================================
📚 PADRÕES INTERNOS (se regex custom não for usado):

- `[prefixo]` → arquivos com colchetes
- `MÓDULO_2`, `Modulo-03`, etc
- `01. Nome`, `3_10.mp4`, `4 Nome da aula`
- `2 (1).mp4` → arquivos com numeração entre parênteses
- `reencode_01`, `reencode-02` → muito comum em vídeos exportados

======================================================================================
📄 SAÍDA:

- Subpastas criadas automaticamente com os prefixos encontrados
- Arquivos movidos com segurança (sem sobrescrever)
- Logs gerados: `movimentos.log` (texto) e `movimentos.csv` (planilha)

======================================================================================
💻 COMO USAR:

1. Salve como `organiza_cursos_telegram_v3.2.py`
2. Execute no terminal:  python3 organiza_cursos_telegram_v3.2.py ./minha_pasta s "^(\\d+)" mp4 --move-para=./Organizados
3. Ou apenas: python3 organiza_cursos_telegram_v3.2.py
Siga as instruções interativas

======================================================================================
🛠 DEPENDÊNCIAS:

Somente bibliotecas nativas:
-os
-shutil
-re
-sys
-csv

======================================================================================
Autor: Gabriel Nasco + SUPORTE T.I.A.I.
Data: Junho de 2025
======================================================================================
""" 

import os
import sys
import shutil
import re
import csv

# ✅ Ajuda interativa
if '--help' in sys.argv:
    print("""
🆘 Ajuda - Uso do Script:
python3 organiza_cursos.py [caminho] [s/n] [regex] [extensão] [--move-para=/novo/caminho] [--dry-run] [--no-log]

Exemplo:
  python3 organiza_cursos.py ./videos s "^(\\d+)" mp4 --move-para=../Organizados

Flags:
  --dry-run     ➜ Simula sem mover
  --move-para   ➜ Mover para pasta externa
  --no-log      ➜ Não salva .log nem .csv
  --help        ➜ Exibe ajuda
""")
    exit()

# ⚙️ Argumentos e flags
args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
flags = [arg for arg in sys.argv[1:] if arg.startswith('--')]

modo_automatico = len(args) >= 2
base_dir = args[0].strip('"') if len(args) >= 1 else input("📁 Caminho da pasta com os vídeos: ").strip()
usar_personalizado = args[1].lower() if len(args) >= 2 else input("Deseja usar uma regra personalizada? (s/n): ").strip().lower()
regex = args[2] if usar_personalizado == 's' and len(args) >= 3 else (input("Regex personalizada: ") if usar_personalizado == 's' else '')
extensao = args[3].lower() if len(args) >= 4 else None

# 🗃 Move externo (default = mesmo local)
destino_raiz = base_dir
for f in flags:
    if f.startswith('--move-para='):
        destino_path = f.split('=', 1)[1].strip().strip('"')
        if os.path.isabs(destino_path):
            destino_raiz = destino_path
        else:
            destino_raiz = os.path.abspath(os.path.join(base_dir, destino_path))

log_path = os.path.join(base_dir, 'movimentos.log')
csv_path = os.path.join(base_dir, 'movimentos.csv')

if not os.path.isdir(base_dir):
    print("❌ Caminho inválido.")
    exit(1)

# 🔠 Regras
padroes = [(regex, "custom")] if usar_personalizado == 's' and regex else [
    (r"^\[(.*?)\]", "[X]"),
    (r"M[OÓ]DULO[_\s-]?(\d+)", "MÓDULO_X"),
    (r"^(\d{1,2})\.(\d{1,2})", "X.Y"),
    (r"^(\d{1,2})[\.\s_-]", "X."),
    (r"^(\d+) \(", "X (n)"),
    (r"reencode[_-](\d{1,2})", "reencode_XX")
]

print("\n🔍 Analisando prefixos nos arquivos...")

def sugerir_prefixos():
    amostras = {}
    for nome in os.listdir(base_dir):
        if not os.path.isfile(os.path.join(base_dir, nome)) or (extensao and not nome.lower().endswith(f".{extensao}")):
            continue
        for padrao, _ in padroes:
            match = re.search(padrao, nome, re.IGNORECASE)
            if match:
                prefixo = match.group(1).strip()
                amostras.setdefault(prefixo, []).append(nome)
                break
    return amostras

sugestoes = sugerir_prefixos()
if not sugestoes:
    print("❌ Nenhum prefixo reconhecido.")
    exit(1)

print("\n📌 Prefixos encontrados:")
for i, (prefixo, lista) in enumerate(sugestoes.items(), 1):
    print(f"{i:2d}. {prefixo} → {len(lista)} arquivos")

usar_todos = 's' if modo_automatico else input("\nUsar TODOS os prefixos? (s/n): ").strip().lower()
prefixos_escolhidos = set(sugestoes.keys()) if usar_todos == 's' else set(p.strip() for p in input("Quais usar? ").split(','))

# 🧾 Logs
log = []
csv_data = []

def registrar(txt):
    print(txt)
    log.append(txt)

# 🧹 Limpa log anterior
if os.path.exists(log_path): os.remove(log_path)
if os.path.exists(csv_path): os.remove(csv_path)

# 🚀 Organização
for nome in os.listdir(base_dir):
    origem = os.path.join(base_dir, nome)
    if not os.path.isfile(origem) or (extensao and not nome.lower().endswith(f".{extensao}")):
        continue

    destino = None
    for padrao, _ in padroes:
        match = re.search(padrao, nome, re.IGNORECASE)
        if match:
            prefixo = match.group(1).strip()
            if prefixo in prefixos_escolhidos:
                destino = prefixo.replace(' ', '_')
            break

    if destino:
        pasta_destino = os.path.join(destino_raiz, destino)
        os.makedirs(pasta_destino, exist_ok=True)
        novo_nome = nome
        novo_caminho = os.path.join(pasta_destino, novo_nome)

        contador = 1
        while os.path.exists(novo_caminho):
            nome_base, ext = os.path.splitext(nome)
            novo_nome = f"{nome_base}_{contador}{ext}"
            novo_caminho = os.path.join(pasta_destino, novo_nome)
            contador += 1

        if '--dry-run' in flags:
            registrar(f"(Simulado) {nome} ➜ {destino}/")
        else:
            shutil.move(origem, novo_caminho)
            registrar(f"{nome} ➜ {destino}/")
        csv_data.append([nome, prefixo, destino])
    else:
        registrar(f"[IGNORADO] {nome} (sem padrão)")

# 💾 Gera log
if '--no-log' not in flags:
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Arquivo', 'Prefixo', 'Destino'])
        writer.writerows(csv_data)

print("\n📦 Organização concluída. Verifique 'movimentos.log' e 'movimentos.csv'.")
