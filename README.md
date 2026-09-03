# Semana 7 — Autenticação e Autorização

Evolução da Book API da semana 6 (FastAPI + SQLAlchemy + Pydantic), adicionando
cadastro/login de usuários, JWT e controle de acesso por papel (`user` / `admin`).

## O que foi adicionado

| Arquivo | O que faz |
|---|---|
| `security.py` | Hash de senha com `bcrypt` e criação/validação de JWT |
| `dependencies.py` | `get_current_user` (exige token válido) e `require_admin` (exige role admin) |
| `models.py` | Novo modelo `User` (name, email único, hashed_password, role) |
| `schemas.py` | `UserCreate`, `UserLogin`, `UserOut` (sem senha!), `Token` |
| `crud.py` | Funções de acesso a dados para `User` |
| `main.py` | Rotas `/auth/register`, `/auth/login`, `/users/me`, `/users`, `/users/{id}` + proteção nas rotas de `books`/`authors` |
| `exemplo_01_hash_senha.py` | Script isolado do exercício 1 (hash/verify), sem FastAPI/DB |

`database.py` não mudou.

## Como rodar

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Abra `http://127.0.0.1:8000/docs`. No Swagger, use o botão "Authorize" com o
token retornado por `/auth/login` (formato `Bearer <token>`) para testar as
rotas protegidas.

## Quem pode fazer o quê

| Rota | Sem token | USER | ADMIN |
|---|---|---|---|
| `GET /books`, `/authors` | ✅ | ✅ | ✅ |
| `POST`/`PUT` books, authors | 401 | ✅ | ✅ |
| `DELETE` books, authors | 401 | 403 | ✅ |
| `GET /users/me` | 401 | ✅ | ✅ |
| `GET /users` | 401 | ✅ | ✅ |
| `DELETE /users/{id}` | 401 | 403 | ✅ |

Fui um pouco além do que os exercícios pediam ao proteger também
`books`/`authors` com os dois níveis de acesso (não só `/users`), pra deixar
o `role` realmente significando alguma coisa em mais de uma rota — se quiser
apresentar só o escopo exato pedido (users), é só remover os `Depends` de
`get_current_user`/`require_admin` das rotas de books/authors.

## Desafio extra — 3 problemas de segurança encontrados

1. **JWT sem expiração longa demais / segredo fraco em produção**
   `SECRET_KEY` tem um valor padrão hardcoded (`dev-only-secret-change-me`) e
   o token expira em 30 min, mas se alguém rodasse isso em produção sem
   definir a variável de ambiente `SECRET_KEY`, qualquer pessoa poderia forjar
   tokens válidos. Correção: exigir `SECRET_KEY` via variável de ambiente
   (falhar ao subir a aplicação se ela não existir) e nunca commitar segredos
   no repositório.

2. **Sem confirmação de senha / política de senha fraca no registro**
   `POST /auth/register` aceita qualquer string como senha (inclusive `"1"`),
   sem exigir tamanho mínimo. Correção: validar tamanho mínimo (ex: 8
   caracteres) no `UserCreate` com um `field_validator` do Pydantic, e
   idealmente checar contra listas de senhas vazadas.

3. **Sem rate limiting no `/auth/login`**
   Como está, nada impede um ataque de força bruta contra o endpoint de
   login (tentar milhares de senhas por segundo). Correção: adicionar rate
   limiting por IP/email (ex: `slowapi`) e/ou bloqueio temporário após N
   tentativas incorretas.

Perguntas do enunciado, respondidas rapidamente:

- **Se o JWT nunca expirasse?** um token roubado/vazado ficaria válido para
  sempre — não existiria forma de "deslogar" o usuário sem trocar o
  `SECRET_KEY` (o que invalidaria todos os tokens de todo mundo).
- **Se `/users/me` retornasse a senha?** mesmo com hash, exporia o hash para
  qualquer pessoa autenticada tentar quebrar offline; por isso `UserOut` não
  tem esse campo.
- **Se um USER conseguisse chamar `DELETE /users/:id`?** qualquer usuário
  comum poderia apagar a conta de qualquer outra pessoa, inclusive admins —
  por isso essa rota depende de `require_admin`.
