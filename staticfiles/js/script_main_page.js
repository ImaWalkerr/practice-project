const isMobile = {
	Android: function() {
	    return navigator.userAgent.match(/Android/i);
	},
	BlackBerry: function() {
	    return navigator.userAgent.match(/BlackBerry/i);
	},
	iOS: function() {
	    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	},
	Opera: function() {
	    return navigator.userAgent.match(/Opera Mini/i);
	},
	Windows: function() {
	    return navigator.userAgent.match(/IEMobile/i);
	},
	any: function() {
	    return (
	        isMobile.Android() ||
            isMobile.BlackBerry() ||
            isMobile.iOS() ||
            isMobile.Opera() ||
            isMobile.Windows());
	}
};

//Menu burger//
const iconMenu = document.querySelector('.menu__icon');
if (iconMenu) {
	const MenuHeader = document.querySelector('.header__registration');
	iconMenu.addEventListener("click", function (e) {
		document.body.classList.toggle('_lock');
		iconMenu.classList.toggle('_active');
		MenuHeader.classList.toggle('_active');
	});
}


let body = document.querySelector('body');
if (isMobile.any()) {
	body.classList.add('touch');
	let arrow = document.querySelectorAll('.sidebar__arrow');
	for (i = 0; i < arrow.length; i++) {
		let thisLink = arrow[i].previousElementSibling;
		let subMenu = arrow[i].nextElementSibling;
		let thisArrow = arrow[i];

		arrow[i].addEventListener('click', function () {
			subMenu.classList.toggle('open');
			thisArrow.classList.toggle('active');
		});
	}
} else {
	body.classList.add('mouse');
}