document.addEventListener('DOMContentLoaded', () => {

    let url = 'http://127.0.0.1:8000/'
    
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
            fetch(`${url}like-post/${button.dataset.id}/`, {
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

        document.querySelector('.alert').style.display = 'none';
    })

    document.querySelectorAll('.like-comment-span').forEach(span => {
        span.onclick = (e) => {
            e.preventDefault();
            fetch(`${url}like-comment/${span.dataset.id}/`, {
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

    if (document.querySelector('#edit-profile-icon')) {

        const profileForm = document.querySelector('#profile-info-edit');
        const profileView = document.querySelector('#profile-info-display');

        if (document.querySelector('.errorlist')){
            profileForm.style.display = 'block';
            profileView.style.display = 'none';
        } else {
            document.querySelector('#edit-profile-icon').onclick = () => {
                profileForm.style.display = 'block';
                profileView.style.display = 'none';
            };
    
            document.querySelector('#profile-form-submit').onclick = () => {
                profileForm.style.display = 'none';
                profileView.style.display = 'block';
            };
        }
    }

    if (document.querySelector('#btn-follow')) {

        let button = document.querySelector('#btn-follow');
        button.onclick = (e) => {
            e.preventDefault();
            fetch(`${url}follow`, {
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
              .then(request => request.json())
              .then(data => {
                  console.log(data);
                  button.innerHTML = data.status.toString();
                  let followSpan = document.querySelector('#follower-count');
                  let followerCount = parseInt(followSpan.innerHTML);
                  if (data.status === 'unfollow' ){
                    followSpan.innerHTML = `${followerCount + 1}`;
                  } else {
                    followSpan.innerHTML = `${followerCount - 1}`;
                  }  
              }).catch(error => {
                  console.log(error);
              })
        }
    }
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
