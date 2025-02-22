const portfolioTab = document.getElementById('portfolio-tab');
const projectTab = document.getElementById('project-tab');
const questionTab = document.getElementById('question-tab');
const answerTab = document.getElementById('answer-tab');

const portfolioPost = document.getElementById('portfolio-post');
const projectPost = document.getElementById('project-post');
const questionPost = document.getElementById('question-post');
const answerPost = document.getElementById('answer-post');

portfolioTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = '#dddddd';
    projectTab.style.backgroundColor = '';
    questionTab.style.backgroundColor = '';
    answerTab.style.backgroundColor = '';

    portfolioPost.style.display = 'grid';
    projectPost.style.display = 'none';
    questionPost.style.display = 'none';
    answerPost.style.display = 'none';
});

projectTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = '';
    projectTab.style.backgroundColor = '#dddddd';
    questionTab.style.backgroundColor = '';
    answerTab.style.backgroundColor = '';

    portfolioPost.style.display = 'none';
    projectPost.style.display = 'grid';
    questionPost.style.display = 'none';
    answerPost.style.display = 'none';
});

questionTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = '';
    projectTab.style.backgroundColor = '';
    questionTab.style.backgroundColor = '#dddddd';
    answerTab.style.backgroundColor = '';

    portfolioPost.style.display = 'none';
    projectPost.style.display = 'none';
    questionPost.style.display = 'grid';
    answerPost.style.display = 'none';
});

answerTab.addEventListener('click', function () {
    portfolioTab.style.backgroundColor = '';
    projectTab.style.backgroundColor = '';
    questionTab.style.backgroundColor = '';
    answerTab.style.backgroundColor = '#dddddd';

    portfolioPost.style.display = 'none';
    projectPost.style.display = 'none';
    questionPost.style.display = 'none';
    answerPost.style.display = 'grid';
});

const profilePostTab = document.querySelectorAll('.profile-post-tab');
const profilePostBody = document.querySelectorAll('.profile-post-body');
let maxHeight = 0;

for (let i = 0; i < 4; i++) {
    profilePostTab[i].click();
    if (maxHeight < profilePostBody[i].offsetHeight) {
        maxHeight = profilePostBody[i].offsetHeight;
    }
}

profilePostBody.forEach(function (body) {
    body.style.height = maxHeight + 'px';
});

portfolioTab.click();
