



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
