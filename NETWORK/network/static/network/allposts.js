document.addEventListener('DOMContentLoaded', function() {

    // by default, load the New Post Section on top of All Posts
    allposts();

    // when click the nav bar All Posts, will call allposts() to send get request to fetch all posts
    document.querySelector('#allposts').addEventListener('click', function(event) {
        event.preventDefault();
        allposts();
      });
    
    // when submit the new post form, JS send post request to server
    document.querySelector('#newpost-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/newposts',{
            method: 'POST',
            body: JSON.stringify({
                content:this.querySelector('textarea').value
            })        
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
            document.querySelector('#newpost-form > textarea').value = "";
            allposts();
        })
        .catch(error => {
            alert(error.message);
        });
    });
});


// pagination on allposts page
let currentPage = 1;
document.addEventListener('DOMContentLoaded', function (){
    const prevBtn1 = document.querySelector('#prev-btn1');
    const nextBtn1 = document.querySelector('#next-btn1');

    if (prevBtn1){prevBtn1.addEventListener('click', ()=> {
        if (currentPage > 1) {allposts(currentPage - 1);}});}

    if (nextBtn1){nextBtn1.addEventListener('click', ()=> {
        allposts(currentPage + 1);});}
});




function allposts(page = 1) {
    document.querySelector('#all-posts-container').style.display = 'block';
    document.querySelector('#new-post').style.display = 'block';
    document.querySelector('#user-profile').style.display = 'none';
    // Pagination: 10 on a page
    fetch(`/allposts?page=${page}`)
    .then(response => response.json())
    .then(data => {
        const container = document.querySelector('#all-posts')
        // If first page, hide previous button, if last page, hide next button
        document.querySelector('#next-btn1').style.display = data.has_next ? 'inline-block' : 'none';
        document.querySelector('#prev-btn1').style.display = data.has_previous ? 'inline-block' :'none';
        // everytime click all post in the nav bar will earse the content in all-post div 
        // the heading and button outside of all-post div still remian seeable
        container.innerHTML = '';
        data.posts.forEach(post => {
            const element = document.createElement('div');
            element.innerHTML = `
                <strong>Poster: </strong> <a href="/">${post.poster}</a>
                <strong>Content: </strong> ${post.content}
                <strong>Likes: </strong> ${post.likes}
                <strong>TimeStamp: </strong> ${post.timestamp}
                <span id="like">🤍${post.likes}</span> 
                 `;
            element.className = 'posts';
            container.append(element);
            // call like toggler to add eventlistener to like button
            likeToggle(post, element);
            // call profile to add eventlistener to view user's profile 
            profile(post, element);
                })
                currentPage = page;
            })
        }
        
  

function profile(post, element) {
    // clicking on a username will load that user's profile page
    element.querySelector('a').addEventListener('click', function(event){
        event.preventDefault();
        loadProfilePage(post);
    });
}

function loadProfilePage(post, page=1){
    fetch(`/profile/${post.poster}?page=${page}`)
        .then(response => response.json())
        .then(userprofile => {
            document.querySelector('#all-posts-container').style.display = 'none';
            document.querySelector('#new-post').style.display = 'none';
            document.querySelector('#user-profile').style.display = 'block';
            document.querySelector('#user-profile').innerHTML = 
            // display the number of followers the user has, and the number of people that user follows
            `
            <h3>${userprofile.username}</h3>
            <p id="followers">Followers: ${userprofile.followers}</p>
            <p id="following">Following: ${userprofile.following}</p>
            `;
            // call follow/unfollow toggle button
            followToggle(userprofile);

            // display all of the posts for the user, in reverse chronological order
            userprofile.posts.forEach(post => {
                const element = document.createElement('div');
                element.innerHTML = `
                <strong>Poster: </strong> ${post.poster}
                <strong>Content: </strong> ${post.content}
                <strong>Likes: </strong> ${post.likes}
                <strong>TimeStamp: </strong> ${post.timestamp}
                <span id="like">🤍${post.likes}</span> 
                `;
                document.querySelector('#user-profile').append(element);  
                element.className = "posts"   // same className as the posts in all post 
                // call like toggle to 
                likeToggle(post, element); 
            });
            // pagination to check if there is next/previous page, recursively call the next/previous page
            if(userprofile.has_previous){
                const prevBtn2 = document.createElement('button');
                prevBtn2.innerHTML = `Previous`;
                prevBtn2.className = 'btn btn-outline-primary';
                document.querySelector('#user-profile').append(prevBtn2);
                prevBtn2.addEventListener('click', ()=>{
                    loadProfilePage(post, page-1);
                })    
            }
            if(userprofile.has_next){
                const nextBtn2 = document.createElement('button');
                nextBtn2.innerHTML = `Next`;
                nextBtn2.className = 'btn btn-outline-primary';
                document.querySelector('#user-profile').append(nextBtn2);   
                nextBtn2.addEventListener('click', () => {
                    loadProfilePage (post, page+1);
                })   
            }
        })
}

function likeToggle(post, element){
        element.querySelector('#like').addEventListener('click', function() {
        if (this.innerHTML.includes('🤍')){
            fetch(`/allposts/${post.id}`, {
            method: 'put',
            body: JSON.stringify({likes: post.likes + 1})})
            .then(response => response.json())
            .then(result => {
            alert(result.message)
            this.innerHTML = `❤️${result.post.likes}`;
            post.likes = result.post.likes;})
            .catch (error => alert(error.message));
        }
        else {
            fetch(`/allposts/${post.id}`, {
            method: 'put',
            body: JSON.stringify({likes: post.likes - 1})})
            .then(response => response.json())
            .then(result => {
            alert(result.message)
            this.innerHTML = `🤍${result.post.likes}`;
            post.likes = result.post.likes;})
            .catch(error => alert(error.message));
        }
    }); // ends event listener of like clicks
}


function followToggle(userprofile){
    // add follow/unfollow button if current user is not same as the profile user
    if (userprofile.currentuser != userprofile.username ){
        let button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-primary';
        button.innerHTML = userprofile.is_following ? "Unfollow" : "Follow";
        document.querySelector('#user-profile').append(button);  

        // if click follow/unfollow, send put request to amend in database
        button.addEventListener('click', function() {
        fetch(`/profile/${userprofile.username}`,{
            method:'put',
            body: JSON.stringify({
                is_following: !userprofile.is_following
            })
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
            userprofile.is_following = !userprofile.is_following;
            this.innerHTML = userprofile.is_following ? 'Unfollow':'Follow';
            document.querySelector('#followers').innerHTML = `Followers: ${result.followers}`;
        })
        .catch(error => {alert(error.message)});
        });
    }          
}
    