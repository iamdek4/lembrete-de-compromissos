Agendador de Compromissos
Este projeto é um agendador de compromissos escrito em Python que permite aos usuários adicionar e gerenciar agendamentos. O aplicativo utiliza uma interface gráfica com o Tkinter e armazena os dados em um arquivo JSON.

Funcionalidades
Adicionar Agendamentos: Os usuários podem inserir a data, hora e descrição de um compromisso. O formato da data deve ser dd/mm/yyyy e a hora deve ser hh:mm.
Notificações: O aplicativo verifica periodicamente se há compromissos pendentes e notifica o usuário quando um compromisso está prestes a ocorrer, emitindo um som e exibindo uma mensagem.
Persistência de Dados: Os agendamentos são salvos em um arquivo agendamentos.json, que é carregado ao iniciar o aplicativo. Isso permite que os dados sejam mantidos entre as sessões.
