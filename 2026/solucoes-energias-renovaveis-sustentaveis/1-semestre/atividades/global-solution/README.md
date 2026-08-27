# Space Energy Monitor

Projeto desenvolvido para a Global Solution 2026.1 da disciplina Soluções em Energias Renováveis e Sustentáveis.

## Professor

André Tritiack de Farias

## Integrantes do Grupo

Nome: Bruno Riquelme Coutinho Pereira - RM: 569619

Nome: Eduardo Bigoli Portela - RM: 569897

Nome: Lucas Lino Marques da Silva - RM: 572863

## Sobre o projeto

O Space Energy Monitor é um dashboard web criado para simular o monitoramento energético de uma missão espacial experimental sustentável.

A ideia do projeto é acompanhar dados simulados da missão, como geração de energia solar, consumo total, carga da bateria, temperatura dos módulos, comunicação e status operacional.

Com esses dados, o sistema gera alertas automáticos, sugere decisões básicas e calcula um índice de sustentabilidade da missão.

## Objetivo

Desenvolver uma solução simples e funcional para monitorar os sistemas energéticos de uma missão espacial, aplicando conceitos de:

- energia solar;
- consumo energético;
- bateria;
- temperatura;
- comunicação;
- sustentabilidade;
- tomada de decisão automatizada.

## Funcionalidades

- Simulação de dados da missão.
- Exibição da geração solar em kW.
- Exibição do consumo total em kW.
- Monitoramento da bateria em porcentagem.
- Monitoramento dos módulos da missão.
- Classificação dos módulos em Normal, Atenção ou Crítico.
- Cores diferentes para facilitar a identificação dos status.
- Geração automática de alertas.
- Sugestão de decisões automáticas.
- Cálculo do índice de sustentabilidade.
- Botão para simular uma nova leitura dos dados.

## Módulos monitorados

O sistema simula o monitoramento dos seguintes módulos:

- Painéis Solares;
- Baterias;
- Comunicação;
- Controle Térmico;
- Suporte à Vida.

Cada módulo possui dados de temperatura, disponibilidade energética, comunicação e status.

## Regras utilizadas

O sistema classifica os módulos com base em regras simples:

- Crítico: temperatura acima de 80 °C, disponibilidade energética abaixo de 20% ou comunicação abaixo de 50%.
- Atenção: temperatura acima de 65 °C, disponibilidade energética abaixo de 40% ou comunicação abaixo de 70%.
- Normal: quando os dados estão dentro dos limites definidos.

Essas regras também são usadas para gerar alertas e decisões automáticas.

## Alertas e decisões

Quando o sistema identifica uma situação de risco, ele exibe alertas como:

- energia solar abaixo do consumo total;
- bateria em nível crítico;
- temperatura crítica em algum módulo;
- baixa disponibilidade energética;
- comunicação instável.

Com base nesses alertas, o sistema sugere decisões como:

- ativar modo economia;
- priorizar energia para módulos essenciais;
- redirecionar energia solar para as baterias;
- acionar resfriamento emergencial;
- tentar reconexão com a base terrestre.

## Índice de sustentabilidade

O índice de sustentabilidade é calculado com base em três fatores:

- geração solar em relação ao consumo total;
- nível da bateria;
- quantidade de módulos em operação normal.

A classificação pode ser:

- Operação sustentável;
- Operação moderada;
- Operação crítica.

Esse índice foi criado para resumir de forma simples a condição energética da missão.

## Tecnologias utilizadas

- HTML5;
- CSS3;
- JavaScript.

## Estrutura do projeto

space-energy-monitor/
├── index.html
├── style.css
├── script.js
├── README.md
└── entrega.txt

## Como executar

1. Baixe ou clone este repositório.
2. Abra a pasta do projeto.
3. Execute o arquivo index.html em um navegador.
4. Clique no botão Simular nova leitura para gerar novos dados da missão.

Também é possível executar com a extensão Live Server no Visual Studio Code.

## Observação

Este projeto utiliza dados simulados para representar cenários de uma missão espacial experimental. A proposta foi desenvolvida com foco acadêmico, buscando aplicar conceitos de energia renovável, sustentabilidade e lógica de programação em uma solução simples e funcional.