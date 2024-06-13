$(".question_swipe").on('click', function (ev) {
    var this_elem = document.getElementById('p_question_' + $(this).data('id'));

    const request = new Request(
        'http://127.0.0.1:8000/like_question/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'question_id=' + $(this).data('id') + '&islike=' + this_elem.getAttribute('data-islike')
        }
    )

    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => {
                if (response_json.status == "ok") {
                    $('p#score_question_' + $(this).data('id')).text(response_json.likes_count);
                    this_elem.setAttribute("data-islike", response_json.islike);
                    if (response_json.islike == 1) {
                        document.getElementById('image_question_' + $(this).data('id')).setAttribute("src", "/static/img/pressed_like.png");
                    } else {
                        document.getElementById('image_question_' + $(this).data('id')).setAttribute("src", "/static/img/unpressed_like.png");
                    }
                } else if (response_json.status == "not_auth") {
                    window.location.replace("http://127.0.0.1:8000/login/");
                } else {
                    alert('Аn error has occurred');
                }
            }
        )
    );
});

$(".answer_swipe").on('click', function (ev) {
    var this_elem = document.getElementById('p_answer_' + $(this).data('id'));

    const request = new Request(
        'http://127.0.0.1:8000/like_answer/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'answer_id=' + $(this).data('id') + '&islike=' + this_elem.getAttribute('data-islike')
        }
    )

    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => {
                if (response_json.status == "ok") {
                    $('p#score_answer_' + $(this).data('id')).text(response_json.likes_count);
                    this_elem.setAttribute("data-islike", response_json.islike);
                    if (response_json.islike == 1) {
                        document.getElementById('image_answer_' + $(this).data('id')).setAttribute("src", "/static/img/pressed_like.png");
                    } else {
                        document.getElementById('image_answer_' + $(this).data('id')).setAttribute("src", "/static/img/unpressed_like.png");
                    }
                } else if (response_json.status == "not_auth") {
                    window.location.replace("http://127.0.0.1:8000/login/");
                } else {
                    alert('Аn error has occurred');
                }
            }
        )
    );
});

$(".form-check-input").on('click', function (ev) {
    var this_elem = document.getElementById('flex_check_' + $(this).data('id'));

    const request = new Request(
        'http://127.0.0.1:8000/marked_as_correct/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'answer_id=' + $(this).data('id') + '&marked_as_correct=' + this_elem.getAttribute('data-marked_as_correct')
        }
    )

    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => {
                if (response_json.status == "ok") {
                    this_elem.setAttribute("data-marked_as_correct", response_json.marked_as_correct);
                    if (response_json.marked_as_correct == 1) {
                        document.getElementById('flex_check_' + $(this).data('id')).checked = true;
                    } else {
                        document.getElementById('flex_check_' + $(this).data('id')).checked = false;
                    }
                } else if (response_json.status == "not_auth") {
                    window.location.replace("http://127.0.0.1:8000/login/");
                } else {
                    alert('Аn error has occurred');
                }
            }
        )
    );
});
