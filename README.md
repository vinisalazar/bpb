# Boas Práticas bot

Esse é o código fonte para o bot de boas práticas do grupo Código Bonito.

## Desenvolvendo localmente

Caso deseje rodá-lo localmente, você precisará da chave da API do bot, solicite-a no grupo antes de tudo.

### Instalação

Instale as dependências usando [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html):

```sh
conda env create -f environment.yml
conda activate bpb
```

Ou usando o [venv](https://docs.python.org/3/library/venv.html) do Python 3:

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Configurando o ambiente e rodando

Defina a chave da API em seu terminal da seguinte forma:

```sh
export TEL_TOKEN="CHAVE_DA_API_AQUI"
```

E então pode iniciar o processo:

```sh
python run.py
```
