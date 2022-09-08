# selectors

link = response.css('a.product-item-link::attr(href)').get()
or
link = response.css('a.product-item-link').attrib['href']
title = response.css('a.product-item-link::text').get()
price = response.css('span.price::text').get()