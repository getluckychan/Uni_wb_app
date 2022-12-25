console.log('search.js loaded');

const url = window.location.href;
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultsBox = document.getElementById('results-box');

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
console.log(csrf)
const sendSearchData = (search) => {
    $.ajax(
        {
            type: 'POST',
            url: '/searchuser/',
            data: {
                'csrfmiddlewaretoken': csrf,
                'data': search
            },
            success: (res) => {
                console.log(res.search);
                const data = res.search;
                if (Array.isArray(data)) {
                    resultsBox.innerHTML = '';
                        data.forEach(search => {
                            let avatar = search.avatar;
                            if (avatar === 'None') {
                                avatar = '/media/avatars/img.png'
                            }
                            resultsBox.innerHTML += `
                                <a href="/profile/${search.pk}" class="dropdown-item w-100">
                                <div class="container">
                                    <div class="row">
                                    <div class="col w-50">
                                        <img src="${avatar}"
                                             class="rounded"
                                              height="50px"
                                               alt="User Image">
                                    </div>
                                        <div class="col w-50">
                                            <h5>${search.full_name}</h5>
                                            <p class="text-muted">${search.job}</p>
                                        </div>
                                    </div>
                                </div>
                                </a>`
                        })
                } else {
                    if (searchInput.value.length > 0) {
                        resultsBox.innerHTML = `<b>${data}</b>`;
                    } else {
                        resultsBox.classList.add('not-visible')
                    }
                }
            },
            error: (error) => {
                console.log(error);
            }
        }
    )
}


searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value);
    searchInput.classList.add('dropdown-toggle')
    sendSearchData(e.target.value);
})

