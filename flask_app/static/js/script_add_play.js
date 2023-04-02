api_id = document.getElementById("api_id").value

getGame(api_id)

async function getGame(id) {
    var response = await fetch("https://api.boardgameatlas.com/api/search?ids="+id+"&pretty=true&client_id=s6BXnmvfwR")
    var data = await response.json()

    document.getElementById("imgGame").src = `${data['games'][0]['images']['medium']}`
    document.getElementById("name").innerHTML = `${data['games'][0]['name']}`
    document.getElementById("inputTitle").value=data['games'][0]['name']
    
    return data;
}