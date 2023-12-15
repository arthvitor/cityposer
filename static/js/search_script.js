// Adicionando informações no HTML de maneira dinâmica
function resultSearch(artistData) {
    for (let i = 0; i < artistData.length; i++) {
        // Cada um dos elementos do dicionário
        let dicionario = artistData[i]

        // Selecionando elemento que vai conter o menu
        let populate_div = document.querySelector('.populate-result-search');

        // Criando uma div onde será armazenado esses elementos
        let div_result_choice = document.createElement('div');
        div_result_choice.classList.add('div-result-choice');
        div_result_choice.setAttribute('data-id', dicionario.id);

        // Criando imagem
        let img_div_choice = document.createElement('img');
        img_div_choice.classList.add('img-div-choice');
        img_div_choice.src = dicionario.img

        // Criando texto
        let p_div_choice = document.createElement('p');
        p_div_choice.classList.add('p-div-choice');
        p_div_choice.textContent = dicionario.name;

        // Adicionando os elementos as suas divs
        div_result_choice.append(img_div_choice);
        div_result_choice.append(p_div_choice);

        // Adicionando divs a div principal
        populate_div.append(div_result_choice)

        // Adicionando evento em cima das divs para receber os ids no backend
        div_result_choice.addEventListener('click', function() {
            let id_artist = div_result_choice.getAttribute('data-id');
            sendDatatoBackend(id_artist);
        });
    }
};

// // Mandando dados para o backend via AJAX
// function sendDatatoBackend(id_artist) {
//     // Realizando requisição para o AJAX
//     fetch('/search', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ 'id_artist': id_artist })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.sucess) {
//             console.log('Requisição enviada com Sucesso', data);
//             // Redirecionar o usuário para a página desejada
//             window.location.href = '/quiz';
//         } else {
//             console.log('Erro na requisição');
//         }
//     })
//     .catch(error => {
//         console.log('Erro na requisição', error);
//     });
// }

document.addEventListener("DOMContentLoaded", function () {
    // Inicialize o NProgress
    NProgress.configure({ showSpinner: false });

    // Adicione o evento de click ao elemento desejado
    var searchButtons = document.querySelectorAll('.div-result-choice');
    searchButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var id_artist = button.getAttribute('data-id');
            sendDatatoBackend(id_artist);
        });
    });

    // Função para enviar dados para o backend via AJAX
    function sendDatatoBackend(id_artist) {
        // Iniciar o NProgress antes da requisição
        NProgress.start();

        // Realizar a requisição
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'id_artist': id_artist })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Requisição enviada com Sucesso', data);

            // Terminar o NProgress após a conclusão da requisição
            NProgress.done();

            // Redirecionar o usuário para a página desejada
            window.location.href = '/quiz';
        })
        .catch(error => {
            console.log('Erro na requisição', error);

            // Terminar o NProgress em caso de erro
            NProgress.done();
        });
    }
});

// Rodando as funções
resultSearch(artistDataJson);