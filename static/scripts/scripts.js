/* Получение запроса со строки ввода */
document.querySelector('.header__search__container__input').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.querySelector('.header__search').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })




    /* Подгрузка товаров OZON */

    $(document).ready(function() {
        $.getJSON('/parser', function(data) {
            let container = $('#product-cards-container-ozon');
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


    /* Подгрузка товаров YandexMarket */

    $(document).ready(function() {
        $.getJSON('/parser', function(data) {
            let container = $('#product-cards-container-yandex-market');
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


    /* Подгрузка товаров AliExpress */

    $(document).ready(function() {
        $.getJSON('/parser', function(data) {
            let container = $('#product-cards-container-AliExpress');
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


    /* Подгрузка товаров WildBerries */

    $(document).ready(function() {
        $.getJSON('/parser', function(data) {
            let container = $('#product-cards-container-WildBerries');
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
})
