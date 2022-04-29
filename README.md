<h1 align="center"><strong>Clube do Livro - API</strong></h1>

<br>

<h2 align="center"><strong>Descrição</strong></h2>

Nosso projeto consiste em uma API Rest para uma rede social voltada a compartilhamento de experiências através da leitura. Onde os leitores poderam pesquisar sobre livros obtendo informações como título, autor, gênero, sinopse, entre outras. Bem como visualizar a opinião de outros leitores a respeito do livro pesquisado O leitor também poderá realizar avaliações dos livros lidos de forma textual e/ou nota de 0 a 5.

<br/>
<br/>

Para utilização desta API localmente se faz necessário a criação de um arquivo .env nos moldes do arquivo .env.example.

<br/>
<br/>

<h2 align="center"><strong>Endpoints</strong></h2>

<br/>
<br/>

- ### _Criação de usuário_

  -> POST /api/cadastro - Formato da requisição:

  ```json
  {
    "name": "Teste",
    "email": "teste@teste.com",
    "password": "teste"
  }
  ```

  -> Status code 201 - Formato da resposta:

  ```json
  {
    "id": "c13ade32-6e19-4a0b-8de4-d2a7b3f0f028",
    "name": "Teste",
    "email": "teste@teste.com"
  }
  ```

  -> Possíveis erros

  - Email já cadastrado - Status code 409;

    ```json - response
    {
      "msg": "Email already exists"
    }
    ```

<br/>
<br/>

- ### _Login de usuário_

  -> POST /api/entrar - Formato da requisição:

  ```json
  {
    "email": "teste@teste.com",
    "password": "teste"
  }
  ```

  -> Status code 200 - Formato da resposta:

  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTI2MDQ2OCwianRpIjoiZjhhYmZhZDAtNWI2OC00MDAyLWFhYzEtMzEyNTY1N2QyMTNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJyZWFkZXJfaWQiOiJjMTNhZGUzMi02ZTE5LTRhMGItOGRlNC1kMmE3YjNmMGYwMjgiLCJuYW1lIjoiVGVzdGUiLCJlbWFpbCI6InRlc3RlQHRlc3RlLmNvbSIsImF2YXRhciI6bnVsbH0sIm5iZiI6MTY1MTI2MDQ2OCwiZXhwIjoxNjUxMjYxMzY4fQ.BqbgkhOJ1noODaaOM0QWEzWNfl-qpi7p2J6LMAN_1UU"
  }
  ```

  -> Possíveis erros

  - Usuário não encontrado - Status code 404;

    ```json - response
    {
      "msg": "reader not found"
    }
    ```

<br/>
<br/>

<h3 align="center">Endpoints que necessitam de autenticação</h3>

<br/>

Para este tipo de endpoint é necessário enviar o token de acesso no header da requisição da seguinte maneira:

```js - header
{
  headers: {
    Authorization: `Bearer ${access_token}`;
  }
}
```

-> Possíveis erros ao acessar rotas protegidas sem token

- Status code 401 - Formato da resposta:

  ```json - response
  {
    "msg": "Missing Authorization Header"
  }
  ```

- ### _Informações do usuário logado_

  -> GET /api - Requisição sem corpo:

  -> Status code 200 - Formato da resposta:

  ```json
  {
    "id": "c13ade32-6e19-4a0b-8de4-d2a7b3f0f028",
    "name": "Teste",
    "email": "teste@teste.com"
  }
  ```

<br/>
<br/>

- ### _Update do usuário logado_

  -> PUT /api - Formato da requisição (somente informações que serão atualizadas):

  ```json
  {
    "name": "Teste Um",
    "email": "teste@teste.com",
    "password": "teste"
  }
  ```

  -> Status code 200 - Formato da resposta:

  ```json
  {
    "name": "Teste Um",
    "email": "teste@teste.com"
  }
  ```

<br/>
<br/>

- ### _Deleção do usuário logado_

  -> DELETE /api - Requisição sem corpo:

  -> Status code 200 - Formato da resposta:

  ```json
  {
    "msg": "Reader Teste Um has been deleted"
  }
  ```

<br/>
<br/>
