document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.querySelector('.edit-btn');
    editBtn.addEventListener('click', editPost);
})

function editPost() {
    const editBox = document.createElement('textarea');
    const editBtn = document.querySelector('.edit-btn');
    const parentDiv = editBtn.parentNode;

    parentDiv.append(editBox);
}