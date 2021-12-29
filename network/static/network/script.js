document.addEventListener('DOMContentLoaded', function () {


  if (document.querySelector('#edit') != null) {
    document.querySelector('#edit').onclick = function () {
      title = document.querySelector('.article-title').innerHTML;
      content = document.querySelector('.article-content').innerHTML;
      id = document.querySelector('article').dataset.id

      form = `<form id="compose-form">
            <div class="form-group">
                Title: <input class="form-control" id="compose-title" value="${title}">
            </div>
            <div class="form-group">
                Content: <textarea class="form-control" id="compose-content">${content}</textarea>
            </div>
                   <input type="button" onclick="save_data(${id})" class="btn btn-primary" value="Save">

        </form>`
      document.querySelector('.media-body').innerHTML = form;

    }

  }

});

function save_data(post_id) {
  title = document.querySelector('#compose-title').value;
  content = document.querySelector('#compose-content').value;

  fetch('/post/' + post_id, {
    method: 'PUT',
    body: JSON.stringify({
      title: title,
      content: content
    })
  })

  fetch('/post/' + post_id)
    .then(response => response.json())
    .then(post => {
      tmp = `<div class="article-metadata">
                <a class="mr-2" href="{% url 'user-detail' ${id} %}">${post['author']['username']}</a>
                <small class="text-muted">${post['date_posted']}</small>
            </div>
            <h2 class="article-title">${post['title']}</h2>
            <p class="article-content">${post['content']}</p>
            <div>
                 <a id="edit" class="btn btn-secondary mt-1 mb-1">Edit</a>
            </div>`

      document.querySelector('.media-body').innerHTML = tmp
      location.reload();
    });

}