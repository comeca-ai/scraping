# DashboardGenie

Este projeto utiliza um sistema multi-agente de IA para criar automaticamente dashboards temáticos.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    Crie um arquivo chamado `.env` na raiz do projeto e adicione suas chaves de API:

    ```
    OPENAI_API_KEY=sua_chave_de_api_da_openai
    SERPER_API_KEY=sua_chave_de_api_do_serper
    ```

## Execução

Para iniciar o processo de criação do dashboard, execute o seguinte comando:

```bash
python main.py
```

O sistema iniciará o fluxo de trabalho e você poderá acompanhar o progresso de cada agente no console. Ao final, o resultado será um arquivo HTML com o dashboard completo.
