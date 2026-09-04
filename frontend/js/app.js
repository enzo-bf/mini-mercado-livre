const API_URL = "http://127.0.0.1:8000";

const elementos = {
    statusApi: document.querySelector("#status-api"),
    mensagem: document.querySelector("#mensagem"),

    totalProdutos: document.querySelector("#total-produtos"),
    totalPedidos: document.querySelector("#total-pedidos"),
    totalEstoque: document.querySelector("#total-estoque"),

    formProduto: document.querySelector("#form-produto"),
    produtoId: document.querySelector("#produto-id"),
    nome: document.querySelector("#nome"),
    preco: document.querySelector("#preco"),
    estoque: document.querySelector("#estoque"),
    tituloFormProduto: document.querySelector(
        "#titulo-form-produto"
    ),
    cancelarEdicao: document.querySelector("#cancelar-edicao"),

    formPedido: document.querySelector("#form-pedido"),
    pedidoProduto: document.querySelector("#pedido-produto"),
    quantidade: document.querySelector("#quantidade"),

    listaProdutos: document.querySelector("#lista-produtos"),
    listaPedidos: document.querySelector("#lista-pedidos"),
    atualizarProdutos: document.querySelector(
        "#atualizar-produtos"
    )
};

let produtos = [];
let pedidos = [];

function formatarMoeda(valor) {
    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
}

