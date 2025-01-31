/* Подгрузка товаров OZON */

$(document).ready(function() {
    $.getJSON('/parser', function(data) {
        let container = $('#product-cards-container');
        container.empty();
        data.forEach(product => {
            let card = `
                <div class="main-page__card">
                    <a href="${product.pruduct_url}" target="_blank"><img src="${product.product_photo}" alt="Картинка продукта"></a>
                    <h1 id="product_cost">${product.product_ozon_card_price}</h1>
                    <h3 id="product_name">${product.product_name}</h3>
                    <div class="product_reviews">
                        <span>🌟${product.product_stars}</span>   
                        <span>🗯️ ${product.product_reviews}</span>
                    </div>
                    <div class="product_date">
                        <h5>🛒  Завтра</h5>
                    </div>
                </div>
            `;
            container.append(card);
        });
    });
});



