document.addEventListener('DOMContentLoaded', function() {
    const editBtns = document.querySelectorAll('.edit-btn');
    const likeBtns = document.querySelectorAll('.like-btn');

    editBtns.forEach(editBtn => {
        editBtn.addEventListener('click', editPost);
    });
    likeBtns.forEach(likeBtn => {
        likeBtn.addEventListener('click', likePost);
    });
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
    console.log(postid);

    // Get data from post
    fetch(`/like/${postid}`)
    .then(response => response.json())
    .then(post => {
        // Print post
        console.log(post);
        console.log('done');
    });

}


