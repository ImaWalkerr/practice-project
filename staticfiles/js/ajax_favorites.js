//Django AJAX
//Cookie obtainer Django
function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i])
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

const csrftoken = getCookie('csrftoken')

//Setup ajax connections safe
function csrfSafeMethod(method) {
    // these HTTP methods do not  require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$.ajaxSetup({
    beforeSend: (xhr, settings) => {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})
// End Django AJAX

//Add to favorites
const add_to_favorites_url ='/add/'
const remove_from_favorites_url = '/remove/'
const favorites_api_url = '/api/'
const added_for_favorites_class = 'added'

function add_to_favorites() {
    $('.add-to-favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const type = $(el).data('type')
            const id = $(el).data('id')
            const genres = $(el).data('genres')
            const url_root = $(el).data('url_root')

            if( $(e.target).hasClass(added_for_favorites_class) ) {
                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                        genres: genres,
                        url_root: url_root,
                    },
                    success: (data) => {
                        $(el).removeClass(added_for_favorites_class).text('ReMust')
                        get_session_favorites_statistics()
                    }
                })
            } else {
                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                        genres: genres,
                        url_root: url_root,
                    },
                    success: (data) => {
                        $(el).addClass(added_for_favorites_class).text('UnMust')
                        get_session_favorites_statistics()
                    }
                })
            }
        })
    })
}

//Save favorites list for user
function get_session_favorites() {
    get_session_favorites_statistics()

    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {
                $('.add-to-favorites').each((index, el) => {
                    const type = $(el).data('type')
                    const id = $(el).data('id')
                    const genres = $(el).data('genres')
                    const url_root = $(el).data('url_root')

                    if (json[i].type == type && json[i].id == id && json[i].genres == genres && json[i].url_root == url_root) {
                        $(el).addClass(added_for_favorites_class).text('UnMust')
                    }
                })
            }
        }
    })
}


function get_session_favorites_statistics() {
    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            $('#favorites_statistics').empty()
            let sites_plural = json.length > 1 ? ' musts ' : ' must '
            $('#favorites_statistics').html(json.length + sites_plural)
        }
        if (json == null) {
            $('#favorites_statistics').empty()
        }
    })
}


$(document).ready(function () {
    add_to_favorites()
    get_session_favorites()
})
