function afficher(lien) {
    const source = lien.getAttribute("src");
    const ctn = document.getElementById('contenu');
    ctn.src = source;
}