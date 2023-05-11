// form = document.querySelector('#cupcake-form')

// form.addEventListener('submit', (e) => {
//     e.preventDefault();
// })



const $list = $('#cupcake-list')

$('#cupcake-form').submit((e) => {
    e.preventDefault();
    inputs = $('#cupcake-form').serializeArray()
    inputs = inputs.map(function (input) { return input.value; })
    addCupcake(...inputs);
});

async function updateList(){
    $list.empty()
    req = await axios.get('/api/cupcakes');
    cupcakes = req.data.cupcakes;
    for(let cupcake of cupcakes){
        console.log(cupcake)
        new_li = `<li class = "cupcake-li" data-id = ${cupcake.id}>Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}</li>`
        $list.append(new_li)
    }
}

async function addCupcake(flavor, size, rating, image){
    if (image == ''){
        image = null
    }
    res = await axios.post('/api/cupcakes', {
        flavor,
        size,
        rating,
        image
    })
    console.log(res)

    updateList()

}


updateList()
