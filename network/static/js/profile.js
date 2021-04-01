document.addEventListener('DOMContentLoaded',() => {

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
            fetch(`${window.location.href}follow/${button.dataset.id}/`, {
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
}); 
