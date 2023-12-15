let pontuacao = 0;

document.addEventListener('DOMContentLoaded', async function(){
    // Recebendo dados do backend quando eles estiverem prontos
    try {
        // Enquanto os dados estão sendo carregados, mostrar loader na tela
        showLoader();

        // Buscar dados do quiz
        const quizDataResponse = await fetch('/quiz-data');
        const quizData = await quizDataResponse.json();

        // Construir a página do quiz
        buildQuiz(quizData);

        // Ocultando o loader após o carregamento
        hideLoader();
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
    }
});

function showLoader() {
    let loaderElements = document.getElementsByClassName('loader type-animation');

    if (loaderElements.length > 0) {
        loaderElements[0].style.display = 'block';
    } else {
        console.error('Nenhum elemento com a classe "loader type-animation" encontrado.');
    }
}

function hideLoader() {
    let loaderElements = document.getElementsByClassName('loader type-animation');

    if (loaderElements.length > 0) {
        loaderElements[0].style.display = 'none';
    } else {
        console.error('Nenhum elemento com a classe "loader type-animation" encontrado.');
    }
}

function shuffleArray(array, targetSize) {
    if (array && array.length && targetSize > 0) {
        // Preencher o array até atingir o tamanho desejado
        const filledArray = [...array];
        while (filledArray.length < targetSize) {
            filledArray.push(...array);
        }

        // Embaralhar o array usando o algoritmo de Fisher-Yates
        for (let i = filledArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [filledArray[i], filledArray[j]] = [filledArray[j], filledArray[i]];
        }

        // Retornar apenas as primeiras 'targetSize' alternativas
        return filledArray.slice(0, targetSize);
    } else {
        console.error('Array inválido, indefinido ou tamanho alvo inválido.');
    }
}


function generateRandomNumber(n) {
    return Math.random().toFixed(n);
}

function getCategory(value) {
    if (value >= 0.9) {
        return 'Muito alegre';
    } else if (value >= 0.6) {
        return 'Bem alegre';
    } else if (value >= 0.4) {
        return 'Meio alegre';
    } else if (value >= 0.2) {
        return 'Tristinho';
    } else {
        return 'Meme do Sr. Incrível com Depressão';
    }
}

