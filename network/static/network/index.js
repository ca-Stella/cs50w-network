document.addEventListener('DOMContentLoaded', function() {
    const editBtns = document.querySelectorAll('.edit-btn');
    editBtns.forEach(editBtn => {
        editBtn.addEventListener('click', editPost);
    });

    function editPost() {
        const postid = this.classList[1];
        console.log(postid);
        const editblock = document.querySelector(`#edit-block-${postid}`);
        editblock.style.display = 'block';
        const editBox = document.querySelector(`#edit-${postid}`)
        editBox.innerHTML = document.querySelector(`#post-content-${postid}`).innerHTML;
    
    }
})

