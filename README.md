# Compra e Venda de ações
## da busca dos dados até colocar em produção
![acoes-1](https://user-images.githubusercontent.com/55574172/125682188-207308ac-fc3d-4fc5-8f8d-487bc1b1aad4.jpg)


# Buscando os dados

Para buscar os dados podermos ir até o site da B3 Bolsa de Valores do Brasil na parte de Séries Históricas <a> http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/ <a/>
  
  Em seguida podemos passar esses dados pelo notebook(Engenharia de dados) para modela-los e deixá-los prontos para o trabalho com MACD
  
  
  # Criando o MACD e criando um bot no telegram 
  
  No notebook está todo o código com as análises e o bot prontos, faltando apenas trocar a ação caso queira e DEVE-SE colocar o:
my_token = 'aqui vai o token do bot'
chat_id = 'e aqui vai o id do chat que na frente deve-se colocar o sinal de menos "-"'
  
E caso queira receber testar se tudo está funcionando basta ir até o ultimo campo jo jupyter notebook e tirar a parte do if:
if ontem != hoje:
    envia_mensagem(msg, chat_id, my_token)


e no macd_bot.py está a o código para automatizar o bot, basta apenas encontrar algum serviço que rode o seu código e adicioná-lo.

#STREAMLIT E ARQUIVO PRONTO
coloquei o projeto no Streamlit para que dê para analisar todas as ações de maneira fácil e rápida. Basta colocar o arquivo que foi feito na parte de engenharia de dados e caso não queira fazer essa parte, disponibilizei o arquivo no seguinte link: <a>https://1drv.ms/u/s!Aspr3ED-ZkUEaTNKojOQevr3kvI?e=YRDbKm <a/>

para acessar o projeto online basta seguir este link: <a> https://share.streamlit.io/bertuci/compra_e_venda_acoes/main/str <a/>
