async function loadHome(idStore, storeSlug, currency) {
    fetch('http://'+storeSlug+'.nubecat.com/api/v1/store/' + idStore)
        .then(response => response.json())
        .then(data => {

            for (let x = 0; x < data.data.length; x++) {

                const name = data.data[x].name;
                if (data.data[x].products.length > 0) {
                    document.getElementById("loadhome").innerHTML += `<h4 class="mt-4 mb-3">${name}</h4>`;
                    let rowProduct = ` <div class="row">`;
                    for (let y = 0; y < data.data[x].products.length; y++) {
                        const productName = data.data[x].products[y].name;
                        const productImage = data.data[x].products[y].image;
                        const id = data.data[x].products[y].id
                        const productPrice = data.data[x].products[y].price;
                        let price = ``;
                        if(productPrice != null){
                            price = `<div class="col">
                                                        <h5 class="text-primary">${currency} ${productPrice}</h5>
                                                    </div>`
                        }

                        rowProduct += `<div class="col-12 col-md-6 col-lg-3 mb-3">
                                        <div class="card">
                                            <a href="http://${storeSlug}.nubecat.com/producto/${id}">
                                                <img class="card-img-top" src="${productImage}" alt=""> 
                                            </a>   
                                            <div class="card-body">
                                                <h6 class="card-title text-secondary">
                                                    <a href="http://${storeSlug}.nubecat.com/producto/${id}" class="text-secondary" title="View Product">${productName}</a>
                                                </h6>
                                                <div class="row">
                                                    `+price+`
                                                    
                                                    <div class="col">
                                                        <a href="#" class="btn btn-success btn-block">Agregar</a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>`
                    }
                    rowProduct += `</div>`;
                    document.getElementById("loadhome").innerHTML += rowProduct;
                }


            }
            document.getElementById("loading").innerHTML = '';
        })
}
