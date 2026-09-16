document.addEventListener('DOMContentLoaded', function (){
    document.querySelector('#my-posts').addEventListener('click', function(event) {
        if(event.target.classList.contains('edit-btn')){
            let post_id = event.target.dataset.postId;
            fetch(`/allposts/${post_id}`)
            .then(response => response.json())
            .then(result => {
                event.target.parentElement.innerHTML = `
                    <button class="save-btn btn btn-outline-primary" data-post-id="${post_id}">Save</button>
                    <textarea >${result.content}</textarea>
                    
                `
            })
        } // ends event delagation of click edit button 

        if (event.target.classList.contains('save-btn')){
            const text = event.target.parentElement.querySelector('textarea').value;
            let post_id = event.target.dataset.postId;
            fetch(`/allposts/${post_id}`, {
                method: 'put',
                body: JSON.stringify({content: text})
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                event.target.parentElement.innerHTML = `
                    <strong>Poster: </strong> ${result.post.poster}
                    <strong>Content: </strong> ${text}
                    <strong>Likes: </strong> ${result.post.likes}
                    <strong>TimeStamp: </strong> ${result.post.timestamp}
                    <button class="edit-btn btn btn-outline-primary" data-post-id="${result.post.id}">Edit</button>
                    `
            })
        } // ends event delegation of click save button
    })
})
