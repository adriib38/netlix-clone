
let cards = Array.prototype.slice.call(document.getElementsByClassName('card'));
let modal = document.getElementById('modal-movie-serie');
let closeModal = document.getElementsByClassName('close')[0];

let modalInfo = document.getElementsByClassName('modal-info')[0];
let modalTitle = document.querySelector('.modal-info .title');
let modalDescription = document.querySelector('.modal-info .description');
let modalLink = document.querySelector('.modal-info .link');
let modalCover = document.querySelector('.modal-info .cover');
let modalDuration = document.querySelector('.modal-info .duration');

closeModal.onclick = function() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
}
  

/**
 * Hover in card
 */
cards.forEach((card) => {
  
    let titleAdded = false;
    let imgHTML = card.innerHTML;

    card.addEventListener('mouseenter', async function () {
        if (!titleAdded) {
            //card.style.transform = 'scale(1.2)';
            //card.style.padding = '15px';
            //card.style.background = '#111111';
            card.classList.add('card-expanded');

            let typeCard = card.getAttribute('type');
            const movieJson = await getMovieInfo(typeCard, card.id);

            const infoDiv = document.createElement('div');
            const titleH3 = document.createElement('h3');
            const descP = document.createElement('p');
            const genresP = document.createElement('p');
            const playA = document.createElement('a');

            titleH3.style.margin = '0px';
            titleH3.style.fontSize = '15px';
            titleH3.textContent = movieJson.title;

            descP.textContent = movieJson.description;
            descP.style.fontSize = '10px';

            genresP.textContent = movieJson.genres[0] ?? '';
            playA.setAttribute('href', `/${typeCard}/${ movieJson.uuid }`);
            playA.textContent = 'play';
            playA.style.fontSize = '10px';

            infoDiv.appendChild(titleH3);
            infoDiv.appendChild(descP);
            infoDiv.appendChild(genresP);
            infoDiv.appendChild(playA);

            card.appendChild(infoDiv);
            card.style.height = card.scrollHeight + 'px';

            titleAdded = true;
        }
    });

    card.addEventListener('mouseleave', function () {
        // Restaurar el HTML original al salir del elemento
        if (titleAdded) {
            //card.style.transform = '';
            //card.style.background = '';
            card.style.height = '';
            card.classList.remove('card-expanded');

            // Eliminar los elementos agregados durante mouseenter
            const infoDiv = card.querySelector('div');
            if (infoDiv) {
                card.removeChild(infoDiv);
            }

            titleAdded = false;
        }
    });

});

/**
 * Click in card
 */
cards.forEach((card) => {
    card.addEventListener('click', async function(){
        printModal(card.id);
    });
});

async function printModal(uuid) {
    try {
        const movieJson = await getMovieInfo(uuid);
        if (movieJson) {
            modalTitle.textContent = movieJson.title;
            modalDescription.textContent = movieJson.description;
            modalLink.setAttribute('href', `/movie/${movieJson.uuid}`);
            modalCover.setAttribute('src', `${movieJson.cover_image}`);
            modalDuration.textContent = movieJson.duration_min + ' mins.';

            modal.style.display = 'block';
    
        } else {
            console.error('No se pudo obtener la información de la película.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getMovieInfo(type, uuid){
    const response = await fetch(`http://127.0.0.1:8000/api/${type}s/${uuid}/`);
    if(!response.ok) {
        
    }
    const data = await response.json();
    return data;
}