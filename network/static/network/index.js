document.addEventListener('DOMContentLoaded', function() {
    const editBtns = document.querySelectorAll('.edit-btn');
    editBtns.forEach(editBtn => {
        editBtn.addEventListener('click', editPost);
    });

})

function editPost() {
    const postid = this.classList[1];
    console.log(postid);
    const editblock = document.querySelector(`#edit-block-${postid}`);
    editblock.style.display = 'block';
    const editBox = document.querySelector(`#edit-${postid}`);
    editBox.innerHTML = document.querySelector(`#post-content-${postid}`).innerHTML;

    const saveBtn = document.querySelector(`#save-${postid}`);
    saveBtn.addEventListener('click', updatePost);
}

function updatePost() {
    const postid = this.classList[1];
    const editContent = document.querySelector(`#edit-${postid}`).value;
    fetch(`/edit/${postid}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: editContent
        })
    })
    .then(result => {
        const editblock = document.querySelector(`#edit-block-${postid}`);
        editblock.style.display = 'none';
        document.querySelector(`#post-content-${postid}`).innerHTML = editContent;
    })
}

