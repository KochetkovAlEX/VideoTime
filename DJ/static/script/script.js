
// document.addEventListener('DOMContentLoaded', ()=>{
//     var a = document.getElementsByTagName('video')[0]
//     a.volume = 0.2
// })


const com_btn = document.querySelector(".comm_");
const comm_place = document.getElementById('comment')
const like_btn = document.querySelector('.like_')
const like = document.getElementById('like')
const video = document.getElementById('video')

com_btn.addEventListener('click', ()=>{
    if(comm_place.style.display == 'block'){
        comm_place.style.display = 'none'
    }
    else{
        comm_place.style.display = 'block'
    };
})

like_btn.addEventListener('click', ()=>{
    console.log(1)
    if(like.style.backgroundColor == 'gray'){
        like.style.backgroundColor = '#FF0078' 
    }
    else{
        like.style.backgroundColor = 'gray'
    } 
})
