const suggestions = document.querySelector('.suggestions ul');

let typingTimer;                //timer identifier
let doneTypingInterval = 350;  //time in ms
let myInput = document.querySelector('#searchInput');

// input.addEventListener('keyup', searchHandler);
// suggestions.addEventListener('click', useSuggestion);

//on keyup, start the countdown
myInput.addEventListener('keyup', () => {
    console.log("hi")
	clearTimeout(typingTimer);
    // if (myInput.value) {
    typingTimer = setTimeout(searchHandler, doneTypingInterval);
    // }
});

async function searchHandler(e) { //e is event
	console.log("work")
	const inputVal = document.querySelector('#searchInput').value;
	if (inputVal.length > 0) {
		// results = getGames(inputVal);
    var response = await fetch("https://api.boardgameatlas.com/api/search?name="+inputVal+"&pretty=true&fuzzy_match=true&client_id=s6BXnmvfwR")
    var data = await response.json()
    var results = []
    for (var i=0; i<data['games'].length; i++){
		var result = {}
    	result['name'] = data['games'][i]['name']
		result['img'] = data['games'][i]['images']['small']
		result['id'] = data['games'][i]['id']
		results.push(result)
    }
	console.log(results.length)
	}
	//showSuggestions(results); // originally passed parameter inputVal
  suggestions.innerHTML = '';
  console.log(inputVal)
	if (results.length > 0) {
		for (i = 0; i < results.length; i++) {
			let name = results[i]['name'];

			let id = results[i]['id'];
			// Highlights only the first match
			// TODO: highlight all matches
			// const match = item.match(new RegExp(inputVal, 'i'));
			// item = item.replace(match[0], `<strong>${match[0]}</strong>`);
			// suggestions.innerHTML += `<li><a href="/game/${id}">${name}</a></li>`;
			suggestions.innerHTML += `<a href="/game/${id}"><li>${name}</li></a>`;
		}
		suggestions.classList.add('has-suggestions');
	} 
	else {
		results = [];
		suggestions.innerHTML = '';
		suggestions.classList.remove('has-suggestions');
	}
}



// BELOW CODE IS NOT CURRENTLY IN USE BUT SAVED HERE

// async function getGames(game) {
//   // var game = document.getElementById("searchInput").value
//   var response = await fetch("https://api.boardgameatlas.com/api/search?name="+game+"&pretty=true&client_id=s6BXnmvfwR")
//   var data = await response.json()
//   console.log("1:",data['games'][0]['name'])
//   var searchResults = []
//   for (var i=0; i<data['games'].length; i++){
//     searchResults.push(data['games'][i]['name'])
//   }
//   // document.getElementById("name").innerHTML = `${data['games'][0]['name']}`
//   // console.log(`${data['games'][0]['images']['small']}`)
//   // document.getElementById("imgGame").src = `${data['games'][0]['images']['medium']}`
//   return searchResults
// }

// // function search(str) {
// //   let results = [];
// // 	const val = str.toLowerCase();
// // 	for (i = 0; i < games.length; i++) {
// // 		if (games[i].toLowerCase().indexOf(val) > -1) {
// // 			results.push(games[i]);
// // 		}
// // 	}
// // 	return results;
// // }

// // function searchHandler(e) { //e is event
// // 	const inputVal = e.currentTarget.value;
// // 	let results = [];
// // 	if (inputVal.length > 0) {
// // 		results = getGames(inputVal);
// //     console.log("2: ", results)
// // 	}
// // 	showSuggestions(results); // originally passed parameter inputVal
// // }



// function showSuggestions(results) { //parameter inputVal removed
//   suggestions.innerHTML = '';
// 	if (results.length > 0) {
// 		for (i = 0; i < results.length; i++) {
// 			let item = results[i];
//       console.log("4:",results[i])
// 			// Highlights only the first match
// 			// TODO: highlight all matches
// 			// const match = item.match(new RegExp(inputVal, 'i'));
// 			// item = item.replace(match[0], `<strong>${match[0]}</strong>`);
// 			suggestions.innerHTML += `<li>${item}</li>`;
// 		}
// 		suggestions.classList.add('has-suggestions');
// 	} else {
// 		results = [];
// 		suggestions.innerHTML = '';
// 		suggestions.classList.remove('has-suggestions');
// 	}
// }

// function useSuggestion(e) {
// 	input.value = e.target.innerText;
// 	input.focus();
// 	suggestions.innerHTML = '';
// 	suggestions.classList.remove('has-suggestions');
// }


// // Execute a function when the user presses a key on the keyboard
// // search.addEventListener("keypress", function(event) {
// //   // If the user presses the "Enter" key on the keyboard
// //   if (event.key === "Enter") {
// //     // Cancel the default action, if needed
// //     event.preventDefault();
// //     // Trigger the button element with a click
// //     document.getElementById("searchButton").click();
// //   }
// // });


