# CKP01 — Chatbot Profissional • IA de Assistência à Escrita

**Prompt Engineering & AI • FIAP • 2º Semestre 2026**

**Integrantes:** 
- Gabriel de Paula Santos (RM573195) 
- Joao Lucas Silva Lopes (RM573875) 
- Alan Otalvaro (RM571794) 
- Joao Pedro Ribeiro Santos (RM570562) 
- Joao Pedro Evangelista (RM573899) 
- Enzo Ribeiro (RM569429)

**Peso:** 25%  
**Apresentação:** Aula 04  
**Entrega:** 23:55 do dia da Aula 05 (`.zip` via Teams - somente o líder)
---

# Domínio

O domínio escolhido pelo grupo foi **Inteligência Artificial aplicada à assistência de escrita**.

A proposta do projeto é desenvolver um chatbot profissional capaz de auxiliar o usuário em diferentes etapas da produção e desenvolvimento de textos.

O sistema utiliza um modelo de linguagem para compreender a solicitação do usuário, analisar sua intenção e direcioná-la para a tarefa correspondente.

O chatbot possui **três funcionalidades principais**:

1. **Resumo de textos**
2. **Expansão de textos**
3. **Brainstorm para geração de ideias**

A escolha desse domínio foi motivada pela possibilidade de aplicar técnicas de **Prompt Engineering** em diferentes situações relacionadas à escrita, utilizando um único assistente capaz de adaptar seu comportamento de acordo com a necessidade do usuário.

# Público-alvo

O chatbot pode ser utilizado principalmente por:

- Estudantes;
- Profissionais;
- Pessoas desenvolvendo projetos;
- Pessoas que precisam organizar ou reduzir textos;
- Usuários que desejam desenvolver conteúdos;
- Pessoas que procuram novas ideias para trabalhos, projetos ou textos.

# Requisitos atendidos

| Requisito | Status | Implementação |
|-----------|---------|---------------|
| Pipeline LCEL | ✅ | `src/chain.py` - composição de prompt, modelo e parser |
| ChatOllama | ✅ | `ChatOllama` utilizando `gemma4:cloud` via Ollama Cloud |
| Memória gerenciada / Token Buffer Memory | ✅ | `src/memory.py` - memória baseada em limite de 2000 tokens |
| Controle de tokens | ✅ | `tiktoken` utilizado para contabilizar os tokens do histórico |
| Pydantic v2 | ✅ | `AnaliseSchema` em `src/schemas.py`, com 4 campos |
| Contexto da conversa | ✅ | Histórico armazenado pela memória e utilizado nas interações |
| Context Rotation | ✅ | Implementado em `src/context_rot.py`, com teste de retenção de contexto |
| Prompt Engineering | ✅ | Prompts separados para persona, análise, contexto e cada tarefa |
| Resumo | ✅ | Objetivo e regras definidos nos prompts de resumo |
| Expansão | ✅ | Objetivo e regras definidos nos prompts de expansão |
| Brainstorm | ✅ | Objetivo e regras definidos nos prompts de brainstorm |

# Funcionamento do sistema

Antes de executar uma das funcionalidades principais, o chatbot realiza uma **análise da solicitação do usuário**.

Essa etapa identifica informações importantes para determinar como a solicitação deverá ser processada.

## Fluxo principal

```text
Usuário
   ↓
Mensagem
   ↓
Análise da solicitação
   ↓
Identificação do tipo de tarefa
   ↓
Resumo / Expansão / Brainstorm
   ↓
Construção do Prompt
   ↓
Persona + Objetivo + Regras + Contexto + Histórico
   ↓
ChatOllama
   ↓
Output Parser
   ↓
Resposta
   ↓
Atualização da memória
```

# Funcionalidades

## Resumo

A funcionalidade de resumo recebe um conteúdo fornecido pelo usuário e transforma esse conteúdo em uma versão mais curta, clara e organizada.

O chatbot busca preservar as informações e ideias principais, evitando adicionar informações que não estejam presentes no conteúdo original.

Entre os elementos que devem ser preservados estão:

