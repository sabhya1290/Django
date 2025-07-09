
const articles = document.getElementById('articles-data').textContent;
const data = JSON.parse(articles);
console.log(data[0]);