function buildQuiz(quizData) {
    let quizContainer = document.getElementById('quiz-wrapper');
    let resultContainer = document.getElementById('result-container');
    let nextQuestionButton = document.getElementById('next-question-btn');

    let currentQuestionIndex = 0;

    let question_txt = [
        {'question_1': 'O quão alegre seu artista é?'},
        {'question_2': 'Qual album é o mais longo?'},
        {'question_3': 'Qual a música mais alta?'},
        {'question_4': 'Qual é a música mais triste, mas que você ainda dança?'},
        {'question_5': 'Qual é o album menos cantável?'}
    ];

    const questionData = [
        {
            number: 1,
            question: question_txt[0]['question_1'],
            options: (() => {
                const valence = quizData.question_1.map(item => item.valence_avg).reduce((acc, val) => acc + val, 0) / quizData.question_1.length;
                const energy = quizData.question_1.map(item => item.energy_avg).reduce((acc, val) => acc + val, 0) / quizData.question_1.length;
        
                // Gera cinco opções únicas
                const optionsSet = new Set();
                optionsSet.add(getCategory(valence * energy));
        
                while (optionsSet.size < 5) {
                    optionsSet.add(getCategory(generateRandomNumber(2)));
                }
        
                // Converte o conjunto para um array e embaralha
                const options = shuffleArray([...optionsSet], 5);
        
                return options;
            })(),
            correctOption: (() => {
                const valence = quizData.question_1.map(item => item.valence_avg).reduce((acc, val) => acc + val, 0) / quizData.question_1.length;
                const energy = quizData.question_1.map(item => item.energy_avg).reduce((acc, val) => acc + val, 0) / quizData.question_1.length;
                const result = valence * energy;
        
                return getCategory(result);
            })(),
        },        
        {
            number: 2,
            question: question_txt[1]['question_2'],
            options: (() => {
                function getRandomAlbumName(albums) {
                    const randomIndex = Math.floor(Math.random() * albums.length);
                    return albums[randomIndex].name;
                }

                const albums = quizData.question_2;
                const topAlbums = albums.sort((a, b) => b.SUM - a.SUM).slice(0, 5).map(album => album.name);
                const options = [...topAlbums, ...Array(5 - topAlbums.length).fill(null).map(() => getRandomAlbumName(albums))];
                return shuffleArray(options, 5);
            })(),
            correctOption: (() => {
                const topAlbum = quizData.question_2.sort((a, b) => b.SUM - a.SUM)[0];
                return topAlbum.name;
            })(),
        },
        {
            number: 3,
            question: question_txt[2]['question_3'],
            options: (() => {
                function getRandomSongName(songs) {
                    const randomIndex = Math.floor(Math.random() * songs.length);
                    return songs[randomIndex].name;
                }

                const songs = quizData.question_3;
                const loudestSongs = songs.sort((a, b) => a.loudness - b.loudness).slice(0, 5).map(song => song.name);
                const options = loudestSongs.concat(Array(5 - loudestSongs.length).fill(null).map(() => getRandomSongName(songs)));
                return shuffleArray(options, 5);
            })(),
            correctOption: (() => {
                const loudestSong = quizData.question_3.sort((a, b) => a.loudness - b.loudness)[0];
                return loudestSong.name;
            })(),
        },
        {
            number: 4,
            question: question_txt[3]['question_4'],
            options: (() => {
                function getRandomSongName(songs) {
                    const randomIndex = Math.floor(Math.random() * songs.length);
                    return songs[randomIndex].name;
                }
        
                const songs = quizData.question_4;
        
                // Encontrar a música com menor valência e maior dançabilidade
                const idealSong = songs.reduce((acc, song) => {
                    // Comparar a valência (quanto menor, melhor) e dançabilidade (quanto maior, melhor)
                    if (!acc || (song.valence < acc.valence && song.danceability > acc.danceability)) {
                        return song;
                    }
                    return acc;
                }, null);
        
                // Conjunto para garantir a exclusividade das opções
                const optionsSet = new Set();
                
                // Adicionar a música ideal como resposta
                if (idealSong) {
                    optionsSet.add(idealSong.name);
                }
        
                // Adicionar músicas aleatórias até atingir 5 opções únicas
                while (optionsSet.size < 5) {
                    optionsSet.add(getRandomSongName(songs));
                }
        
                // Converter o conjunto para um array e embaralhar
                const options = shuffleArray([...optionsSet], 5);
        
                return options;
            })(),
            correctOption: (() => {
                const idealSong = quizData.question_4.reduce((acc, song) => {
                    if (!acc || (song.valence < acc.valence && song.danceability > acc.danceability)) {
                        return song;
                    }
                    return acc;
                }, null);
        
                return idealSong ? idealSong.name : null;
            })(),
        },
        {
            number: 5,
            question: question_txt[4]['question_5'],
            options: (() => {
                function getRandomSongName(songs) {
                    const randomIndex = Math.floor(Math.random() * songs.length);
                    return songs[randomIndex].name;
                }
        
                const songs = quizData.question_5;
        
                // Encontrar a música com menor valor da multiplicação entre instrumentalness e speechiness
                const idealSong = songs.reduce((acc, song) => {
                    const product = song.instrumentalness * song.speechiness;
        
                    // Comparar o produto (quanto menor, melhor)
                    if (!acc || product < acc.product) {
                        return { product, name: song.name };
                    }
                    return acc;
                }, null);
        
                // Conjunto para garantir a exclusividade das opções
                const optionsSet = new Set();
        
                // Adicionar a música ideal como resposta
                if (idealSong) {
                    optionsSet.add(idealSong.name);
                }
        
                // Adicionar músicas aleatórias até atingir 5 opções únicas
                while (optionsSet.size < 5) {
                    optionsSet.add(getRandomSongName(songs));
                }
        
                // Converter o conjunto para um array e embaralhar
                const options = shuffleArray([...optionsSet], 5);
        
                return options;
            })(),
            correctOption: (() => {
                const idealSong = quizData.question_5.reduce((acc, song) => {
                    const product = song.instrumentalness * song.speechiness;
        
                    // Comparar o produto (quanto menor, melhor)
                    if (!acc || product < acc.product) {
                        return { product, name: song.name };
                    }
                    return acc;
                }, null);
        
                return idealSong ? idealSong.name : null;
            })(),
        }        
        // Adicione outros objetos para as outras perguntas
    ];

    // Embaralhe as opções após criar todas as perguntas
    questionData.forEach(question => {
        question.options = shuffleArray(question.options, 5);
    });

    console.log(questionData);

    function createQuestionElement(questionData) {
        let questionContainer = document.createElement('div');
        questionContainer.className = 'question-container';
    
        // Criar elementos para número e texto da pergunta
        let questionNumber = document.createElement('h1');
        let questionText = document.createElement('p');
    
        // Preencher número e texto da pergunta
        questionNumber.textContent = `Pergunta ${questionData.number}`;
        questionText.textContent = questionData.question;
    
        // Adicionar número e texto ao contêiner da pergunta
        questionContainer.appendChild(questionNumber);
        questionContainer.appendChild(questionText);
    
        // Criar contêiner para opções
        let optionsContainer = document.createElement('div');
        optionsContainer.className = 'options-container';
    
        // Iterar sobre as opções e criar botões
        questionData.options.forEach(function (option) {
            let optionButton = document.createElement('button');
            optionButton.className = 'quiz-option';
            optionButton.textContent = option;
    
            optionButton.addEventListener('click', function () {
                if (!questionData.answered) {
                    let isCorrect = option === questionData.correctOption;
                    showResultMessage(isCorrect);
    
                    // Marcar a pergunta como respondida
                    questionData.answered = true;
    
                    nextQuestionButton.style.display = 'block';
                } else {
                    console.log('Pergunta já respondida.');
                }
            });
    
            optionsContainer.appendChild(optionButton);
        });
    
        // Adicionar contêiner de opções ao contêiner principal da pergunta
        questionContainer.appendChild(optionsContainer);
    
        // Retornar a pergunta completa
        return questionContainer;
    }
    
function showNextQuestion() {
    // Limpar o conteúdo do contêiner de perguntas
    quizContainer.innerHTML = '';

    if (currentQuestionIndex < questionData.length) {
        // Limpar o conteúdo da resultContainer
        resultContainer.innerHTML = '';
        resultContainer.style.display = 'none';

        // Esconder o botão 'Próxima Pergunta'
        nextQuestionButton.style.display = 'none';

        // Criar e adicionar a próxima pergunta ao contêiner do quiz
        let questionElement = createQuestionElement(questionData[currentQuestionIndex]);
        quizContainer.appendChild(questionElement);

        // Adiciona transição de opacidade
        setTimeout(function () {
            questionElement.style.opacity = '1';
        }, 10);
    } else {
        // Todas as perguntas foram respondidas, adicione o slide de pontuação final
        resultContainer.style.display = 'none';
        nextQuestionButton.style.display = 'none';
        showFinalSlide();
    }
}

function showFinalSlide() {
    // Adicione a slide para exibir a pontuação final
    const finalSlide = document.createElement('div');
    finalSlide.className = 'swiper-slide';
    finalSlide.innerHTML = `
    <p class='point_final'>Sua pontuação final: ${pontuacao} pontos</p>
    <p class='backhome'>Obrigado por jogar, espero que tenha gostado. Volte para <a href='/'>home</a> para testar com mais artistas<p>
    `;

    // Adicione o slide diretamente ao swiper, sem usar appendSlide
    swiper.wrapperEl.appendChild(finalSlide);

    // Atualize a navegação do swiper
    swiper.update();

    // Remova temporariamente a transição para evitar interferências
    swiper.wrapperEl.style.transition = 'none';

    // Force uma reflow para garantir que as alterações anteriores sejam aplicadas
    swiper.wrapperEl.offsetHeight;

    // Adicione uma pequena pausa antes de mover para o último slide
    setTimeout(() => {
        swiper.slideTo(swiper.slides.length - 1); // Mova para a última slide

        // Restaure a transição após o movimento para o último slide
        swiper.wrapperEl.style.transition = '';
    }, 50);
}
    
function showResultMessage(isCorrect) {
    // Verificar se é a última pergunta antes de exibir a mensagem e o botão 'Próxima Pergunta'
    const isLastQuestion = currentQuestionIndex === questionData.length - 1;

    // Adicione aqui o código para gerar o gráfico com base na resposta (isCorrect)
    const questionCurrent = questionData[currentQuestionIndex];

    // Exibir mensagem de resultado
    const resultMessage = document.createElement('p');
    resultMessage.textContent = isCorrect ? 'Resposta Correta!' : 'Resposta Incorreta!';
    resultContainer.appendChild(resultMessage);

        // Adicione aqui o código para gerar o gráfico com base na resposta (isCorrect)
        const questionnow = questionData[currentQuestionIndex];

    // Certifique-se de que há dados para a pergunta atual
    if (questionnow && questionnow.number === 2) {
        const questionNumber = questionnow.number;

        // Selecione o elemento onde você deseja renderizar o gráfico
        const graphContainer = document.createElement('div');
        graphContainer.id = 'boxplot-container';
        resultContainer.appendChild(graphContainer);

        // Acesse os dados correspondentes no seu JSON quizData
        const quizDataCurrent = quizData[`question_${questionNumber}`];

        if (quizDataCurrent) {
            const data = quizDataCurrent;

            // Extraia os nomes e somas dos dados para o boxplot
            const names = data.map(item => item.name);
            const sums = data.map(item => item.sum);

            // Use o Plotly para criar um boxplot
            Plotly.newPlot('boxplot-container', [{
                type: 'box',
                x: names,
                y: sums,
                boxpoints: 'all', // Mostra todos os pontos
                jitter: 0.3, // Adiciona jitter para melhor visualização
                pointpos: -1.8, // Posição dos pontos em relação às caixas
                boxmean: 'sd', // Adiciona a média e o desvio padrão
                marker: { color: isCorrect ? 'green' : 'red' }, // Cor do boxplot
            }], {
                title: `Quão grande cada album é`,
                xaxis: { title: 'Músicas' },
                yaxis: { title: 'Soma' },
                legend: { traceorder: 'normal'},
                annotations: [{
                    text: 'Descubra quais albuns são os mais longos',
                    showarrow: false,
                    x: 0.5,
                    y: 1.4,
                    xref: 'paper',
                    yref: 'paper',
                    xanchor: 'center',
                    yanchor: 'bottom'
                }],
                plot_bgcolor: 'lightgrey',
                width: 800,
                height: 550,
                 margin: { b: 100 }
            });
        } else {
            console.error(`Dados para a Questão ${questionNumber} não encontrados em quizData.`);
            }
        } else if (questionnow && questionnow.number === 4) {
            const questionNumber = questionnow.number;
        
            // Selecione o elemento onde você deseja renderizar o gráfico
            const scatterContainer = document.createElement('div');
            scatterContainer.id = 'scatter-container';
            resultContainer.appendChild(scatterContainer);
        
            // Acesse os dados correspondentes no seu JSON quizData
            const quizDataCurrent = quizData[`question_${questionNumber}`];
        
            if (quizDataCurrent) {
                const data = quizDataCurrent;
        
                // Extraia os dados de danceability, valence e nomes
                const danceability = data.map(item => item.danceability);
                const valence = data.map(item => item.valence);
                const names = data.map(item => item.name);
        
                // Use o Plotly para criar um scatterplot
                Plotly.newPlot('scatter-container', [{
                    type: 'scatter',
                    mode: 'markers',
                    x: danceability,
                    y: valence,
                    text: names,
                    marker: { color: isCorrect ? 'green' : 'red' },
                }], {
                    title: `Scatterplot da Questão ${questionNumber}`,
                    xaxis: { title: 'Danceability' },
                    yaxis: { title: 'Valence' },
                    legend: { traceorder: 'normal' },
                    annotations: [{
                        text: 'Conheça as músicas mais tristes, mas dançantes',
                        showarrow: false,
                        x: 0.5,
                        y: 1.1,
                        xref: 'paper',
                        yref: 'paper',
                        xanchor: 'center',
                        yanchor: 'bottom'
                    }],
                    plot_bgcolor: 'lightgrey',
                    width: 800,
                    height: 550,
                    margin: { b: 100 }
                });
            } else {
                console.error(`Dados para a Questão ${questionNumber} não encontrados em quizData.`);
            }
    }

    // Atualizar pontuação exibida
    const scoreElement = document.getElementById('score');
    if (scoreElement) {
        scoreElement.textContent = `Pontuação: ${pontuacao}`;
    }

    if (!isLastQuestion) {
        // Exibir o botão 'Próxima Pergunta'
        nextQuestionButton.style.display = 'block';
        resultContainer.style.display = 'flex';
    } 
}

    swiper = new Swiper('.swiper-container', {
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    nextQuestionButton.addEventListener('click', function () {
        currentQuestionIndex++;
        showNextQuestion();
    });

    showNextQuestion();
}
