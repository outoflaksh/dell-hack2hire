const express = require("express");
const axios = require("axios");

const app = express();

app.get("/", (req, res) => {
  res.json({ msg: "hello" });
});

app.get("/weather/:city", (req, res) => {
  const city = req.params.city;
  const response = axios
    .get("https://pokeapi.co/api/v2/pokemon/ditto")
    .then(function (response) {
      res.json(response.data);
    });
});

app.listen(8000);
