document.getElementById('add-company-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('company-name').value;
    const email = document.getElementById('company-email').value;

    const response = await fetch('/add_company', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, contact_email: email })
    });
    
    if (response.ok) 
        {
        alert('Şirket başarıyla eklendi.');
    } else {
        alert('Şirket ekleme başarısız oldu.');
    }
});

C.addEventListener('submit', async (e) => {
    e.preventDefault();
    const company_id = document.getElementById('company-id').value;
    const game_name = document.getElementById('game-name').value;
    const genre = document.getElementById('game-genre').value;
    const cpi = document.getElementById('game-cpi').value;
    const retention_rate = document.getElementById('game-retention').value;

    const response = await fetch('/add_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_id, game_name, genre, cpi, retention_rate })
    });
    
    if (response.ok) {
        alert('Oyun başariyla eklendi.');
    } else {
        alert('Oyun ekleme başarısız oldu.');
    }
});

document.getElementById('evaluate-game-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('evaluate-game-id').value;
    console.log("GameIdForm= "+id);
    const response = await fetch(`/evaluate_game/${id}`, { method: 'POST' });
    const result = await response.json();
    
    console.log("resultId= "+result.resultId);
    if (response.ok) {
        document.getElementById('evaluation-result').innerText = `Karar: ${result.decision ? "Yayınlanabilir" : "Yayınlanamaz"}\nSebep: ${result.reason}`;
    } else {
        document.getElementById('evaluation-result').innerText = "Değerlendirme başarısız oldu.";
    }
});

document.getElementById('get-game-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const gameId = document.getElementById('game-id').value;

    const response= await fetch(`/get_game`,{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({gameId})
    });

    const result = await response.json();//Flaskten return jsonify olarak dönen değere eşit.
    if (response.ok) {
        document.getElementById('get-game-result').innerText = result.game_name;
    }
});









/* Fetch */
function getStudent(url){
    fetch(url)
    .then((response)=>{ /*tek satırdan oluşuyosa .then((response)=> response.json) oto return  */
        return response.json();
    }).then((data)=>{console.log(data)})
    .catch((error=> console.log(error)))
}
//getStudent("https://jsonplaceholder.typicode.com/comments?postId=2");

//async await
function AsynAwaitTest(postid){
    document.querySelector('#customButton').addEventListener("click",async()=>{
        const responseComment= await fetch("https://jsonplaceholder.typicode.com/comments");
        const comments= await responseComment.json();
        //2
        const customComment=await fetch(`https://jsonplaceholder.typicode.com/comments?postId=${postid}`)
        const commentresult= await customComment.json();
        console.log(commentresult);
    })
}

/*const response2 = await fetch(`/get_game`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json' 
    },
    body: JSON.stringify({ "gameId": gameId })
});*/
