//apprearance

$("body").css("background", "#212");
$("footer").attr("class", "dark");

console.log(window.location.href)

// toggle list vs card view 
$(".option__button").on("click", function() {
    $(".option__button").removeClass("selected");
    $(this).addClass("selected");
    if ($(this).hasClass("option--grid")) {
        $(".results-section").attr("class", "results-section results--grid");
    } else if ($(this).hasClass("option--list")) {
        $(".results-section").attr("class", "results-section results--list");
    }
});

function getGenres() {
    var inputElements = document.getElementsByClassName('genrebox');
    var l = ''
    for (var i = 0; i < inputElements.length; i++) {
        if (inputElements[i].checked) {
            l = l + ' ' + inputElements[i].id
        }
    }
    return l
}


function doSearch() {
    var data = {
        "search": document.getElementById("searchfield").value,
        "popularity": document.getElementById("poprange ").value,
        "genres": getGenres(),
        "isAdult": false,
        "limit": 10

    };
    console.log(window.location.href + "/here");
    console.log(data)
    $.ajax({
        type: "POST",
        url: "localhost:3000/here", //localhost Flask
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(data) {
            document.getElementById('id ').innerHTML = '';
            data.forEach(element => {
                // console.log(element)
                document.getElementById('id ').innerHTML = document.getElementById('id ').innerHTML + CreateView(element);
            })

        }
    });
}

var rangeSlider = function() {
    var slider = $('.range-slider '),
        range = $('.range-slider__range '),
        value = $('.range-slider__value ');

    slider.each(function() {
        value.each(function() {
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function() {
            $(this).next(value).html(this.value);
            console.log(this.value)
        });
    });
};

rangeSlider();


function getMovies() {
    doSearch()
}


function CreateView(m) {
    return ` 
	<div class="profile">
        <div class="profile__image">
			<img src="${m.imgPath}" alt="${m.title}">
			</div>
				<div class="profile__info">
					<h3> ${m.title }
					</h3>
					<p class="profile__info__extra"> ${ m.description }
					</p>
				</div>
				<div class="profile__stats">
					<p class="profile__stats__title"> Relased
					</p>											
					<h5 class="profile__stats__info"> ${ m.bday }
					</h5>
				</div>
				<div class="profile__stats">
					<p class="profile__stats__title"> Country
					</p>											
					<h5 class="profile__stats__info"> ${ m.language }
					</h5>
				</div>
				<div class="profile__stats">
					<p class="profile__stats__title"> Genres
					</p>
					<h5> ${ m.genres }
					</h5>  </div> <div class="profile__stats">
					<p class="profile__stats__title">  Popularity
					</p> <h5 class="profile__stats__info"> ${ m.popularity}
					</h5> </div> <div class="profile__cta"> 
					<a class="button"> 
		 				Search  123 Movies </a>
            	</div>
			</div>
		</div>
	</div>
	</div>
            `
}