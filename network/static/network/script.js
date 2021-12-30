document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('svg').forEach(function (e) {
    e.onclick = function () {
      let likes = parseInt(e.nextElementSibling.innerHTML)
      if (e.firstElementChild.firstElementChild.classList.contains("active")) {
        likes -= 1
      } else {
        likes += 1
      }
      e.firstElementChild.firstElementChild.classList.toggle('active')
      post_id = e.dataset.id

      fetch('/likes/' + post_id, {
        method: 'POST',
        body: JSON.stringify({
          likes: likes,
        })
      })

      e.nextElementSibling.innerHTML = likes
    }
  })

  if (document.querySelector('#edit') != null) {
    document.querySelector('#edit').onclick = function () {
      content = document.querySelector('.article-content').innerHTML;
      id = document.querySelector('article').dataset.id

      form = `<form id="compose-form">
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
  content = document.querySelector('#compose-content').value;

  fetch('/post/' + post_id, {
    method: 'PUT',
    body: JSON.stringify({
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
            <p class="article-content">${post['content']}</p>
            <div>
                 <a id="edit" class="btn btn-secondary mt-1 mb-1">Edit</a>
            </div>`

      document.querySelector('.media-body').innerHTML = tmp
      location.reload();
    });

}