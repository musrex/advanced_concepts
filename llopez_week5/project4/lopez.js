document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputElement = document.getElementById('artistSearch');
    const dataListElement = document.getElementById('artistList');

    form.addEventListener('submit', fetchArtworks);
    autoComplete(inputElement, dataListElement);
});


function fetchArtworks(event) {
    event.preventDefault(); // prevent the form from submmitting normally
    const artistTitle = document.getElementById('artistSearch').value;

    if (!artistTitle) {
        alert('Please select a valid artist from the list.');
        return false;
    }

    const url = `https://api.artic.edu/api/v1/artworks/search?q=${artistTitle}&fields=id,title,image_id,artist_title,date_start,description,artwork_type_title`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);
            displayArtworks(data.data);
        })
        .catch(error => {
            console.error('Error fetching artworks:', error);
            alert('Failed to fetch artworks. Please try again.');
        });
 }

function displayArtworks(artworks) {
    const gallery = document.getElementById('artworkGallery');
    gallery.innerHTML = '';

    artworks.forEach(artwork => {
        const artDiv = document.createElement('div');
        artDiv.className = 'artwork';

        const titleElement = document.createElement('h3');
        titleElement.textContent = artwork.title || 'No title available';

        const artistInfoText = artwork.artist_title ? artwork.artist_title : 'Unknown Artist';
        const dateText = artwork.date_start ? ', ' + artwork.date_start : '';
        const artworkTypeText = artwork.artwork_type_title ? '. ' + artwork.artwork_type_title : '';
        const artistTitle = document.createElement('p');
        artistTitle.textContent = artistInfoText + dateText + artworkTypeText;

        if (artwork.image_id) {
            const imgUrl = `https://www.artic.edu/iiif/2/${artwork.image_id}/full/843,/0/default.jpg`;
            const imgElement = new Image();
            imgElement.src = imgUrl;
            imgElement.alt = artwork.title;
            imgElement.style.width = '100%';
            
            imgElement.onload = function() {
                artDiv.appendChild(imgElement);
                artDiv.appendChild(titleElement);
                artDiv.appendChild(artistTitle);
                gallery.appendChild(artDiv);
            };

            imgElement.onerror = function() {
                console.log(`Failed to load image: ${imgUrl}`);
            };

        } else {
            console.log('No image ID for artwork:', artwork);
        }
    });
}

function autoComplete(inputElement, dataListElement) {
    inputElement.addEventListener('input', function() {
        const searchQuery = this.value;
        if (searchQuery.length < 3) {
            return; // Prevent excessive API calls
        }
        const url = `https://api.artic.edu/api/v1/artists/search?q=${encodeURIComponent(searchQuery)}&limit=12`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                dataListElement.innerHTML = ''; // Clear previous results
                data.data.forEach(artist => {
                    const option = document.createElement('option');
                    option.value = artist.title; // Display value in the input
                    dataListElement.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    });

}
