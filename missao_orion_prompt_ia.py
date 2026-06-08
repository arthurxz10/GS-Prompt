"""
=============================================================
  MISSAO ORION — Sistema de Analise Inteligente via IA
  Disciplina: Prompt & Artificial Intelligence
  Curso: Analise e Desenvolvimento de Sistemas — FIAP 1CCPY
  Global Solution 2026.1
=============================================================
  Grupo 05:
    Arthur dos Santos Bezerra  — RM 569721
    Carlos Henrique Fratezi    — RM 571792
    Felipe Gouveia Braga       — RM 568956
=============================================================

DESCRICAO:
  Sistema que simula dados operacionais de uma capsula espacial
  (Missao ORION) e os envia para um modelo de linguagem real
  (Llama 3.3 via Groq API) que analisa o status, detecta riscos,
  prevê falhas e gera recomendacoes automaticas de acao.

DEPENDENCIAS:
  pip install groq
"""

import random
import time
import os
from groq import Groq

# CONFIGURACAO DA API
GROQ_API_KEY = "professor utilize sua API"

# Parametros do modelo — controlam o comportamento da IA
MODELO = "llama-3.3-70b-versatile"   # modelo Llama 3.3 70B via Groq
TEMPERATURA = 0.4      # 0.0 = mais deterministico / 1.0 = mais criativo
                       # 0.4 e ideal para analises tecnicas com alguma variacao
MAX_TOKENS = 900       # limite de tokens na resposta
TOP_P = 0.9            # nucleus sampling — filtra tokens de baixa probabilidade


# SIMULADOR DE DADOS DA MISSAO ORION

