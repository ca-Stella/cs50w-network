document.addEventListener('DOMContentLoaded', function() {
    const editBtns = document.querySelectorAll('.edit-btn');
    const likeBtns = document.querySelectorAll('.like-btn');

    editBtns.forEach(editBtn => {
        editBtn.addEventListener('click', editPost);
    });
    likeBtns.forEach(likeBtn => {
        likeBtn.addEventListener('click', likePost);
    });

    loadLikes();
})

function editPost() {
    const postid = this.classList[1];
    const postContent = document.querySelector(`#post-content-${postid}`);
    const editblock = document.querySelector(`#edit-block-${postid}`);
    const editBox = document.querySelector(`#edit-${postid}`);

    editblock.style.display = 'block';
    postContent.style.display = 'none';
    editBox.innerHTML = postContent.innerHTML;

    const saveBtn = document.querySelector(`#save-${postid}`);
    saveBtn.addEventListener('click', updatePost);
}

function updatePost() {
    const postid = this.classList[1];
    const editContent = document.querySelector(`#edit-${postid}`).value;
    const postContent = document.querySelector(`#post-content-${postid}`);

    fetch(`/edit/${postid}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: editContent
        })
    })
    .then(result => {
        const editblock = document.querySelector(`#edit-block-${postid}`);
        editblock.style.display = 'none';
        postContent.style.display = 'block';
        document.querySelector(`#post-content-${postid}`).innerHTML = editContent;
    })
}

function likePost() {
    const postid = this.classList[1];
    const currentUser = document.querySelector('#current-user').innerHTML;
    console.log(postid);

    fetch(`/like/${postid}`, {
        method: 'PUT',
        body: JSON.stringify({
            postid: postid,
        })
    })
    .then(response => response.json())
    .then(result => {
        const likeBtnTxt = document.querySelector(`#like-${postid}`);
        const likeBtn = document.querySelector(`#like-btn-${postid}`);
        likeBtnTxt.innerHTML = result['likeCount'];
        if (result['alreadyLiked']) {
            likeBtn.style.backgroundColor = '#fecdcd';
        } else {
            likeBtn.style.backgroundColor = 'white';
        }
    })
}


function loadLikes() {
    const allLikeBtns = document.querySelectorAll('.like-btn');

    allLikeBtns.forEach(likeBtn => {
        const postid = likeBtn.classList[1];
        fetch(`/like/${postid}`)
        .then(response => response.json())
        .then(result => {
            const likeBtnTxt = document.querySelector(`#like-${postid}`);
            const likeBtn = document.querySelector(`#like-btn-${postid}`);
            likeBtnTxt.innerHTML = result['likeCount'];
            if (result['alreadyLiked']) {
                likeBtn.style.backgroundColor = '#fecdcd';
            } else {
                likeBtn.style.backgroundColor = 'white';
            }
        })
    })
}
