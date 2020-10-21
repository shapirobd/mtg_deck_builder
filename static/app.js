$("#filter-form").on("submit", async function (evt) {
	// let power;
	// $("#power-form:input").each(() => {
	// 	if ($(this).is(":checked")) {
	// 		let label = $("label[for='" + $(this).attr("id") + "']");
	// 		types.push(label);
	// 	}
	// });

	// let toughness;
	// $("#toughness-form:input").each(() => {
	// 	if ($(this).is(":checked")) {
	// 		let label = $("label[for='" + $(this).attr("id") + "']");
	// 		types.push(label);
	// 	}
	// });

	evt.preventDefault();

	let types = [];
	$("#type-form input").each(function () {
		if ($(this).is(":checked")) {
			let label = $("label[for='" + $(this).attr("id") + "']")[0]["innerText"];
			types.push(label);
		}
	});

	let sets = [];
	$("#set-form input").each(function () {
		if ($(this).is(":checked")) {
			let label = $("label[for='" + $(this).attr("id") + "']")[0]["innerText"];
			sets.push(label);
		}
	});

	let rarities = [];
	$("#rarity-form input").each(function () {
		if ($(this).is(":checked")) {
			let label = $("label[for='" + $(this).attr("id") + "']")[0]["innerText"];
			rarities.push(label);
		}
	});
	let colors = [];
	$("#color-form input").each(function () {
		if ($(this).is(":checked")) {
			let label = $("label[for='" + $(this).attr("id") + "']")[0]["innerText"];
			colors.push(label);
		}
	});

	let resp = await axios.get("http://127.0.0.1:5000/home/filter", {
		params: {
			types: `${types}`,
			sets: `${sets}`,
			rarities: `${rarities}`,
			colors: `${colors}`,
		},
	});
	console.log(resp);
	filteredCards = resp.data.filtered_cards;
	bookmarkedCards = resp.data.bookmarked_cards;
	bookmarkedCardIDs = [];
	for (let card of bookmarkedCards) {
		bookmarkedCardIDs.push(card["id"]);
	}
	$("#cards").empty();
	for (let card of filteredCards) {
		cardHTML = genereateCardHTML(card, bookmarked_cards);
		$("#cards").append(cardHTML);
	}
});

function genereateCardHTML(card) {
	return `
    <div class="col-3">
        <div class="card text-white bg-transparent my-4 mx-3" style="width: 15rem">
            <img
                src="${card.image_url}"
                class="card-img-top mtg-card"
                alt="..."
            />
            <button
                class="btn btn-sm btn-secondary my-1"
                type="button"
                data-toggle="collapse"
                data-target="#info-${card.id}"
                aria-expanded="false"
                aria-controls="collapseExample"
            >
                Show Info
            </button>
            <div class="collapse" id="info-${card.id}">
                <div class="card-body">
                    <h5 class="card-title">${card.name}</h5>
                    {% for attr, value in ${card}.__dict__.items() %} {% if attr !=
                    'image_url' and attr != 'text' and attr != '_sa_instance_state'
                    and value and value != '' %}
                    <p><b>{{attr}}:</b> {{value}}</p>
                    {% else %} {% endif %} {% endfor %}
                </div>
            </div>
            <div class="col">
                <div class="row">
                    {% if ${card.id} in bookmarked_card_ids %}
                        <form action="/cards/${card.id}/unbookmark" method='POST'>
                            <button class="col btn btn-md btn-primary"><i class="fas fa-bookmark"></i></button>
                        </form>
                    {% else %}
                        <form action="/cards/${card.id}/bookmark" method='POST'>
                            <button class="col btn btn-md btn-primary"><i class="far fa-bookmark"></i></button>
                        </form>
                    {% endif %}
                    <button
                        class="col btn btn-sm btn-secondary ml-1"
                        type="button"
                        data-toggle="collapse"
                        data-target="#add-${card.id}"
                        aria-expanded="false"
                        aria-controls="collapseExample"
                    >
                        Add to Deck
                    </button>
                </div>
            </div>
            <div class="">
                <div class="row justify-content-center">
                    <div class="collapse col" id="add-${card.id}">
                        <div>
                            {% if decks | length == 0 %}
                                <a class="col btn btn-md btn-primary my-1" href="/new?card-to-add=${card.id}">Create Deck <i class="fas fa-plus"></i></a>
                            {% else %}
                                {% for deck in decks %}
                                <form action="/cards/${card.id}/decks/{{deck.id}}" method="POST">
                                    <button class="col btn btn-md btn-primary my-1">{{deck.deck_name}}</button>
                                </form>
                                {% endfor %}
                            {% endif %}
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
}