function escaparHtml(valor) {
    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function exibirMensagem(texto, tipo = "sucesso") {
    elementos.mensagem.textContent = texto;

    elementos.mensagem.className =
        `mensagem mensagem-${tipo}`;

    window.setTimeout(() => {
        elementos.mensagem.classList.add("oculto");
    }, 4000);
}

async function requisicao(
    caminho,
    opcoes = {}
) {
    const resposta = await fetch(
        `${API_URL}${caminho}`,
        {
            headers: {
                "Content-Type": "application/json",
                ...opcoes.headers
            },
            ...opcoes
        }
    );

    if (resposta.status === 204) {
        return null;
    }

    const tipoConteudo = resposta.headers.get("content-type") || "";
    const corpo = tipoConteudo.includes("application/json")
        ? await resposta.json()
        : await resposta.text();

    if (!resposta.ok) {
        let mensagem = typeof corpo === "object"
            ? corpo.detail
            : corpo;

        if (Array.isArray(mensagem)) {
            mensagem = mensagem
                .map(erro => erro.msg)
                .join(", ");
        }

        throw new Error(
            mensagem || "Não foi possível concluir a operação."
        );
    }

    return corpo;
}

async function verificarApi() {
    try {
        await requisicao("/health/");

        elementos.statusApi.textContent = "API online";
        elementos.statusApi.className =
            "status status-online";
    } catch {
        elementos.statusApi.textContent = "API offline";
        elementos.statusApi.className =
            "status status-offline";
    }
}

async function carregarProdutos() {
    try {
        produtos = await requisicao("/produtos/");

        renderizarProdutos();
        preencherSelectProdutos();
        atualizarResumo();
    } catch (erro) {
        exibirMensagem(erro.message, "erro");
    }
}

async function carregarPedidos() {
    try {
        pedidos = await requisicao("/pedidos/");

        renderizarPedidos();
        atualizarResumo();
    } catch (erro) {
        exibirMensagem(erro.message, "erro");
    }
}

function atualizarResumo() {
    elementos.totalProdutos.textContent = produtos.length;
    elementos.totalPedidos.textContent = pedidos.length;

    const totalEstoque = produtos.reduce(
        (total, produto) => total + produto.estoque,
        0
    );

    elementos.totalEstoque.textContent = totalEstoque;
}

function renderizarProdutos() {
    if (produtos.length === 0) {
        elementos.listaProdutos.innerHTML = `
            <div class="estado-vazio">
                Nenhum produto cadastrado.
            </div>
        `;

        return;
    }

    elementos.listaProdutos.innerHTML = produtos
        .map(produto => `
            <article class="produto-card">
                <span class="produto-id">
                    Produto #${produto.id}
                </span>

                <h3>${escaparHtml(produto.nome)}</h3>

                <p class="produto-preco">
                    ${formatarMoeda(produto.preco)}
                </p>

                <p class="produto-estoque">
                    ${produto.estoque} unidade(s) em estoque
                </p>

                <div class="produto-acoes">
                    <button
                        class="botao botao-editar"
                        onclick="editarProduto(${produto.id})"
                    >
                        Editar
                    </button>

                    <button
                        class="botao botao-excluir"
                        onclick="excluirProduto(${produto.id})"
                    >
                        Excluir
                    </button>
                </div>
            </article>
        `)
        .join("");
}

function renderizarPedidos() {
    if (pedidos.length === 0) {
        elementos.listaPedidos.innerHTML = `
            <tr>
                <td colspan="4" class="estado-vazio">
                    Nenhum pedido realizado.
                </td>
            </tr>
        `;

        return;
    }

    elementos.listaPedidos.innerHTML = pedidos
        .map(pedido => {
            const produto = produtos.find(
                item => item.id === pedido.produto_id
            );

            const nomeProduto = produto
                ? produto.nome
                : `Produto #${pedido.produto_id}`;

            return `
                <tr>
                    <td>#${pedido.id}</td>
                    <td>${escaparHtml(nomeProduto)}</td>
                    <td>${pedido.quantidade}</td>
                    <td>
                        ${formatarMoeda(pedido.valor_total)}
                    </td>
                </tr>
            `;
        })
        .join("");
}

function preencherSelectProdutos() {
    const produtosDisponiveis = produtos.filter(
        produto => produto.estoque > 0
    );

    elementos.pedidoProduto.innerHTML = `
        <option value="">
            Selecione um produto
        </option>

        ${produtosDisponiveis
            .map(produto => `
                <option value="${produto.id}">
                    ${escaparHtml(produto.nome)}
                    (${produto.estoque} disponível)
                </option>
            `)
            .join("")}
    `;
}

function limparFormularioProduto() {
    elementos.formProduto.reset();
    elementos.produtoId.value = "";
    elementos.tituloFormProduto.textContent =
        "Cadastrar produto";
    elementos.cancelarEdicao.classList.add("oculto");
}

window.editarProduto = function (produtoId) {
    const produto = produtos.find(
        item => item.id === produtoId
    );

    if (!produto) {
        return;
    }

    elementos.produtoId.value = produto.id;
    elementos.nome.value = produto.nome;
    elementos.preco.value = Number(produto.preco);
    elementos.estoque.value = produto.estoque;

    elementos.tituloFormProduto.textContent =
        `Editar produto #${produto.id}`;

    elementos.cancelarEdicao.classList.remove("oculto");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
};

window.excluirProduto = async function (produtoId) {
    const confirmou = window.confirm(
        "Deseja realmente excluir este produto?"
    );

    if (!confirmou) {
        return;
    }

    try {
        await requisicao(
            `/produtos/${produtoId}`,
            {
                method: "DELETE"
            }
        );

        exibirMensagem("Produto excluído com sucesso.");

        await carregarProdutos();
    } catch (erro) {
        exibirMensagem(erro.message, "erro");
    }
};

elementos.formProduto.addEventListener(
    "submit",
    async evento => {
        evento.preventDefault();

        const produtoId = elementos.produtoId.value;

        const payload = {
            nome: elementos.nome.value.trim(),
            preco: Number(elementos.preco.value),
            estoque: Number(elementos.estoque.value)
        };

        try {
            if (produtoId) {
                await requisicao(
                    `/produtos/${produtoId}`,
                    {
                        method: "PUT",
                        body: JSON.stringify(payload)
                    }
                );

                exibirMensagem(
                    "Produto atualizado com sucesso."
                );
            } else {
                await requisicao(
                    "/produtos/",
                    {
                        method: "POST",
                        body: JSON.stringify(payload)
                    }
                );

                exibirMensagem(
                    "Produto cadastrado com sucesso."
                );
            }

            limparFormularioProduto();
            await carregarProdutos();
        } catch (erro) {
            exibirMensagem(erro.message, "erro");
        }
    }
);

elementos.formPedido.addEventListener(
    "submit",
    async evento => {
        evento.preventDefault();

        const payload = {
            produto_id: Number(
                elementos.pedidoProduto.value
            ),
            quantidade: Number(
                elementos.quantidade.value
            )
        };

        try {
            const pedido = await requisicao(
                "/pedidos/",
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );

            exibirMensagem(
                `Pedido #${pedido.id} criado. Total: ` +
                formatarMoeda(pedido.valor_total)
            );

            elementos.formPedido.reset();
            elementos.quantidade.value = 1;

            await carregarProdutos();
            await carregarPedidos();
        } catch (erro) {
            exibirMensagem(erro.message, "erro");
        }
    }
);

elementos.cancelarEdicao.addEventListener(
    "click",
    limparFormularioProduto
);

elementos.atualizarProdutos.addEventListener(
    "click",
    async () => {
        await carregarProdutos();
        exibirMensagem("Produtos atualizados.");
    }
);

async function iniciarAplicacao() {
    await verificarApi();
    await carregarProdutos();
    await carregarPedidos();
}

iniciarAplicacao();