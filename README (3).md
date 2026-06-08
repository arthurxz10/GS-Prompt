# 🛸 Missão ORION — Mission Control AI

> Sistema inteligente de análise de telemetria espacial com IA real via Llama 3.3 70B  
> **Disciplina:** Prompt & Artificial Intelligence — FIAP 1CCPY  
> **Global Solution 2026.1**

---

## 👥 Grupo 05

| Nome | RM |
|---|---|
| Arthur dos Santos Bezerra | 569721 |
| Carlos Henrique Fratezi | 571792 |
| Felipe Gouveia Braga | 568956 |

---

## 📋 Descrição

O **Mission Control AI** é um sistema Python que simula dados operacionais de uma cápsula espacial e os envia para um modelo de linguagem real (Llama 3.3 70B via Groq API) para análise inteligente em tempo real.

O sistema demonstra na prática os conceitos de **prompt engineering**, **controle de parâmetros do modelo** e **instruções de raciocínio estruturado para IA** — o modelo não tem respostas pré-prontas, ele raciocina sobre os dados recebidos a cada execução.

---

## 🚀 Funcionalidades

- **Simulador de telemetria** com 4 cenários operacionais distintos
- **Análise completa de status** — classifica a missão em NOMINAL / ATENÇÃO / CRÍTICO / EMERGÊNCIA
- **Previsão de falhas** — identifica sistemas em risco e estima impacto
- **Plano de ação** — recomendações priorizadas em P1, P2 e P3 para o Mission Control
- **Conversa livre** — o operador pode fazer qualquer pergunta em linguagem natural com histórico de contexto (multi-turn)

---

## 🛰️ Cenários Simulados

| Cenário | Descrição |
|---|---|
| `normal` | Todos os sistemas dentro dos parâmetros nominais |
| `critico` | Múltiplos sistemas em estado de alerta simultâneo |
| `falha_energia` | Painéis solares com geração crítica, bateria caindo |
| `falha_comunicacao` | Perda severa de sinal e latência extrema com a Terra |

---

## 🧠 Prompt Engineering — Decisões Técnicas

### System Prompt
O `SYSTEM_PROMPT` define a persona **ORION-AI**, os parâmetros de referência numéricos de cada sensor e o formato estruturado obrigatório da resposta (Status → Análise → Riscos → Recomendações → Observações).

### Controle de Parâmetros por Tipo de Análise

| Função | `temperature` | `top_p` | Motivo |
|---|---|---|---|
| Análise de status | `0.4` | `0.90` | Equilíbrio entre precisão técnica e variação |
| Previsão de falhas | `0.2` | `0.85` | Mais conservador — análise de risco exige consistência |
| Plano de ação | `0.3` | `0.90` | Base técnica com abertura para soluções criativas |
| Conversa livre | `0.5` | `0.95` | Mais natural para interação com o operador |

---

## 📁 Estrutura do Projeto

```
missao-orion-prompt-ia/
├── missao_orion_prompt_ia.py   # sistema principal
└── README.md
```

---

## ⚙️ Como Executar

### 1. Instale a dependência

```bash
pip install groq
```

### 2. Configure sua chave de API

Crie uma conta gratuita em [console.groq.com](https://console.groq.com) e gere uma API Key.  
No arquivo `missao_orion_prompt_ia.py`, substitua na linha de configuração:

```python
GROQ_API_KEY = "sua_chave_aqui"
```

### 3. Execute

```bash
python missao_orion_prompt_ia.py
```

---

## 🖥️ Exemplo de Uso

```
=================================================================
   MISSAO ORION — Mission Control AI
   Sistema de Analise Inteligente — Prompt & AI
   FIAP 1CCPY — Global Solution 2026.1
=================================================================

[SIMULADOR DE TELEMETRIA] Selecione o cenario da missao:
  1. Operacao Normal
  2. Situacao Critica (multiplos alertas)
  3. Falha no Sistema de Energia Solar
  4. Falha no Sistema de Comunicacao
  5. Cenario Aleatorio

[MENU DE ANALISE] O que deseja analisar?
  1. Analise Completa de Status da Missao
  2. Previsao de Falhas
  3. Recomendacoes de Acao para Mission Control
  4. Perguntar livremente ao ORION-AI
  5. Gerar novos dados (mesmo cenario)
  6. Trocar cenario
  0. Sair
```

---

## 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **Groq API** — inferência de alta velocidade
- **Llama 3.3 70B Versatile** — modelo de linguagem principal
- **Biblioteca `groq`** — cliente oficial Python

---

## 📎 Links

- 🎬 **Vídeo Pitch:** _em breve_
- 🏫 **Instituição:** [FIAP](https://www.fiap.com.br)
