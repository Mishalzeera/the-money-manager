document.ready(bodyFade())

function bodyFade() {
    gsap.fromTo("#body", {opacity: 0},{opacity:1, duration: .4});
}