def gerar_dados_missao(cenario="normal"):
    """
    Gera dados simulados dos sensores da capsula ORION.
    Cada cenario representa uma situacao operacional diferente.

    Cenarios disponiveis:
      - normal:    operacao dentro dos parametros esperados
      - critico:   multiplos sistemas em estado de alerta
      - falha_energia: problemas no sistema de energia solar
      - falha_comunicacao: perda parcial de sinal com a Terra
    """

    if cenario == "normal":
        dados = {
            "ciclo_missao": random.randint(1, 300),
            "temperatura_interna_C": round(random.uniform(19.0, 23.5), 1),
            "temperatura_externa_C": round(random.uniform(-270.0, -240.0), 1),
            "pressao_cabine_kPa": round(random.uniform(99.5, 101.5), 2),
            "nivel_oxigenio_pct": round(random.uniform(20.5, 21.5), 2),
            "energia_solar_W": round(random.uniform(4800, 5200), 1),
            "bateria_reserva_pct": round(random.uniform(78, 98), 1),
            "consumo_energia_W": round(random.uniform(2800, 3200), 1),
            "sinal_comunicacao_dBm": round(random.uniform(-85, -70), 1),
            "latencia_comunicacao_ms": round(random.uniform(800, 1200), 0),
            "vibracao_estrutural_g": round(random.uniform(0.001, 0.010), 4),
            "radiacao_Gy_h": round(random.uniform(0.0001, 0.0008), 5),
            "velocidade_orbital_km_s": round(random.uniform(7.6, 7.8), 3),
            "altitude_km": round(random.uniform(398, 402), 1),
        }

    elif cenario == "critico":
        dados = {
            "ciclo_missao": random.randint(200, 400),
            "temperatura_interna_C": round(random.uniform(27.0, 31.0), 1),
            "temperatura_externa_C": round(random.uniform(-270.0, -240.0), 1),
            "pressao_cabine_kPa": round(random.uniform(96.0, 98.5), 2),
            "nivel_oxigenio_pct": round(random.uniform(18.0, 19.5), 2),
            "energia_solar_W": round(random.uniform(2200, 3000), 1),
            "bateria_reserva_pct": round(random.uniform(18, 35), 1),
            "consumo_energia_W": round(random.uniform(4200, 4800), 1),
            "sinal_comunicacao_dBm": round(random.uniform(-110, -95), 1),
            "latencia_comunicacao_ms": round(random.uniform(3500, 5000), 0),
            "vibracao_estrutural_g": round(random.uniform(0.045, 0.090), 4),
            "radiacao_Gy_h": round(random.uniform(0.0020, 0.0050), 5),
            "velocidade_orbital_km_s": round(random.uniform(7.4, 7.6), 3),
            "altitude_km": round(random.uniform(380, 392), 1),
        }

    elif cenario == "falha_energia":
        dados = {
            "ciclo_missao": random.randint(50, 200),
            "temperatura_interna_C": round(random.uniform(21.0, 24.0), 1),
            "temperatura_externa_C": round(random.uniform(-270.0, -240.0), 1),
            "pressao_cabine_kPa": round(random.uniform(100.0, 101.0), 2),
            "nivel_oxigenio_pct": round(random.uniform(20.8, 21.2), 2),
            "energia_solar_W": round(random.uniform(800, 1500), 1),   # FALHA
            "bateria_reserva_pct": round(random.uniform(28, 45), 1),   # CAINDO
            "consumo_energia_W": round(random.uniform(3000, 3500), 1),
            "sinal_comunicacao_dBm": round(random.uniform(-88, -75), 1),
            "latencia_comunicacao_ms": round(random.uniform(900, 1400), 0),
            "vibracao_estrutural_g": round(random.uniform(0.002, 0.012), 4),
            "radiacao_Gy_h": round(random.uniform(0.0002, 0.0010), 5),
            "velocidade_orbital_km_s": round(random.uniform(7.6, 7.8), 3),
            "altitude_km": round(random.uniform(398, 402), 1),
        }

    elif cenario == "falha_comunicacao":
        dados = {
            "ciclo_missao": random.randint(100, 350),
            "temperatura_interna_C": round(random.uniform(20.5, 23.0), 1),
            "temperatura_externa_C": round(random.uniform(-270.0, -240.0), 1),
            "pressao_cabine_kPa": round(random.uniform(100.0, 101.2), 2),
            "nivel_oxigenio_pct": round(random.uniform(20.6, 21.3), 2),
            "energia_solar_W": round(random.uniform(4700, 5100), 1),
            "bateria_reserva_pct": round(random.uniform(80, 95), 1),
            "consumo_energia_W": round(random.uniform(2900, 3100), 1),
            "sinal_comunicacao_dBm": round(random.uniform(-125, -112), 1),  # FALHA
            "latencia_comunicacao_ms": round(random.uniform(8000, 15000), 0),  # FALHA
            "vibracao_estrutural_g": round(random.uniform(0.001, 0.008), 4),
            "radiacao_Gy_h": round(random.uniform(0.0001, 0.0006), 5),
            "velocidade_orbital_km_s": round(random.uniform(7.6, 7.8), 3),
            "altitude_km": round(random.uniform(398, 402), 1),
        }

    else:
        # cenario aleatorio misturando valores para teste
        dados = gerar_dados_missao("normal")

    return dados


def formatar_dados_para_prompt(dados):
    """
    Converte o dicionario de dados em texto estruturado
    para ser inserido no prompt enviado ao modelo.
    """
    texto = f"""
=== TELEMETRIA MISSAO ORION — CICLO {dados['ciclo_missao']} ===

[AMBIENTE E ESTRUTURA]
  Temperatura interna da cabine : {dados['temperatura_interna_C']} °C
  Temperatura externa (espaco)  : {dados['temperatura_externa_C']} °C
  Pressao da cabine             : {dados['pressao_cabine_kPa']} kPa
  Nivel de oxigenio             : {dados['nivel_oxigenio_pct']} %
  Vibracao estrutural           : {dados['vibracao_estrutural_g']} g
  Radiacao ionizante            : {dados['radiacao_Gy_h']} Gy/h

[ENERGIA]
  Geracao solar atual           : {dados['energia_solar_W']} W
  Bateria de reserva            : {dados['bateria_reserva_pct']} %
  Consumo total dos sistemas    : {dados['consumo_energia_W']} W
  Balanco energetico            : {round(dados['energia_solar_W'] - dados['consumo_energia_W'], 1)} W

[COMUNICACAO]
  Forca do sinal com a Terra    : {dados['sinal_comunicacao_dBm']} dBm
  Latencia de comunicacao       : {dados['latencia_comunicacao_ms']} ms

[ORBITAL]
  Altitude atual                : {dados['altitude_km']} km
  Velocidade orbital            : {dados['velocidade_orbital_km_s']} km/s

=== FIM DA TELEMETRIA ===
""".strip()
    return texto


