# TODO
## MVP
- [X] Permitir o agendamento de publicações.
- [X] Definir a relação do cliente com o plano x Vertical
- [X] Documentação da API: Implementação com Swagger.
- [X] Usar Postgres (adicionar no compose e mudar a configuração do projeto)
- [X] ~~Adicionar plano ao model de usuário~~ Subscription
- [ ] Remover imagens temporárias criadas pelo teste
- [X] Autenticação baseada em JWT
- [ ] Filas
- [X] Github action para testes
- [ ] Testar usando Postgresql
- [X] Servir arquivos pela aplicação por enquanto
- [X] Ler configurações do ambiente (environment)
- [ ] Noticias em rascunho não devem ser disponíveis para leitura
- [ ] Endpoint para noticias precisa ter permissões. Editor pode criar, editar e excluir suas próprias notícias. Leitor só vê as noticias de acordo com seu plano.
- [X] Endpoint para administrar usuários
- [X] Limitar aos admins o Endpoint para administrar usuários
- [ ] Nested update para Subscription?

## Se tiver tempo
- [X] Descrever campos nos models para sair no schema da API?
- [ ] Enviar email ao autor de uma notícia que ela foi publicada com sucesso
- [ ] Testar usando Postgresql
- [ ] Considerar se há algum código que se beneficie de tipagem
- [ ] Caching com Redis
- [ ] Pre commit hook ou pelo menos um script pra rodar antes de fazer um commit (que reformate o código com o black ou autopep8?)
- [ ] Remover imagens temporárias criadas pelo teste
- [ ] Talvez não retornar 404 para leitors Jota Info tentando acessar notícias não disponiveis nesse plano ou nas verticais do plano dele
- [ ] Tornar assinaturas mais dinâmicas. Com data de criação, termino e permitir que haja mais de uma mas apenas uma ativa de cada vez