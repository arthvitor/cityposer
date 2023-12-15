// Script

// Função para evento de scroll para o header - Home
let header = document.querySelector('header') // Variável do header
let scrollYpos = 0; // Posição da página
let ticking = false; // Ainda não sei kkkk

function header_modify(scrollYpos) {
    if (scrollYpos >= 500) {
        header.style.visibility = 'visible';
        header.classList.add('header-visible')
    }
    else if (scrollYpos <= 500) {
        header.style.visibility = 'hidden';
        header.classList.remove('header-visible');
    } 
} // Mudando a visibilidade do header

window.addEventListener('scroll', (event) => {
    scrollYpos = window.scrollY;
    if (!ticking) {
        window.requestAnimationFrame(() => {
            header_modify(scrollYpos);
            ticking = false;
        });
        ticking = true;    
    }
});

// Evento para caso o usuário mande uma requisição incorreta
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function () {
        let flashErrorIntro = document.querySelector('.flash-messages-error');
        if (flashErrorIntro) {
            flashErrorIntro.classList.add('hidden');
        }
    }, 5000);
})