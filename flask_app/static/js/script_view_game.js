// api_id = document.getElementById("#api_id").Value
api_id = document.getElementById("api_id").value

getGame(api_id)

async function getGame(id) {
  var response = await fetch("https://api.boardgameatlas.com/api/search?ids="+id+"&pretty=true&client_id=s6BXnmvfwR")
  var data = await response.json()
  document.getElementById("imgGame").src = `${data['games'][0]['images']['medium']}`
  document.getElementById("name").innerHTML = `${data['games'][0]['name']}`
  document.title = `${data['games'][0]['name']} - Details`
  document.getElementById("year").innerHTML = `${data['games'][0]['year_published']}`
  if (data['games'][0]['min_players']==data['games'][0]['max_players']){
    document.getElementById("num_players").innerHTML = `${data['games'][0]['max_players']}`
  }
  else{
    document.getElementById("num_players").innerHTML = `${data['games'][0]['min_players']}-${data['games'][0]['max_players']}`
  }
  document.getElementById("play_time").innerHTML = `${data['games'][0]['min_playtime']}-${data['games'][0]['max_playtime']} minutes`
  document.getElementById("designer").innerHTML = `${data['games'][0]['primary_designer']['name']}`
  document.getElementById("publisher").innerHTML = `${data['games'][0]['primary_publisher']['name']}`
  document.getElementById("description").innerHTML = `${data['games'][0]['description_preview']}`

  // document.getElementById("inputTitle").value=data['games'][0]['name']
  var inputTitles = (document.getElementsByClassName("inputTitle"))
  for (i=0; i<inputTitles.length; i++){
    inputTitles[i].value = data['games'][0]['name']
  }
  return data
}


function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}