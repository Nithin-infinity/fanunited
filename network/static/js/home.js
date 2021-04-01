document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.post-comment-button').forEach( button => {
        button.onclick = () => {
            let commentDiv = document.querySelector(`#comment-section-${button.dataset.id}`);
            if (commentDiv.style.display==='block') {
                commentDiv.style.display = 'none';
            } else {
                commentDiv.style.display = 'block';
            }
        }
    })

    document.querySelectorAll('.post-like-button').forEach(button => {
        button.onclick = (e) => {
            e.preventDefault();
            fetch(`${window.location.href}like-post/${button.dataset.id}/`, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'Accept': 'application/json, text/plain, */*', 
                    'Content-Type': 'application/json',
                },
                body: {
                    "id" : `${button.dataset.id}`,
                }
              })
              .then((response) => response.json())
              .then(function (data) {
                console.log(data);
                document.querySelector(`#like-comment-link-${button.dataset.id}`).innerHTML = `${data.numLikes} liked`;

              })
              .catch(function (error) {
                console.log('Request failed', error);
              });
        }

    })

    document.addEventListener('click', event => {
        if (!event.target.classList.contains('fa-ellipsis-h')){
            document.querySelectorAll('.post-menu-dropdown-container').forEach(div => {
                div.style.display = 'none';
            }
        )}
        
    })

    document.querySelectorAll('.like-comment-span').forEach(span => {
        span.onclick = (e) => {
            e.preventDefault();
            fetch(`${window.location.href}like-comment'/${span.dataset.id}/`, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'Accept': 'application/json, text/plain, */*', 
                    'Content-Type': 'application/json',
                },
                body: {
                    "id" : `${span.dataset.id}`,
                }
              })
              .then((response) => response.json())
              .then(function (data) {
                console.log(data);
                document.querySelector(`#like-comment-icon-${span.dataset.id}`).innerHTML = `${data.numLikes}`;

              })
              .catch(function (error) {
                console.log('Request failed', error);
              });
        }

    })
})


function showMenu (icon){
    document.querySelectorAll('.post-menu-dropdown-container').forEach(div => {
        if (div.dataset.id !== icon.dataset.id) {
            div.style.display = 'none';
        }
    })
    let displayMenu = document.getElementById(`post-menu-dropdown-container-${icon.dataset.id}`);
    if (displayMenu.style.display === 'block'){
        displayMenu.style.display = 'none';
    } else {
        displayMenu.style.display = 'block';
    }
}
