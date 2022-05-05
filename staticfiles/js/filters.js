document.querySelector('#search-platforms').oninput = function () {
    let val = this.value.trim();
    let filterPlatformItems = document.querySelectorAll('.search-platforms li');
    if (val !== '') {
        filterPlatformItems.forEach(function (elem) {
            if (elem.innerText.toLowerCase().search(val.toLowerCase()) === -1) {
                elem.classList.add('hide');
            }
            else {
              elem.classList.remove('hide');
            }
        });
    }
    else {
        filterPlatformItems.forEach(function (elem) {
            elem.classList.remove('hide');
        });
    }
}

document.querySelector('#search-genres').oninput = function () {
    let val = this.value.trim();
    let filterGenreItems = document.querySelectorAll('.search-genres li');
    if (val !== '') {
        filterGenreItems.forEach(function (elem) {
            if (elem.innerText.toLowerCase().search(val.toLowerCase()) === -1) {
                elem.classList.add('hide');
            }
            else {
              elem.classList.remove('hide');
            }
        });
    }
    else {
        filterGenreItems.forEach(function (elem) {
            elem.classList.remove('hide');
        });
    }
}
