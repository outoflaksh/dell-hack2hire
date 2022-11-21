const express = require("express");
const axios = require("axios");

const app = express();

app.get("/", (req, res) => {
  res.json({ msg: "hello" });
});

app.get("/pokemon/:name", (req, res) => {
  const name = req.params.name;
  const response = axios
    .get(`https://pokeapi.co/api/v2/pokemon/${name}`)
    .then(function (response) {
      res.json(response.data);
    });
});

app.post("/pokemon/add", (req, res) => {
  const poke_name = req.body.poke_name;
});

app.listen(8000);
