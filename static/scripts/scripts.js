/* Первый вход в окно авторизации */
document.querySelector('#sign_in').addEventListener('click', function(event) {
    showForm('sign_in');
});

/* Функция для отображения формы входа или регистрации. */
function showForm(type) {
    let sign_in = $('.authorization');
    sign_in.empty();

    let formContent = type === 'sign_in' ? getSignInForm() : getSignUpForm();
    sign_in.append(formContent);

    addEventListeners(type);

    $('.dimmer').remove();
    let dim = $('body');
    dim.append('<div class="dimmer"></div>');
}

/* Форма авторизации */
function getSignInForm() {
    return `
        <div class="authorization_container">
            <div id="cross">
                <a id="cross_a"><img id="cross_img" src="static/img/main ico/cross.png" alt="закрыть"></a>
            </div>
            <form method="post" class="form-control">
                <h1>Войдите в аккаунт</h1>
                <input type="email" name='mail' placeholder="Введите почту" class="form-control">
                <input type="password" name='password' placeholder="Введите пароль" class="form-control">
                <button class="btn btn-success">Войти</button>
            </form>
            <div class="horizontal-line-reg"></div>
            <button id="reg_btn" class="reg_btn" href="/registration">Создать аккаунт</button>
        </div>
    `;
}

/* Форма регистрации */
function getSignUpForm() {
    return `
        <div class="authorization_container">
            <div id="cross">
                <a id="cross_a"><img id="cross_img" src="static/img/main ico/cross.png" alt="закрыть"></a>
            </div>
            <form method="post" class="form-control">
                <h1>Создайте аккаунт</h1>
                <p><input type="text" name='nick' placeholder="Введите имя" class="form-control"></p>
                <input type="email" name='mail' placeholder="Введите почту" class="form-control">
                <p>
                    <input type="password" name='password1' placeholder="Введите пароль" class="form-control">
                    <input type="password" name='password2' placeholder="Повторите пароль" class="form-control">
                </p>
                <p>
                    <button class="btn btn-success">Зарегистрироваться</button>
                </p>
            </form>
            <div class="horizontal-line-reg"></div>
            <button id="login_btn" class="reg_btn" href="/registration">Войти</button>
        </div>
    `;
}

/* обработка переключения между регистрацией и авторизацией. Закрытие всплывающего окна */
function addEventListeners(type) {
    document.querySelector('#cross_a')?.addEventListener('click', function(event) {
        let sign_in = $('.authorization');
        sign_in.empty();
        $('.dimmer').remove();
    });

    document.querySelector('#reg_btn')?.addEventListener('click', function(event) {
        showForm('sign_up');
    });

    document.querySelector('#login_btn')?.addEventListener('click', function(event) {
        showForm('sign_in');
    });
}


/* ЛК */
document.querySelector('.theme').addEventListener('click', function(event) {
    let lk = $('.main');
    lk.empty();

    let my_lk = `
    <div class="account">
    <div class="user-info">
        <img src="https://stekloinstrument.ru/image/avatarka.png" alt="аватарка"/>
        <h4>{{ current_user }}</h4>
    </div>
    <span>Корзина</span>
    <span>Избранное</span>
    </div>
    <div class="premium-sub">
        <h1>
            Премиум подписка:
        </h1>
        <h3>
            Статус: активно
        </h3>
    </div>
    `;

    lk.append(my_lk);
});