- Ideias principais;
- Conceitos importantes;
- Informações relevantes.

## Expansão

A funcionalidade de expansão recebe uma ideia ou texto fornecido pelo usuário e desenvolve seu conteúdo.

O chatbot pode adicionar:

- Explicações;
- Exemplos;
- Detalhes;
- Contextualização;
- Desenvolvimento dos pontos apresentados.

A expansão deve manter a ideia original do usuário e não alterar seu significado.

## Brainstorm

A funcionalidade de brainstorm tem como objetivo auxiliar o usuário na geração e exploração de ideias.

O chatbot procura:

- Gerar diferentes possibilidades;
- Explorar soluções diferentes para o mesmo problema;
- Combinar ideias;
- Considerar ideias incomuns;
- Fazer perguntas que estimulem a criatividade.

# Análise da solicitação

O projeto utiliza uma etapa específica chamada **análise**, responsável por interpretar a mensagem inicial do usuário antes da geração da resposta.

O `AnaliseSchema`, localizado em `src/schemas.py`, possui quatro campos:

| Campo | Função |
|---------|---------|
| `tipo` | Identifica a tarefa |
| `tema` | Identifica o assunto |
| `palavras_chaves` | Identifica palavras importantes |
| `tipo_descrita` | Identifica características da escrita |

O campo `tipo` identifica uma das três funcionalidades:

```text
resumo
expansao
brainstorm
```

# Prompt Engineering

O projeto utiliza uma estrutura modular de prompts.

```text
assets/
└── prompt/
    ├── main/
    │   ├── persona.md
    │   ├── analise/
    │   ├── brainstorm/
    │   ├── expansao/
    │   └── resumo/
    │
    └── templates/
        └── base.md
```

Essa organização permite separar:

- **Persona**
- **Objetivo**
- **Regras**
- **Contexto**
- **Templates**

# Memória

O chatbot utiliza uma implementação própria de **Token Buffer Memory**, localizada em:

```text
src/memory.py
```

O limite definido no projeto é de:

**2000 tokens**

A cada nova mensagem, o sistema calcula a quantidade de tokens utilizada. Quando o limite é ultrapassado, as mensagens mais antigas são removidas.

## Funcionamento

```text
Nova mensagem
      ↓
Contagem de tokens
      ↓
Mensagem adicionada à memória
      ↓
Cálculo do total
      ↓
Total > 2000 tokens?
      ↓
 ┌───────────────┐
 │               │
Não             Sim
 │               │
 ↓               ↓
Mantém       Remove a mensagem
histórico    mais antiga
 │               │
 └───────┬───────┘
         ↓
Histórico atualizado
```

## Justificativa

A **Token Buffer Memory** foi escolhida porque permite estabelecer um limite direto sobre a quantidade de tokens mantidos no histórico.

Ela permite:

- Controlar o tamanho do contexto;
- Evitar crescimento ilimitado do histórico;
- Manter as interações mais recentes;
- Reduzir informações antigas;
- Controlar a quantidade de tokens processados pelo modelo.

# Context Rotation

O projeto possui uma funcionalidade de **Context Rotation**, implementada em:

```text
src/context_rot.py
```

O teste utiliza **12 idiomas** para avaliar a capacidade do chatbot de manter informações ao longo de várias interações.

Os idiomas utilizados são:

```text
francês
mandarim
coreano
tailandês
holandês
estoniano
húngaro
finlandês
swahili
turco
russo
guarani
```

Ao final do teste, o sistema pergunta:

> Quais idiomas traduzimos até agora?

O resultado permite verificar:

- Quantos idiomas foram lembrados;
- Quais idiomas foram lembrados;
- Quais idiomas foram esquecidos.

### Execução

```bash
python main.py -rot
```

# Pipeline LCEL

O processamento utiliza **LCEL (LangChain Expression Language)**.

A composição principal é:

```text
ChatPromptTemplate
        ↓
ChatOllama
        ↓
Output Parser
```

Para respostas estruturadas:

```text
PydanticOutputParser
```

Para respostas textuais:

```text
StrOutputParser
```

Conceito utilizado:

