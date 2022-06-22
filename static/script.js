"use strict";

const CUPCAKES_URL = "http://localhost:5000/api";

const $cupcakesList = $("#cupcakesList");
const $cupcakesForm = $("#cupcakesForm");


function createCupCakeHTML(cupcake) {
  return `
  <div data-cupcake-id="${cupcake.id}">
    <li>
      ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
      </li>
      <img class="cupcake-img" src="${cupcake.image}"
  </div>
  `;
}

/**Get list of cupcakes in DB. returns [{cupcake},...]*/

async function getStoredCupcakes() {
  const response = await axios.get(`${CUPCAKES_URL}/cupcakes`)
  return response.data.cupcakes;
}

/**adds the DB cupcakes to page */
function showStoredCupcakes(cupcakes) {
  for(let cupcakeInfo of cupcakes) {
    let $cupcake = $(createCupCakeHTML(cupcakeInfo));
    $cupcakesList.append($cupcake)
  }
}

/** handle form for adding of new cupcakes */
async function addNewCupcake(evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $cupcakesList.append(newCupcake);
  $cupcakesForm.trigger("reset");
}

$cupcakesForm.on("submit", addNewCupcake);


/** handle clicking delete: delete cupcake */

async function deleteCupcake(evt) {
  evt.preventDefault();

  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
}

$cupcakesList.on("click", ".delete-button", deleteCupcake);



async function start() {
  const cupcakes = await getStoredCupcakes();
  showStoredCupcakes(cupcakes);
}


start()