/* Получение запроса со строки ввода */
document.querySelector('.header__search__container__input').addEventListener('submit', async function(event) {
    event.preventDefault();
    const query = document.querySelector('.header__search').value;

    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
    });
    
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = await response.json()
    console.log(data)

    document.getElementById('loading').style.display = 'none';

    $(document).ready(function() {
        $.getJSON('/parser/ozon', function(data) {
            let ozon = $('.for_ozon');
            ozon.empty();
            
            let title = `
            <div id="ozon-title" class="main-page__ozon">
                <div class="main-page__ozon__title">
                    <img src="/static/img/logo/ozon logo.png" alt="ozon">
                </div>
                <div id="product-cards-container-ozon" class="main-page__ozon__cards">
                </div>
            </div>
            `
            ozon.append(title)
            let container = $('#product-cards-container-ozon');
            container.empty()
            data.forEach(product => {
                let card = `
                        <div class="main-page__card">
                            <a href="${product.Ссылка}" target="_blank">
                                <img src="${product.Фото}" alt="Картинка продукта">
                                <h1 id="product_cost">${product.Цена}</h1>
                                <h3 id="product_name">${product.Название}</h3>
                                <div class="product_reviews">
                                    <span>⭐️${product.Звёзды}</span>   
                                    <span>🗯️ ${product.Оценки}</span>
                                </div>
                                <div class="product_date">
                                    <h5>🛒  ${product.Время}</h5>
                                </div>
                            </a>
                        </div>
                `;
                container.append(card);
            });
        });
    });


    /* Подгрузка товаров YandexMarket */

    $(document).ready(function() {
        $.getJSON('/parser/yandex', function(data) {
            let yandex = $('.for_yandex');
            yandex.empty();
    
            let title = `
            <div id="yandex-market-title" class="main-page__yandex-market">
                <div class="main-page__yandex-market__title">
                    <img src="/static/img/logo/ЯндексМаркет logo.png" 
                            alt="Яндекс Маркет">
                </div>
                <div id="product-cards-container-yandex-market" class="main-page__yandex-market__cards"></div>
            </div>
            `;
            yandex.append(title);
    
            let container = $('#product-cards-container-yandex-market');
            container.empty();
            data.forEach(product => {
                let card = `
                    <div class="main-page__card">
                        <a href="${product.Ссылка}" target="_blank">
                            <img src="${product.Фото}" alt="Картинка продукта">
                            <h1 id="product_cost">${product.Цена} ₽</h1>
                            <h3 id="product_name">${product.Название}</h3>
                            <div class="product_reviews">
                                <span>⭐️${product.Звёзды}</span>
                                <span>🗯️ ${product.Оценки}</span>
                            </div>
                            <div class="product_date">
                                <h5>🛒  ${product.Время}</h5>
                            </div>
                        </a>
                    </div>
                `;
                container.append(card);
            });
        });
    });


    /* Подгрузка товаров AliExpress */

    $(document).ready(function() {
        $.getJSON('/parser/aliexpress', function(data) {
            let aliexpress = $('.for_aliexpress');
            aliexpress.empty();
    
            let title = `
            <div id="aliexpress-title" class="main-page__AliExpress">
                <div class="main-page__AliExpress__title">
                    <img src="/static/img/logo/aliExpress logo.png" 
                            alt="AliExpress">
                </div>
                <div id="product-cards-container-AliExpress" class="main-page__AliExpress__cards"></div>
            </div>
            `;
            aliexpress.append(title);
    
            let container = $('#product-cards-container-AliExpress');
            container.empty();
            data.forEach(product => {
                let card = `
                    <div class="main-page__card">
                        <a href="${product.Ссылка}" target="_blank">
                            <img src="${product.Фото}" alt="Картинка продукта">
                            <h1 id="product_cost">${product.Цена}</h1>
                            <h3 id="product_name">${product.Название}</h3>
                            <div class="product_reviews">
                                <span>⭐️${product.Звёзды}</span>
                                <span>🗯️ Необходимо уточнить</span>
                            </div>
                            <div class="product_date">
                                <h5>🛒  Необходимо уточнить</h5>
                            </div>
                        </a>
                    </div>
                `;
                container.append(card);
            });
        });
    });

    /* Подгрузка товаров WildBerries */

    $(document).ready(function() {
        $.getJSON('/parser/wildberries', function(data) {
            let wildberries = $('.for_wildberries');
            wildberries.empty();
    
            let title = `
            <div id="wildberries-title" class="main-page__WildBerries">
                <div class="main-page__WildBerries__title">
                    <img src="https://trebon.ru/wp-content/uploads/2023/06/7587_wildberrieslogo_388012-e1687698484868.png" 
                            alt="WildBerries">
                </div>
                <div id="product-cards-container-WildBerries" class="main-page__WildBerries__cards"></div>         <!-- Контейнер для карточек товара -->
            </div>

            `;
            wildberries.append(title);
    
            let container = $('#product-cards-container-WildBerries');
            container.empty();
            data.forEach(product => {
                let card = `
                    <div class="main-page__card">
                        <a href="${product.Ссылка}" target="_blank">
                            <img src="${product.Фото}" alt="Картинка продукта">
                            <h1 id="product_cost">${product.Цена}</h1>
                            <h3 id="product_name">${product.Название}</h3>
                            <div class="product_reviews">
                                <span>⭐️${product.Звёзды}</span>
                                <span>🗯️ ${product.Оценки}</span>
                            </div>
                            <div class="product_date">
                                <h5>🛒  ${product.Время}</h5>
                            </div>
                        </a>
                    </div>
                `;
                container.append(card);
            });
        });
    });

    /* Подгрузка товаров Avito */
    /*
    $(document).ready(function() {
        $.getJSON('/parser', function(data) {
            let container = $('#product-cards-container-avito');
            container.empty();
            data.forEach(product => {
                let card = `
                    <div class="main-page__card">
                        <a href="${product.pruduct_url}" target="_blank">
                            <img src="${product.product_photo}" alt="Картинка продукта">
                            <h1 id="product_cost">${product.product_ozon_card_price}</h1>
                            <h3 id="product_name">${product.product_name}</h3>
                            <div class="product_reviews">
                                <span>⭐️${product.product_stars}</span>   
                                <span>🗯️ ${product.product_reviews}</span>
                            </div>
                            <div class="product_date">
                                <h5>🛒  Завтра</h5>
                            </div>
                        </a>
                    </div>
                `;
                container.append(card);
            });
        });
    });
*/
    } catch (error) {
        console.error('Error:', error)
    }
});
