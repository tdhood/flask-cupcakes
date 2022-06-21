"use strict";

const CUPCAKES_URL = "http://localhost:5001/";

const $cupcakesList = $("#cupcakesList");
const $cupcakesForm = $("#cupcakesForm");


async function getCupCakes(cakes) {
  const response = await axios({
    baseURL: CUPCAKES_URL,
    url: "/",
    method: "GET",
    params: {
      q: cakes,
    },
  });
  const cupcake = response.data;

  const cupcakeList = cupcake.map(cake => ({
    id: cake.id,
    flavor: cake.flavor,
    rating: cake.rating,
    image: cake.image
  }));
  return cupcakeList;
}