# SISTEMA PROMPT — instrucoes fixas que definem o comportamento da IA

SYSTEM_PROMPT = """Voce e o ORION-AI, o sistema de inteligencia artificial de bordo da capsula espacial Missao ORION.

Seu papel e analisar dados de telemetria em tempo real e apoiar a equipe de Mission Control com analises precisas e objetivas.

SUAS RESPONSABILIDADES:
1. Interpretar os dados de sensores recebidos e identificar anomalias
2. Classificar o status geral da missao (NOMINAL / ATENCAO / CRITICO / EMERGENCIA)
3. Prever possiveis falhas com base nos padroes dos dados
4. Recomendar acoes corretivas priorizadas por urgencia

PARAMETROS DE REFERENCIA (valores nominais):
- Temperatura interna: 18°C a 26°C (ideal: 20-24°C)
- Pressao cabine: 99 a 103 kPa
- Oxigenio: 19.5% a 23% (critico abaixo de 19%)
- Energia solar: acima de 4000 W (alerta abaixo de 2500 W)
- Bateria reserva: acima de 40% (critico abaixo de 20%)
- Sinal comunicacao: acima de -100 dBm (perda total abaixo de -120 dBm)
- Latencia comunicacao: abaixo de 2000 ms (critico acima de 5000 ms)
- Vibracao estrutural: abaixo de 0.03 g (alerta acima de 0.05 g)
- Altitude orbital: 395 a 410 km

FORMATO DA SUA RESPOSTA — sempre siga esta estrutura:

STATUS GERAL: [NOMINAL / ATENCAO / CRITICO / EMERGENCIA]

ANALISE DOS SISTEMAS:
(descreva o que esta normal e o que esta fora dos parametros)

RISCOS E PREVISOES DE FALHA:
(liste os riscos identificados e o que pode acontecer se nao houver intervencao)

RECOMENDACOES DE ACAO (por prioridade):
1. [acao mais urgente]
2. [segunda acao]
3. ...

OBSERVACOES ADICIONAIS:
(qualquer informacao relevante para o Mission Control)

Seja tecnico, direto e objetivo. Use linguagem de controle de missao espacial."""


# FUNCOES DE CHAMADA A API GROQ

def analisar_status_geral(dados, cliente_groq):
    """
    Envia os dados de telemetria para o modelo e pede
    uma analise completa do status da missao.
    """
    telemetria = formatar_dados_para_prompt(dados)

    # Prompt do usuario — contexto especifico desta requisicao
    prompt_usuario = f"""Recebi os seguintes dados de telemetria da Missao ORION:

{telemetria}

Por favor, realize uma analise completa do status atual da missao."""

    resposta = cliente_groq.chat.completions.create(
        model=MODELO,
        temperature=TEMPERATURA,    # controla a aleatoriedade da resposta
        max_tokens=MAX_TOKENS,      # limite de tokens gerados
        top_p=TOP_P,                # nucleus sampling
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt_usuario}
        ]
    )

    return resposta.choices[0].message.content


def prever_falhas(dados, cliente_groq):
    """
    Foca especificamente na previsao de falhas futuras
    com base nos dados atuais da telemetria.
    Usa temperatura mais baixa para respostas mais conservadoras/tecnicas.
    """
    telemetria = formatar_dados_para_prompt(dados)

    prompt_usuario = f"""Com base na telemetria abaixo, realize uma analise preditiva focada exclusivamente em PREVISAO DE FALHAS:

{telemetria}

Quais sistemas apresentam maior risco de falha nas proximas horas?
Qual a probabilidade estimada e qual seria o impacto de cada falha prevista?
Responda no formato da sua instrucao padrao."""

    resposta = cliente_groq.chat.completions.create(
        model=MODELO,
        temperature=0.2,        # mais baixo = mais conservador para analise de risco
        max_tokens=MAX_TOKENS,
        top_p=0.85,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt_usuario}
        ]
    )

    return resposta.choices[0].message.content


