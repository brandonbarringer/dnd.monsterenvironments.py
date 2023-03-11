/*
Function to scrape the data from the D&D Beyond website.
This is a console script that can be run in the browser console.
It will return an array of objects with the name and environments of each monster.

From there, you can copy the data and paste it into a JSON file.
and clean up each object to have the correct format.
data/dnd_beyond/dnd_beyond_monsters.json

*/

function getData() {
  rows = document.querySelectorAll('.info');
  const data = [];
  rows.forEach((row) => {
    const name = row.querySelector('.name .link').innerText;
    const environmentEl = row.querySelector('.monster-environment');
    const environments = (() => {
      const env = environmentEl.querySelector('span');
      if (env && env.hasAttribute('title')) {
        return env.getAttribute('title').split(', ');
      }
      return env.innerText
    })();
    data.push({
      name,
      environments,
    })
  })
  return data;
}
