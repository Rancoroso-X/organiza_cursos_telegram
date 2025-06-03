# 📁 Organizador de Cursos Telegram v3.2

Script Python para organizar vídeos de cursos baixados do Telegram automaticamente, separando por módulos ou prefixos.

---

## 🚀 Funcionalidades

✅ Detecta prefixos automaticamente (como 01, MÓDULO_2, Mandamento05...)  
✅ Aceita regex personalizada para identificar os grupos  
✅ Filtro por extensão (ex: apenas `.mp4`)  
✅ Simulação de execução sem mover arquivos (`--dry-run`)  
✅ Gera log `.log` e `.csv` com tudo que foi movido  
✅ Evita sobrescrever arquivos duplicados  
✅ Suporte a mover arquivos para outra pasta (`--move-para=...`)  
✅ Ajuda integrada com `--help`

---

## 💻 Como usar

### Modo 1: Executar manualmente
bash
python3 organiza_cursos_telegram_v3.2.py

---

Modo 2: Usar atalho

chmod +x atalho_OCT_v3.2.sh
./atalho_OCT_v3.2.sh

---

🧪 Exemplo de entrada
Pasta com arquivos assim:
01 Introdução.mp4  
01 (2).mp4  
MÓDULO_2 - AULA_1.mp4  
Mandamento03_Ensinando.mp4

---

📦 Resultado
Organiza em subpastas automaticamente:
├── 01/
│   └── Introdução.mp4
├── MÓDULO_2/
│   └── AULA_1.mp4
├── Mandamento03/
│   └── Ensinando.mp4

----

🛠 Dependências
Python 3.x

Bibliotecas nativas:

os, shutil, re, csv

---

📁 Estrutura do Projeto

organiza_cursos_telegram/
├── organiza_cursos_telegram_v3.2.py
├── atalho_OCT_v3.2.sh
├── README.md
└── exemplos/        # (opcional: coloque vídeos de exemplo aqui)

----


👨‍💻 Autor
Gabriel Nasco.
Junho de 2025