def gerar_recomendacoes(dados, cliente_groq):
    """
    Gera recomendacoes de acao priorizadas para a equipe
    de Mission Control com base nos dados de telemetria.
    """
    telemetria = formatar_dados_para_prompt(dados)

    prompt_usuario = f"""Com base nos dados de telemetria abaixo, gere um plano de acao detalhado para o Mission Control:

{telemetria}

Foque exclusivamente nas ACOES QUE DEVEM SER TOMADAS AGORA.
Priorize por urgencia (P1 = emergencia, P2 = urgente, P3 = preventivo).
Para cada acao, explique o motivo e o resultado esperado."""

    resposta = cliente_groq.chat.completions.create(
        model=MODELO,
        temperature=0.3,        # moderado — quer criatividade nas solucoes mas base tecnica
        max_tokens=MAX_TOKENS,
        top_p=0.9,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt_usuario}
        ]
    )

    return resposta.choices[0].message.content


def perguntar_livremente(pergunta, dados, historico, cliente_groq):
    """
    Permite que o operador faca perguntas em linguagem natural
    sobre a missao. Mantem historico da conversa para contexto.
    """
    telemetria = formatar_dados_para_prompt(dados)

    # Injeta a telemetria atual no primeiro contexto
    contexto_inicial = f"""Os dados atuais de telemetria da Missao ORION sao:

{telemetria}

Use esses dados como referencia para responder as perguntas do operador."""

    # Constroi o historico de mensagens para manter contexto
    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": contexto_inicial},
        {"role": "assistant", "content": "Dados de telemetria recebidos e processados. Pronto para responder suas perguntas sobre a Missao ORION."}
    ]

    # Adiciona historico anterior da conversa
    for msg in historico:
        mensagens.append(msg)

    # Adiciona a pergunta atual
    mensagens.append({"role": "user", "content": pergunta})

    resposta = cliente_groq.chat.completions.create(
        model=MODELO,
        temperature=0.5,        # um pouco mais alto para conversa mais natural
        max_tokens=MAX_TOKENS,
        top_p=0.95,
        messages=mensagens
    )

    texto_resposta = resposta.choices[0].message.content

    # Atualiza historico para proximas perguntas
    historico.append({"role": "user",      "content": pergunta})
    historico.append({"role": "assistant", "content": texto_resposta})

    return texto_resposta, historico


# INTERFACE DE TEXTO — menu principal

def exibir_cabecalho():
    print("\n" + "=" * 65)
    print("   MISSAO ORION — Mission Control AI")
    print("   Sistema de Analise Inteligente — Prompt & AI")
    print("   FIAP 1CCPY — Global Solution 2026.1")
    print("=" * 65)
    print("   Grupo 05:")
    print("     Arthur dos Santos Bezerra  — RM 569721")
    print("     Carlos Henrique Fratezi    — RM 571792")
    print("     Felipe Gouveia Braga       — RM 568956")
    print("=" * 65)


def selecionar_cenario():
    print("\n[SIMULADOR DE TELEMETRIA] Selecione o cenario da missao:")
    print("  1. Operacao Normal")
    print("  2. Situacao Critica (multiplos alertas)")
    print("  3. Falha no Sistema de Energia Solar")
    print("  4. Falha no Sistema de Comunicacao")
    print("  5. Cenario Aleatorio")

    opcoes = {"1": "normal", "2": "critico", "3": "falha_energia", "4": "falha_comunicacao", "5": "aleatorio"}

    while True:
        escolha = input("\nEscolha [1-5]: ").strip()
        if escolha in opcoes:
            return opcoes[escolha]
        print("  Opcao invalida. Tente novamente.")