```text
Prompt | LLM | Parser
```

# ChatOllama

O modelo utilizado é:

```text
gemma4:cloud
```

por meio do:

```text
ChatOllama
```

O modelo é utilizado através do **Ollama Cloud**.

A chave de acesso é configurada através do arquivo `.env`:

```env
OLLAMA_API_KEY=<sua-chave>
```

> O arquivo `.env` não deve ser enviado ao repositório nem incluído no `.zip` da entrega.

# Pydantic

O projeto utiliza **Pydantic** para estruturar a resposta da etapa de análise.

O schema está localizado em:

```text
src/schemas.py
```

O `AnaliseSchema` possui:

```text
tipo
tema
palavras_chaves
tipo_descrita
```

# Interface

A interface atual do chatbot funciona no **terminal**.

Bibliotecas utilizadas:

- **Rich**
- **Prompt Toolkit**

A interface permite que o usuário envie mensagens continuamente e visualize as respostas do chatbot na mesma sessão.

# Estrutura do projeto

```text
2026-ai-checkpoint-4-main/
│
├── assets/
│   └── prompt/
│       ├── context/
│       ├── main/
│       │   ├── analise/
│       │   ├── brainstorm/
│       │   ├── expansao/
│       │   └── resumo/
│       └── templates/
│
├── src/
│   ├── chain.py
│   ├── context_rot.py
│   ├── memory.py
│   ├── process.py
│   ├── schemas.py
│   │
│   └── ui/
│       ├── elements/
│       │   └── screen.py
│       │
│       └── screens/
│           └── history_screen.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

# Principais arquivos

| Arquivo | Responsabilidade |
|----------|------------------|
| `main.py` | Inicialização do chatbot |
| `src/chain.py` | Construção dos pipelines LCEL |
| `src/memory.py` | Implementação da Token Buffer Memory |
| `src/context_rot.py` | Teste de Context Rotation |
| `src/schemas.py` | Definição do `AnaliseSchema` |
| `src/process.py` | Processamento das solicitações |
| `src/ui/` | Componentes da interface |
| `assets/prompt/` | Prompts utilizados pelo chatbot |

# Tecnologias utilizadas

- Python
- LangChain
- LangChain Ollama
- Ollama Cloud
- Gemma 4
- Pydantic
- tiktoken
- Rich
- Prompt Toolkit
- python-dotenv

# Como executar

## 1. Criar o ambiente virtual

```bash
python -m venv .venv
```

## 2. Ativar o ambiente virtual

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar o Ollama Cloud

Crie um arquivo `.env` baseado no `.env.example`:

```env
OLLAMA_API_KEY=<sua-chave>
```

## 5. Executar

```bash
python main.py
```

## Executar o teste de Context Rotation

```bash
python main.py -rot
```

# Limitações atuais

- A interface atualmente funciona pelo terminal;
- O funcionamento depende da configuração do Ollama Cloud;
- A memória possui limite de 2000 tokens;
- Informações antigas podem ser removidas quando o limite é ultrapassado;
- O teste de Context Rotation é executado separadamente através do argumento `-rot`.

# Conclusão

O projeto consiste em uma **IA de assistência à escrita**, desenvolvida para auxiliar usuários em três tarefas principais:

- **Resumo de textos**
- **Expansão de textos**
- **Brainstorm para geração de ideias**

O sistema realiza uma análise inicial da solicitação para identificar a tarefa adequada e utiliza **Prompt Engineering** para adaptar o comportamento do modelo.

A aplicação utiliza uma implementação própria de **Token Buffer Memory**, com limite de **2000 tokens**, para controlar o histórico das conversas.

Além disso, o projeto possui um mecanismo de **Context Rotation** para avaliar a retenção de informações ao longo de múltiplas interações.

Dessa forma, o projeto combina **Prompt Engineering, LangChain, LCEL, ChatOllama, Ollama Cloud, Pydantic, Token Buffer Memory e Context Rotation** para desenvolver um assistente de escrita capaz de auxiliar o usuário em diferentes etapas da criação e desenvolvimento de textos.