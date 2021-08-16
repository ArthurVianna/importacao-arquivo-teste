# User Import API

API REST feita com FastAPI para importação de arquivos para um banco de dados.

## Instalação

Após o download do repositório do projeto, existem duas formas de inicializá-lo. Siga um dos guias a seguir para iniciar o servidor do projeto.

### Container do docker

Para iniciar o projeto por um container do docker, é necessário apenas que o docker-compose esteja instalado em seu ambiente.

Caso não o tenha, siga as instruções na [documentacao do docker](https://docs.docker.com/compose/install/ "Documentacao Docker"), para instalação dos pré-requisitos e do docker-compose.

Com o compose instalado basta rodar
```docker-compose up --build```
no diretório do projeto, para `buildar` e inicializar.

Obs.: O comando acima precisa ser executado apenas uma vez, ou caso haja mudanças no código do projeto. Para executar o projeto sem fazer build de outra imagem do docker rode o mesmo comando sem o argumento ```--build```.

Ao inicializar o projeto pelo docker não é necessário a instalação e configuração de outras dependências do projeto como o banco de dados.

### Localmente

Para executar o projeto localmente é necessário ter uma versão do python 3 instalado. (recomendas-se alguma versão do python 3.9)

*Com o python instalado recomenda-se a criar uma virtualenv para instalação das dependências do projeto. Você pode seguir os passos da própria [documentação do python](https://docs.python.org/pt-br/3/library/venv.html "Documentacao Python") para criar e ativar o seu próprio ambiente virtual*

Com o seu ambiente python configurado, rode o seguinte comando dentro do diretório do projeto para a instalação das dependências.

```sh
pip install -r _requirements.txt
```

Após a execução desse comando podemos configurar a conexão com o banco de dados. O projeto está preparado para ler a variável de ambiente ```DATABASE_URL``` para se conectar com o banco. Caso no seu ambiente não exista uma variável com esse nome pode-se criar um arquivo na raiz do projeto chamado ```.env``` com o seguinte conteúdo:

```
DATABASE_URL="postgresql://[user]:[password]@[endereco]:[port]/[NomeDataBase]"
```

*Substitua o que se encontra entre [ ] de acordo com a configuração do seu banco de dados postgres local*

Obs.: Caso não haja nenhum banco de dados instalado no seu ambiente você pode rodar o projeto sem configurar o endereço da database. Com isso será utilizado o banco de dados sqlite para permanência dos dados.

Com o banco de dados configurado deve-se rodar as migrações do projeto. (Isso irá criar as tabelas necessárias para a execução do projeto no banco de dados)
Basta rodar o seguinte comando para executar as migrações :

```sh
alembic upgrade head
```

Agora o projeto está pronto para a execução, rode o seguinte comando para levantar o servidor do projeto

```sh
uvicorn main:app 
```

Ao rodar esse comando espere até o terminal mostrar uma linha com um link. Esse link e o endereço do projeto, para ver quais os serviços estão disponíveis no projeto basta acessar ```[link]/docs/``` que uma lista com a descrição deles será mostrada.

## Endpoints

O projeto disponibiliza 4 endpoints. Toda a documentação deles pode ser encontrada acessando o servidor do projeto no endpoint ```/docs/```

Um deles é para a importação do arquivo de teste para o projeto e assim importando os dados para o banco.

Obs.: Esse endpoint só irá inserir os dados no banco de dados caso não haja nenhuma linha errada no arquivo enviado. Porém pode-se enviar uma variável na requisição chamada ```force_insert``` com um valor booleano, para que as linhas válidas sejam inseridas mesmo que linhas inválidas sejam encontradas

Os outros três endpoints são para operações com a tabela do projeto ```User```. Estão inclusos dois serviços GET que retornam jsons de um ou vários usuários cadastrados, e um POST para criação de uma nova linha no banco de dados.

## Estrutura relacional

O arquivo disponibilizado para a produção do projeto continha 8 colunas e 49999 linhas de dados que deveriam ser importadas para o banco de dados. As colunas eram:
1. CPF
2. Private
3. Incompleto
4. Data da última compra
5. Compra ticket médio
6. Ticket da última compra
7. Loja mais frequente
8. Loja da última compra

Essas colunas continham em suas linhas os seguintes tipos de dado
1. String até 14 dígitos
2. Boolean (escrito 0 ou 1)
3. Boolean (escrito 0 ou 1)
4. Date escrito em string
5. Valor decimal
6. Valor decimal
7. String até 14 dígitos
8. String até 14 dígitos

Além disso, nas linhas da coluna 4 em diante poderia existir Strings escrito NULL indicando que o dado não existia naquela linha.

Para permanecer esses dados no Projeto foi criado uma tabela chamada ```User```, Onde apenas o CPF era obrigatório ser informado para a sua criação. Os atributos booleanos são opcionais pois está configurado um padrão para preenche-los caso não existam.

A criação das tabelas é feita com migrations criadas automaticamentes pela biblioteca [Alembic](https://alembic.sqlalchemy.org/en/latest/ "Documentacao Alembic"), junto com o [SQLAlchemy](https://www.sqlalchemy.org/ "Documentacao SQLAlchemy"), a partir dos modelos escritos no projeto no módulo ```users```