def menu_analises(dados, cliente_groq):
    historico_conversa = []

    while True:
        print("\n" + "-" * 65)
        print("[MENU DE ANALISE] O que deseja analisar?")
        print("  1. Analise Completa de Status da Missao")
        print("  2. Previsao de Falhas")
        print("  3. Recomendacoes de Acao para Mission Control")
        print("  4. Perguntar livremente ao ORION-AI")
        print("  5. Gerar novos dados (mesmo cenario)")
        print("  6. Trocar cenario")
        print("  0. Sair")
        print("-" * 65)

        escolha = input("Escolha: ").strip()

        if escolha == "0":
            print("\nEncerrando Mission Control AI. Fim da sessao ORION.")
            break

        elif escolha == "1":
            print("\n[ORION-AI] Processando telemetria... aguarde.\n")
            try:
                resposta = analisar_status_geral(dados, cliente_groq)
                print("=" * 65)
                print("ANALISE DE STATUS — ORION-AI")
                print("=" * 65)
                print(resposta)
            except Exception as e:
                print(f"[ERRO] Falha na comunicacao com o modelo: {e}")

        elif escolha == "2":
            print("\n[ORION-AI] Executando analise preditiva... aguarde.\n")
            try:
                resposta = prever_falhas(dados, cliente_groq)
                print("=" * 65)
                print("PREVISAO DE FALHAS — ORION-AI")
                print("=" * 65)
                print(resposta)
            except Exception as e:
                print(f"[ERRO] Falha na comunicacao com o modelo: {e}")

        elif escolha == "3":
            print("\n[ORION-AI] Gerando plano de acao... aguarde.\n")
            try:
                resposta = gerar_recomendacoes(dados, cliente_groq)
                print("=" * 65)
                print("PLANO DE ACAO — ORION-AI")
                print("=" * 65)
                print(resposta)
            except Exception as e:
                print(f"[ERRO] Falha na comunicacao com o modelo: {e}")

        elif escolha == "4":
            print("\n[MODO LIVRE] Digite sua pergunta para o ORION-AI.")
            print("  (Digite 'voltar' para retornar ao menu)\n")
            historico_conversa = []  # reseta historico ao entrar no modo livre

            while True:
                pergunta = input("Operador > ").strip()
                if pergunta.lower() in ["voltar", "sair", "exit"]:
                    break
                if not pergunta:
                    continue
                print("\n[ORION-AI] Processando...\n")
                try:
                    resposta, historico_conversa = perguntar_livremente(
                        pergunta, dados, historico_conversa, cliente_groq
                    )
                    print("ORION-AI > " + resposta + "\n")
                except Exception as e:
                    print(f"[ERRO] {e}\n")

        elif escolha == "5":
            # Regenera dados com o mesmo cenario
            cenario_atual = dados.get("_cenario", "normal")
            dados = gerar_dados_missao(cenario_atual)
            print("\n[SIMULADOR] Novos dados gerados com sucesso.")
            print(formatar_dados_para_prompt(dados))

        elif escolha == "6":
            return "trocar_cenario"

        else:
            print("  Opcao invalida.")

    return "sair"


# PONTO DE ENTRADA PRINCIPAL

def main():
    exibir_cabecalho()

    # Inicializa cliente Groq
    try:
        cliente = Groq(api_key=GROQ_API_KEY)
        print("\n[SISTEMA] Conexao com Groq API estabelecida.")
        print(f"[SISTEMA] Modelo carregado: {MODELO}")
        print(f"[SISTEMA] Temperatura: {TEMPERATURA} | Max tokens: {MAX_TOKENS} | Top-p: {TOP_P}")
    except Exception as e:
        print(f"\n[ERRO FATAL] Nao foi possivel conectar a API: {e}")
        return

    # Loop principal — permite trocar de cenario sem reiniciar
    while True:
        cenario = selecionar_cenario()
        dados = gerar_dados_missao(cenario)
        dados["_cenario"] = cenario  # guarda referencia do cenario nos dados

        print(f"\n[SIMULADOR] Cenario '{cenario}' carregado. Dados de telemetria gerados:")
        print(formatar_dados_para_prompt(dados))

        resultado = menu_analises(dados, cliente)

        if resultado == "sair":
            break
        # se "trocar_cenario", o loop externo repete a selecao


if __name__ == "__main__":
    main()