console.log("Space Energy Monitor iniciado");

// Função para gerar números aleatórios entre um valor mínimo e máximo
function gerarNumeroAleatorio(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function definirModoMissao(geracaoSolar, consumoTotal, bateria) {
    if (bateria < 20) {
        return "Modo Emergência";
    }

    if (bateria < 40) {
        return "Modo Economia";
    }

    if (geracaoSolar < consumoTotal) {
        return "Modo Atenção";
    }

    return "Operação Normal";
}

function definirStatusModulo(temperatura, energia, comunicacao) {
    if (temperatura > 80 || energia < 20 || comunicacao < 50) {
        return "Crítico";
    }

    if (temperatura > 65 || energia < 40 || comunicacao < 70) {
        return "Atenção";
    }

    return "Normal";
}

function gerarAlertas(geracaoSolar, consumoTotal, bateria, modulos) {
    let alertas = [];

    if (geracaoSolar < consumoTotal) {
        alertas.push("Energia solar abaixo do consumo total da missão.");
    }

    if (bateria < 25) {
        alertas.push("Bateria em nível crítico. Risco de perda energética nos módulos.");
    }

    modulos.forEach(function(modulo) {
        if (modulo.temperatura > 80) {
            alertas.push("Temperatura crítica no módulo " + modulo.nome + ".");
        }

        if (modulo.energia < 20) {
            alertas.push("Baixa disponibilidade de energia no módulo " + modulo.nome + ".");
        }

        if (modulo.comunicacao < 50) {
            alertas.push("Comunicação instável no módulo " + modulo.nome + ".");
        }
    });

    if (alertas.length === 0) {
        alertas.push("Nenhum alerta crítico identificado. Missão operando dentro dos parâmetros.");
    }
    
    return alertas;
}

function gerarDecisoes(geracaoSolar, consumoTotal, bateria, modulos) {
    let decisoes = [];

    if (bateria < 25) {
        decisoes.push("Ativar modo economia de energia para preservar os sistemas essenciais.");
    }

    if (geracaoSolar < consumoTotal) {
        decisoes.push("Priorizar energia para suporte à vida, comunicação e controle térmico.");
        decisoes.push("Redirecionar energia solar disponível para recarga das baterias.");
    }

    modulos.forEach(function(modulo){
        if (modulo.temperatura > 80) {
            decisoes.push("Acionar resfriamento emergencial no módulo " + modulo.nome + ".");
        }

        if (modulo.comunicacao < 50) {
            decisoes.push("Tentar reconexão automática do módulo " + modulo.nome + " com a base terrestre.");
        }

        if (modulo.energia < 20) {
            decisoes.push("Reduzir consumo operacional do módulo " + modulo.nome + ".");
        }
    });

    if (decisoes.length === 0) {
        decisoes.push("Manter operação normal e continuar monitoramento preventivo.");
    }

    return decisoes;
}

function calcularSustentabilidade(geracaoSolar, consumoTotal, bateria, modulos) {
    let pontos = 0;

    if (geracaoSolar >= consumoTotal) {
        pontos += 35;
    } else {
        pontos += Math.round((geracaoSolar / consumoTotal) * 35);
    }

    pontos += Math.round((bateria / 100) * 35);

    let modulosNormais = 0;

    modulos.forEach(function(modulo){
        let status = definirStatusModulo(
            modulo.temperatura,
            modulo.energia,
            modulo.comunicacao
        );

        if (status === "Normal") {
            modulosNormais++;
        }
    });

    pontos += Math.round((modulosNormais / modulos.length) * 30);

    return pontos;
}

function classificarSustentabilidade(indice) {
    if (indice >= 80) {
        return "Operação sustentável";
    }

    if (indice >= 50) {
        return "Operação moderada";
    }

    return "Operação crítica";
}

// Função principal que simula uma nova leitura da missão
function simularNovaLeitura() {
    // Dados simulados da missão
    let geracaoSolar = gerarNumeroAleatorio(8, 28);
    let consumoTotal = gerarNumeroAleatorio(10, 24);
    let bateria = gerarNumeroAleatorio(10, 100);
    let modoMissao = definirModoMissao(geracaoSolar, consumoTotal, bateria);

    let modulos = [
        {
         nome: "Painéis Solares",
         funcao: "Captar energia renovável para alimentar a missão",
         temperatura: gerarNumeroAleatorio(25, 70),
         energia: Math.round((geracaoSolar / 28) * 100),
         comunicacao: gerarNumeroAleatorio(80, 100)
        },

        {
         nome: "Baterias",
         funcao: "Armazenar energia para períodos de baixa geração solar",
         temperatura: gerarNumeroAleatorio(25, 90),
         energia: bateria,
         comunicacao: gerarNumeroAleatorio(75, 100)
        },

        {
         nome: "Comunicação",
         funcao: "Manter contato com a base terrestre",
         temperatura: gerarNumeroAleatorio(25, 75),
         energia: gerarNumeroAleatorio(20, 100),
         comunicacao: gerarNumeroAleatorio(35, 100)
        },

        {
         nome: "Controle Térmico",
         funcao: "Regular a temperatura dos equipamentos",
         temperatura: gerarNumeroAleatorio(25, 95),
         energia: gerarNumeroAleatorio(20, 100),
         comunicacao: gerarNumeroAleatorio(70, 100)
        },

        {
         nome: "Suporte à Vida",
         funcao: "Manter condições mínimas para a tripulação",
         temperatura: gerarNumeroAleatorio(25, 85),
         energia: gerarNumeroAleatorio(20, 100),
         comunicacao: gerarNumeroAleatorio(80, 100)
        }

    ];

    // Exibindo os dados na tela
    document.getElementById("geracaoSolar").textContent = geracaoSolar + " kW";
    document.getElementById("consumoTotal").textContent = consumoTotal + " kW";
    document.getElementById("bateria").textContent = bateria + "%";
    document.getElementById("modoMissao").textContent = modoMissao;

    let areaModulos = document.getElementById("listaModulos");

    areaModulos.innerHTML = "";

    modulos.forEach(function(modulo) {
        let status = definirStatusModulo(modulo.temperatura, modulo.energia, modulo.comunicacao);

        let classeStatus = "";

        if (status === "Normal") {
            classeStatus = "normal";
        } else if (status === "Atenção") {
            classeStatus = "atencao";
        } else {
            classeStatus = "critico";
        }

        areaModulos.innerHTML += `
          <div class="modulo ${classeStatus}">
            <h3>${modulo.nome}</h3>
            <p><strong>Função:</strong> ${modulo.funcao}</p>
            <p><strong>Temperatura:</strong> ${modulo.temperatura}°C</p>
            <p><strong>Disponibilidade energética:</strong> ${modulo.energia}%</p>
            <p><strong>Comunicação:</strong> ${modulo.comunicacao}%</p>
            <p><strong>Status:</strong> ${status} </p>
          </div>
        `;
    });
    
    let alertas = gerarAlertas(geracaoSolar, consumoTotal, bateria, modulos);

    let areaAlertas = document.getElementById("listaAlertas");

    areaAlertas.innerHTML = "";

    alertas.forEach(function(alerta) {
        areaAlertas.innerHTML += `
          <div class="alerta">
            <strong>Alerta:</strong> ${alerta}
          </div>
        `;
    });

    let decisoes = gerarDecisoes(geracaoSolar, consumoTotal, bateria, modulos);

    let areaDecisoes = document.getElementById("listaDecisoes");

    areaDecisoes.innerHTML = "";

    decisoes.forEach(function(decisao) {
        areaDecisoes.innerHTML += `
            <div class="decisao">
                <strong>Decisão:</strong> ${decisao}
            </div>
        `;
    });

    let indiceSustentabilidade = calcularSustentabilidade(geracaoSolar, consumoTotal, bateria, modulos);

    let classificacaoSustentabilidade = classificarSustentabilidade(indiceSustentabilidade);

    let areaSustentabilidade = document.getElementById("areaSustentabilidade");

    areaSustentabilidade.innerHTML = `
        <p><strong>${indiceSustentabilidade}%</strong></p>
        <div class="barra-sustentabilidade">
            <div class="progresso-sustentabilidade" style="width: ${indiceSustentabilidade}%;"></div>
        </div>

        <p><strong>Classificação:</strong> ${classificacaoSustentabilidade}</p>
        <p><strong>Critérios:</strong> geração solar, consumo total, nível da bateria e módulos em operação normal.</p>
    `;
}

// Executa uma simulação automaticamente quando a página abre
simularNovaLeitura();